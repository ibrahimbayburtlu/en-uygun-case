

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
    # Graf ve giriş derecesi başlatma
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    # Bağımlılıkları grafa ekle
    for task, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1

    # Her görevin başlangıç ve bitiş zamanlarını tutacak sözlükler
    task_start_time = {task: 0 for task in tasks}
    task_finish_time = {task: 0 for task in tasks}
    
    # Bağımsız görevleri bul
    ready_tasks = []
    for task in tasks:
        if in_degree[task] == 0:
            ready_tasks.append(task)
    
    execution_order = []
    current_time = 0

    while ready_tasks:
        # Hazır görevleri işle
        task = ready_tasks.pop(0)
        execution_order.append(task)
        
        # Görevin başlangıç zamanını belirle
        # Eğer bağımlılıkları varsa, en son biten bağımlılığın zamanını al
        dependencies_finish_time = 0
        if dependencies[task]:
            dependencies_finish_time = max(task_finish_time[dep] for dep in dependencies[task])
        task_start_time[task] = max(current_time, dependencies_finish_time)
        
        # Görevin bitiş zamanını hesapla
        task_finish_time[task] = task_start_time[task] + completion_time[task]
        current_time = task_finish_time[task]

        # Bağımlı görevleri kontrol et
        for dependent in graph[task]:
            in_degree[dependent] -= 1
            # Eğer görev hazırsa, sıraya ekle
            if in_degree[dependent] == 0:
                ready_tasks.append(dependent)
        
        # Hazır görevleri bitiş zamanlarına göre sırala
        ready_tasks.sort(key=lambda x: task_start_time[x] + completion_time[x])

    min_completion_time = max(task_finish_time.values())
    return min_completion_time, execution_order

# Ana fonksiyon
def main():
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
