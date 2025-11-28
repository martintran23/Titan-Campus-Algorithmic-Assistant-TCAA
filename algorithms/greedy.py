# Greedy scheduler (sort by value/time ratio)
def greedy_schedule(tasks, time_available):
    # tasks = [(name, time, value)]
    tasks_sorted = sorted(tasks, key=lambda x: x[2]/x[1], reverse=True)

    total_time = 0
    total_value = 0
    chosen = []

    for name, t, val in tasks_sorted:
        if total_time + t <= time_available:
            total_time += t
            total_value += val
            chosen.append((name, t, val))

    return chosen, total_time, total_value
