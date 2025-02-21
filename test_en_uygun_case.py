import unittest
from en_uygun_case import calculate_task_duration_and_order

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

    def test_job_j_complex_dependencies(self):
        # Job J'nin karmaşık bağımlılıkları için test
        tasks = ['A', 'B', 'C', 'D', 'E', 'F']
        dependencies = {
            'A': [],
            'B': [],
            'C': [],
            'D': ['A'],
            'E': ['B', 'C'],
            'F': ['D', 'E']
        }
        completion_time = {
            'A': 3,
            'B': 2,
            'C': 4,
            'D': 5,
            'E': 2,
            'F': 3
        }
        expected_time = 19  # Tüm sürelerin toplamı: 3 + 2 + 4 + 5 + 2 + 3
        actual_time, actual_order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        
        # Bağımlılık sıralamasını kontrol et
        self.assertTrue(actual_order.index('A') < actual_order.index('D'))
        self.assertTrue(actual_order.index('B') < actual_order.index('E'))
        self.assertTrue(actual_order.index('C') < actual_order.index('E'))
        self.assertTrue(actual_order.index('D') < actual_order.index('F'))
        self.assertTrue(actual_order.index('E') < actual_order.index('F'))

if __name__ == '__main__':
    unittest.main() 