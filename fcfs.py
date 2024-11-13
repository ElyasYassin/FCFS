import matplotlib.pyplot as plt
import pandas as pd
import random

# This class when instantiated will provide attributes for a defined process which include (process id, arrival time, burst time, start time, completion time, waiting time, response time and turnaround time)

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid               
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0        
        self.turnaround_time = 0  
        self.start_time = 0   
        self.response_time = 0
        self.completion_time = 0
        
def generate_processes(num_processes):
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, 10)  # Random arrival time between 0 and 10
        burst_time = random.randint(1, 10)    # Random burst time between 1 and 10
        processes.append(Process(i + 1, arrival_time, burst_time))
    return processes

        
def calculate_fcfs(processes):
    n = len(processes)
    
    # Sort processes based on arrival time
    processes.sort(key=lambda x: x.arrival_time)
    
    # Initialize the start time for the first process
    current_time = processes[0].arrival_time
    
    for i in range(n):
        process = processes[i]
        
        # Process start time is the current time if the process has arrived
        process.start_time = max(current_time, process.arrival_time)
        
        # Response time is the time from arrival to start
        process.response_time = process.start_time - process.arrival_time
        
        # Waiting time is the time from arrival to the time it actually starts
        process.waiting_time = process.start_time - process.arrival_time
        
        # Completion time is start time + burst time
        process.completion_time = process.start_time + process.burst_time
        
        # Turnaround time is the time from arrival to completion
        process.turnaround_time = process.completion_time - process.arrival_time
        
        # Update current time for the next process
        current_time = process.completion_time

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