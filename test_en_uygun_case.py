import unittest
from en_uygun_case import calculate_optimal_schedule
from unittest.mock import patch
from io import StringIO
from en_uygun_case import main

class TestTaskScheduling(unittest.TestCase):
    def test_should_handle_linear_task_dependencies(self):
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
        
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, expected_order)

    def test_should_handle_parallel_task_execution(self):
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
        expected_time = 11
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))

    def test_should_handle_complex_task_dependencies(self):
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
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('D'))
        self.assertTrue(actual_order.index('D') < actual_order.index('E'))

    def test_should_handle_tasks_without_dependencies(self):
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
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(len(actual_order), 3)

    def test_should_handle_empty_dependencies(self):
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
        expected_time = 6
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(set(actual_order), set(tasks))

    def test_should_handle_linear_dependency_chain(self):
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
        expected_time = 7
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, ['A', 'B', 'C', 'D'])

    def test_should_handle_parallel_execution_paths(self):
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
        expected_time = 12
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('E'))

    def test_should_handle_job_j_scenario(self):
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
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        expected_time = 19
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('D'))
        self.assertTrue(actual_order.index('B') < actual_order.index('E'))
        self.assertTrue(actual_order.index('C') < actual_order.index('E'))
        self.assertTrue(actual_order.index('D') < actual_order.index('F'))
        self.assertTrue(actual_order.index('E') < actual_order.index('F'))

    def test_should_handle_diamond_dependency_pattern(self):
        tasks = ['A', 'B', 'C', 'D']
        dependencies = {
            'A': [],
            'B': ['A'],
            'C': ['A'],
            'D': ['B', 'C']
        }
        completion_time = {
            'A': 2,
            'B': 3,
            'C': 4,
            'D': 2
        }
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        expected_time = 11
        self.assertEqual(actual_time, expected_time)
        self.assertTrue(actual_order.index('A') < actual_order.index('B'))
        self.assertTrue(actual_order.index('A') < actual_order.index('C'))
        self.assertTrue(actual_order.index('B') < actual_order.index('D'))
        self.assertTrue(actual_order.index('C') < actual_order.index('D'))

    def test_should_handle_single_task(self):
        tasks = ['A']
        dependencies = {'A': []}
        completion_time = {'A': 5}
        actual_time, actual_order = calculate_optimal_schedule(tasks, dependencies, completion_time)
        expected_time = 5
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_order, ['A'])

class TestMainFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('en_uygun_case.collect_task_names')
    @patch('en_uygun_case.collect_task_dependencies')
    @patch('en_uygun_case.collect_task_durations')
    def test_should_execute_main_successfully(self, mock_completion_times, mock_dependencies, mock_tasks, mock_stdout):
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
    @patch('en_uygun_case.collect_task_names')
    def test_should_handle_empty_task_list(self, mock_tasks, mock_stdout):
        mock_tasks.return_value = []
        main()
        self.assertIn("No tasks were entered!", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main() 