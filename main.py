from collections import deque

# -------------------------------
# Process Class
# -------------------------------
class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.ct = 0
        self.tat = 0
        self.wt = 0


# -------------------------------
# Input Function
# -------------------------------
def take_input():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        pid = i + 1
        at = int(input(f"Enter Arrival Time for P{pid}: "))
        bt = int(input(f"Enter Burst Time for P{pid}: "))
        processes.append(Process(pid, at, bt))

    return processes


# -------------------------------
# Display Function
# -------------------------------
def display(processes):
    print("\nPID\tAT\tBT\tCT\tTAT\tWT")

    total_tat = 0
    total_wt = 0

    for p in processes:
        total_tat += p.tat
        total_wt += p.wt
        print(f"P{p.pid}\t{p.at}\t{p.bt}\t{p.ct}\t{p.tat}\t{p.wt}")

    print("\nAverage Turnaround Time:", total_tat / len(processes))
    print("Average Waiting Time:", total_wt / len(processes))


# -------------------------------
# Gantt Chart
# -------------------------------
def print_gantt(gantt):
    print("\nGantt Chart:")
    for p in gantt:
        print(f"| P{p[0]} ", end="")
    print("|")

    print("0", end="")
    for p in gantt:
        print(f"   {p[2]}", end="")
    print("\n")


# -------------------------------
# FCFS
# -------------------------------
def fcfs(processes):
    processes.sort(key=lambda x: x.at)
    time = 0
    gantt = []

    for p in processes:
        if time < p.at:
            time = p.at

        start = time
        time += p.bt
        end = time

        gantt.append((p.pid, start, end))

        p.ct = end
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt

    print_gantt(gantt)
    return processes


# -------------------------------
# SJF (Non-Preemptive)
# -------------------------------
def sjf(processes):
    n = len(processes)
    completed = 0
    time = 0
    visited = [False] * n
    gantt = []

    while completed < n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if processes[i].at <= time and not visited[i]:
                if processes[i].bt < min_bt:
                    min_bt = processes[i].bt
                    idx = i

        if idx != -1:
            start = time
            time += processes[idx].bt
            end = time

            gantt.append((processes[idx].pid, start, end))

            processes[idx].ct = end
            processes[idx].tat = end - processes[idx].at
            processes[idx].wt = processes[idx].tat - processes[idx].bt

            visited[idx] = True
            completed += 1
        else:
            time += 1

    print_gantt(gantt)
    return processes


# -------------------------------
# Round Robin
# -------------------------------
def round_robin(processes, quantum):
    queue = deque()
    time = 0
    gantt = []

    processes.sort(key=lambda x: x.at)
    remaining_bt = {p.pid: p.bt for p in processes}

    i = 0
    n = len(processes)

    while i < n or queue:
        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1

        if queue:
            p = queue.popleft()

            start = time
            exec_time = min(quantum, remaining_bt[p.pid])
            time += exec_time
            end = time

            gantt.append((p.pid, start, end))

            remaining_bt[p.pid] -= exec_time

            while i < n and processes[i].at <= time:
                queue.append(processes[i])
                i += 1

            if remaining_bt[p.pid] > 0:
                queue.append(p)
            else:
                p.ct = time
                p.tat = p.ct - p.at
                p.wt = p.tat - p.bt
        else:
            time += 1

    print_gantt(gantt)
    return processes


# -------------------------------
# SRTF (Preemptive SJF)
# -------------------------------
def srtf(processes):
    n = len(processes)
    remaining_bt = [p.bt for p in processes]

    time = 0
    completed = 0
    gantt = []
    prev = -1

    while completed != n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if processes[i].at <= time and remaining_bt[i] > 0:
                if remaining_bt[i] < min_bt:
                    min_bt = remaining_bt[i]
                    idx = i

        if idx != -1:
            if prev != idx:
                gantt.append((processes[idx].pid, time))
                prev = idx

            remaining_bt[idx] -= 1
            time += 1

            if remaining_bt[idx] == 0:
                processes[idx].ct = time
                processes[idx].tat = time - processes[idx].at
                processes[idx].wt = processes[idx].tat - processes[idx].bt
                completed += 1
        else:
            time += 1

    print("\nGantt Chart:")
    for g in gantt:
        print(f"| P{g[0]} ", end="")
    print("|")

    return processes


# -------------------------------
# MAIN PROGRAM
# -------------------------------
if __name__ == "__main__":
    print("CPU Scheduling Simulator")
    print("------------------------")
    print("1. FCFS")
    print("2. SJF")
    print("3. Round Robin")
    print("4. SRTF")

    choice = int(input("Enter your choice: "))

    processes = take_input()

    if choice == 1:
        print("\nRunning FCFS...\n")
        result = fcfs(processes)

    elif choice == 2:
        print("\nRunning SJF...\n")
        result = sjf(processes)

    elif choice == 3:
        quantum = int(input("Enter Time Quantum: "))
        print("\nRunning Round Robin...\n")
        result = round_robin(processes, quantum)

    elif choice == 4:
        print("\nRunning SRTF...\n")
        result = srtf(processes)

    else:
        print("Invalid choice")
        exit()

    display(result)
