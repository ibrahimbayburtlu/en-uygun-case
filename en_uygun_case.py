from collections import deque

def collect_task_names():
    tasks = []
    print("Enter tasks (leave empty line to finish):")
    while True:
        task = input("Task name: ").strip()
        if not task:
            break
        tasks.append(task)
    return tasks

def collect_task_dependencies(tasks):
    dependencies = {task: [] for task in tasks}
    print("\nEnter dependencies for each task (press enter if no dependencies):")
    for task in tasks:
        print(f"\nEnter dependencies for task {task} (separate with commas):")
        deps = input().strip()
        if deps:
            dependencies[task] = [dep.strip() for dep in deps.split(',')]
    return dependencies

def collect_task_durations(tasks):
    completion_time = {}
    print("\nEnter completion time for each task:")
    for task in tasks:
        while True:
            try:
                time = int(input(f"Time for task {task}: "))
                if time > 0:
                    completion_time[task] = time
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    return completion_time

def calculate_optimal_schedule(tasks, dependencies, completion_time):
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for task, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1

    queue = deque()
    task_finish_time = {task: 0 for task in tasks}
    current_time = 0 

    for task in tasks:
        if in_degree[task] == 0:
            queue.append(task)

    execution_order = []
    while queue:
        task = queue.popleft()
        execution_order.append(task)
        current_time += completion_time[task]
        task_finish_time[task] = current_time

        for dependent in graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return current_time, execution_order

def main():    
    tasks = collect_task_names()
    if not tasks:
        print("No tasks were entered!")
        return
    
    dependencies = collect_task_dependencies(tasks)
    completion_time = collect_task_durations(tasks)
    
    total_duration, execution_sequence = calculate_optimal_schedule(tasks, dependencies, completion_time)
    
    print("\nResults:")
    print("Minimum Completion Time:", total_duration)
    print("Execution Order:", execution_sequence)

if __name__ == "__main__":
    main()
