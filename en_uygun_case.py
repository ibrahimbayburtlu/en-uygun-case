from collections import deque

# Kullanıcıdan görevleri al
def get_tasks_from_user():
    tasks = []
    print("Enter tasks (leave empty line to finish):")
    while True:
        task = input("Task name: ").strip()
        if not task:
            break
        tasks.append(task)
    return tasks

# Kullanıcıdan bağımlılıkları al
def get_dependencies_from_user(tasks):
    dependencies = {task: [] for task in tasks}
    print("\nEnter dependencies for each task (press enter if no dependencies):")
    for task in tasks:
        print(f"\nEnter dependencies for task {task} (separate with commas):")
        deps = input().strip()
        if deps:
            dependencies[task] = [dep.strip() for dep in deps.split(',')]
    return dependencies

# Kullanıcıdan tamamlama sürelerini al
def get_completion_times(tasks):
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

# En uygun tamamlama süresini ve sıralamayı bul     
def calculate_task_duration_and_order(tasks, dependencies, completion_time):
    """
    This solution uses a topological sort algorithm with the following approach:
    1. Creates a dependency graph using adjacency lists
    2. Uses a queue-based approach (deque) to process tasks in order
    3. Tracks in-degree (number of dependencies) for each task
    4. Calculates minimum completion time by processing tasks in dependency order
    
    Time Complexity: O(V + E) where V is number of tasks and E is number of dependencies
    Space Complexity: O(V) for storing the queue and result
    """
    # Bağımlılık grafı oluştur
    graph = {task: [] for task in tasks}
    # Girdi derecesi başlatma
    in_degree = {task: 0 for task in tasks}
    # Bağımlılıkları grafa ekle
    for task, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1

    # Sıralama için kuyruk oluştur
    queue = deque()
    # Görevin tamamlanma zamanı
    task_finish_time = {task: 0 for task in tasks}
    # Mevcut zaman
    current_time = 0 

    # Bağımlılık olmayan görevleri kuyruğa ekle
    for task in tasks:
        if in_degree[task] == 0:
            queue.append(task)

    # Sıralama için liste oluştur
    execution_order = []
    while queue:
        task = queue.popleft()
        execution_order.append(task)
        #  Mevcut zamana görevin tamamlanma süresini ekle
        current_time += completion_time[task]
        task_finish_time[task] = current_time

        # Bağımlı görevlerin giriş derecesini azalt
        for dependent in graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # En kısa tamamlanma süresi ve sıralama
    min_completion_time = current_time
    return min_completion_time, execution_order


def main():
    # Brief description of the program
    print("Task Scheduler and Optimizer")
    print("This program finds the optimal order to complete tasks with dependencies")
    print("and calculates the minimum completion time.\n")
    
    tasks = get_tasks_from_user()
    if not tasks:
        print("No tasks were entered!")
        return
    
    dependencies = get_dependencies_from_user(tasks)
    completion_time = get_completion_times(tasks)
    

    min_time, order = calculate_task_duration_and_order(tasks, dependencies, completion_time)
    

    print("\nResults:")
    print("Minimum Completion Time:", min_time)
    print("Execution Order:", order)

if __name__ == "__main__":
    main()
