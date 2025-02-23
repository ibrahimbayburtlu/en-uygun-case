import unittest
from en_uygun_case import calculate_task_duration_and_order
from unittest.mock import patch
from io import StringIO
from en_uygun_case import main

class TestTaskScheduling(unittest.TestCase):
    def test_simple_linear_tasks(self):
        # Basit doğrusal görevler için test
        tasks = ['A', 'B', 'C']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['B']
        }
        completion_time = {
            'A': 2,
            'B': 3,
            'C': 4
        }
        expected_time = 9
        expected_order = ['A', 'B', 'C']
        
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, expected_order)

    def test_parallel_tasks(self):
        # Bağımsız başlangıç görevleri olan, sıralı çalışacak görevler için test
        tasks = ['A', 'B', 'C', 'D']
        dependencies = {
            'A': [],
            'B': [],
            'C': ['A'],
            'D': ['B']
        }
        completion_time = {
            'A': 2,
            'B': 3,
            'C': 4,
            'D': 2
        }
        expected_time = 11  # A(2) + B(3) + C(4) + D(2) = 11
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))

    def test_complex_dependencies(self):
        # Karmaşık bağımlılıklar için test
        tasks = ['A', 'B', 'C', 'D', 'E']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['A'],
            'D': ['B', 'C'],
            'E': ['D']
        }
        completion_time = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 2
        }
        expected_time = 12
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        # Bağımlılık sıralamasını kontrol et    
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('D'))
        self.assertTrue(actual_order.index('D') < actual_order.index('E'))

    def test_no_dependencies(self):
        # Bağımlılık olmayan görevler için test
        tasks = ['A', 'B', 'C']
        dependencies = {
            'A': [],
            'B': [],
            'C': []
        }
        completion_time = {
            'A': 1,
            'B': 2,
            'C': 3
        }
        expected_time = 6
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(len(actual_order), 3)

    def test_empty_dependencies(self):
        # Boş bağımlılık durumu için test
        tasks = ['A', 'B', 'C']
        dependencies = {
            'A': [],
            'B': [],
            'C': []
        }
        completion_time = {
            'A': 2,
            'B': 3,
            'C': 1
        }
        expected_time = 6  # Tek worker olduğu için tüm sürelerin toplamı (2 + 3 + 1)
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        # Sıralama önemli değil çünkü bağımlılık yok
        self.assertEqual(set(actual_order), set(tasks))

    def test_linear_dependencies(self):
        # Doğrusal bağımlılıklar için test
        tasks = ['A', 'B', 'C', 'D']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['B'],
            'D': ['C']
        }
        completion_time = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 1
        }
        expected_time = 7  # 1 + 2 + 3 + 1
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        # Sıralama kontrolü
        self.assertEqual(actual_order, ['A', 'B', 'C', 'D'])

    def test_parallel_paths(self):
        # Paralel yollar içeren bağımlılıklar için test
        tasks = ['A', 'B', 'C', 'D', 'E']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['A'],
            'D': ['B'],
            'E': ['C']
        }
        completion_time = {
            'A': 2,
            'B': 3,
            'C': 4,
            'D': 1,
            'E': 2
        }
        expected_time = 12  # A(2) + max(B->D(4), C->E(6)) = 12
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        # Bağımlılık sıralamasını kontrol et
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('E'))

    def test_job_j_scenario(self):
        tasks = ['A', 'B', 'C', 'D', 'E', 'F']
        dependencies = {
            'A': [],        # Bağımsız
            'B': [],        # Bağımsız
            'C': [],        # Bağımsız
            'D': ['A'],     # A'ya bağımlı
            'E': ['B', 'C'], # B ve C'ye bağımlı
            'F': ['D', 'E']  # D ve E'ye bağımlı
        }
        completion_time = {
            'A': 3,  # 0-3
            'B': 2,  # 3-5
            'C': 4,  # 5-9
            'D': 5,  # 9-14 (A'dan sonra)
            'E': 2,  # 14-16 (B ve C'den sonra)
            'F': 3   # 16-19 (D ve E'den sonra)
        }

        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)

        # Bağımlılık kontrolleri
        self.assertTrue(actual_order.index('A') < actual_order.index('D'))
        self.assertTrue(actual_order.index('B') < actual_order.index('E'))
        self.assertTrue(actual_order.index('C') < actual_order.index('E'))
        self.assertTrue(actual_order.index('D') < actual_order.index('F'))
        self.assertTrue(actual_order.index('E') < actual_order.index('F'))

        # Toplam süre kontrolü
        expected_time = 19  # Tek worker ile toplam süre
        self.assertEqual(actual_time, expected_time)

        print("\nJob J Test Sonuçları:")
        print(f"Sıralama: {actual_order}")
        print(f"Toplam Süre: {actual_time}")
        print("\nGörev Zamanlaması (Tek Worker):")
        current_time = 0
        for task in actual_order:
            start_time = current_time
            end_time = start_time + completion_time[task]
            print(f"{task}: {start_time}-{end_time}")
            current_time = end_time

    def test_diamond_pattern(self):

        tasks = ['A', 'B', 'C', 'D']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['A'],
            'D': ['B', 'C']
        }
        completion_time = {
            'A': 2,  # 0-2
            'B': 3,  # 2-5
            'C': 4,  # 5-9
            'D': 2   # 9-11
        }
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        expected_time = 11
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('D'))

    def test_long_chain(self):

        tasks = ['A', 'B', 'C', 'D', 'E']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['B'],
            'D': ['C'],
            'E': ['D']
        }
        completion_time = {
            'A': 1,  # 0-1
            'B': 2,  # 1-3
            'C': 3,  # 3-6
            'D': 2,  # 6-8
            'E': 1   # 8-9
        }
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        expected_time = 9
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, ['A', 'B', 'C', 'D', 'E'])

    def test_multiple_independent_chains(self):

        tasks = ['A', 'B', 'C', 'D', 'E', 'F']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['B'],
            'D': [],
            'E': ['D'],
            'F': []
        }
        completion_time = {
            'A': 2,  # 0-2
            'B': 3,  # 2-5
            'C': 2,  # 5-7
            'D': 4,  # 7-11
            'E': 3,  # 11-14
            'F': 1   # 14-15
        }
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        expected_time = 15
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('B') < actual_order.index('C'))
        self.assertTrue(actual_order.index('D') < actual_order.index('E'))

    def test_single_task(self):
        tasks = ['A']
        dependencies = {'A': []}
        completion_time = {'A': 5}
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        expected_time = 5
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, ['A'])

class TestMainFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('en_uygun_case.get_tasks_from_user')
    @patch('en_uygun_case.get_dependencies_from_user')
    @patch('en_uygun_case.get_completion_times')
    def test_successful_execution(self, mock_completion_times, mock_dependencies, mock_tasks, mock_stdout):

        mock_tasks.return_value = ['A', 'B', 'C']
        mock_dependencies.return_value = {
            'A': [],
            'B': ['A'],
            'C': ['B']
        }
        mock_completion_times.return_value = {
            'A': 2,
            'B': 3,
            'C': 4
        }


        main()


        output = mock_stdout.getvalue()
        self.assertIn("Results:", output)
        self.assertIn("Minimum Completion Time:", output)
        self.assertIn("Execution Order:", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('en_uygun_case.get_tasks_from_user')
    def test_no_tasks_entered(self, mock_tasks, mock_stdout):

        mock_tasks.return_value = []


        main()


        self.assertIn("No tasks were entered!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('en_uygun_case.get_tasks_from_user')
    @patch('en_uygun_case.get_dependencies_from_user')
    @patch('en_uygun_case.get_completion_times')
    def test_complex_task_scenario(self, mock_completion_times, mock_dependencies, mock_tasks, mock_stdout):

        mock_tasks.return_value = ['A', 'B', 'C', 'D', 'E', 'F']
        mock_dependencies.return_value = {
            'A': [],
            'B': [],
            'C': [],
            'D': ['A'],
            'E': ['B', 'C'],
            'F': ['D', 'E']
        }
        mock_completion_times.return_value = {
            'A': 3,
            'B': 2,
            'C': 4,
            'D': 5,
            'E': 2,
            'F': 3
        }


        main()


        output = mock_stdout.getvalue()
        self.assertIn("Results:", output)
        self.assertIn("Minimum Completion Time:", output)
        self.assertIn("Execution Order:", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('en_uygun_case.get_tasks_from_user')
    @patch('en_uygun_case.get_dependencies_from_user')
    @patch('en_uygun_case.get_completion_times')
    def test_single_task_scenario(self, mock_completion_times, mock_dependencies, mock_tasks, mock_stdout):

        mock_tasks.return_value = ['A']
        mock_dependencies.return_value = {'A': []}
        mock_completion_times.return_value = {'A': 5}


        main()


        output = mock_stdout.getvalue()
        self.assertIn("Results:", output)
        self.assertIn("Minimum Completion Time:", output)
        self.assertIn("Execution Order:", output)

if __name__ == '__main__':
    unittest.main() 