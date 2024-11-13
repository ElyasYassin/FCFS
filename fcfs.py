import matplotlib.pyplot as plt
import pandas as pd

# This class when instantiated will provide attributes for a defined process which include (process id, arrival time, burst time, waiting time and turnaround time)

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid               
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0        
        self.turnaround_time = 0     
        
def calculate_fcfs(processes):
    n = len(processes)
    
    # Sort processes based on arrival time
    processes.sort(key=lambda x: x.arrival_time)
    
    # Calculate waiting time for the first process
    processes[0].waiting_time = 0
    
    # Calculate waiting time for the remaining processes
    for i in range(1, n):
        # Waiting time of current process = burst time of previous process + waiting time of previous process
        processes[i].waiting_time = processes[i - 1].burst_time + processes[i - 1].waiting_time
    
    # Calculate turnaround time for each process
    for process in processes:
        process.turnaround_time = process.burst_time + process.waiting_time

    return processes

def print_process_info(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    n = len(processes)

    print("PID\tArrival\tBurst\tWaiting\tTurnaround")
    for process in processes:
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.waiting_time}\t{process.turnaround_time}")
    
    print("\nAverage Waiting Time:", total_waiting_time / n)
    print("Average Turnaround Time:", total_turnaround_time / n)

def get_processes_from_user():
    processes = []
    num_processes = int(input("Enter the number of processes: "))
    
    for i in range(num_processes):
        pid = int(input(f"\nEnter Process ID for process {i+1}: "))
        arrival_time = int(input(f"Enter Arrival Time for process {pid}: "))
        burst_time = int(input(f"Enter Burst Time for process {pid}: "))
        processes.append(Process(pid, arrival_time, burst_time))
    
    return processes

def create_gantt_chart(processes):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_yticks([10 * (i + 1) for i in range(len(processes))])
    gnt.set_yticklabels([f'P{process.pid}' for process in processes])
    gnt.grid(True)
    
    for i, process in enumerate(processes):
        gnt.broken_barh([(process.start_time, process.burst_time)], (10 * (i + 1) - 5, 9), facecolors=('tab:blue'))

    plt.title("Gantt Chart for FCFS Scheduling")
    plt.show()
    
def plot_histograms(processes):
    pids = [process.pid for process in processes]
    waiting_times = [process.waiting_time for process in processes]
    turnaround_times = [process.turnaround_time for process in processes]

    # Waiting Time Histogram
    plt.figure()
    plt.bar(pids, waiting_times, color='tab:orange')
    plt.xlabel('Process ID')
    plt.ylabel('Waiting Time')
    plt.title('Waiting Time per Process')
    plt.show()

    # Turnaround Time Histogram
    plt.figure()
    plt.bar(pids, turnaround_times, color='tab:green')
    plt.xlabel('Process ID')
    plt.ylabel('Turnaround Time')
    plt.title('Turnaround Time per Process')
    plt.show()