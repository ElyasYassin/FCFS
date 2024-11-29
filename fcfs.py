import matplotlib.pyplot as plt
import pandas as pd
import random
from tabulate import tabulate
import time


# This class when instantiated will provide attributes for a defined process which include (process id, arrival time, burst time, start time, completion time, waiting time, response time and turnaround time)

# The process
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
        arrival_time = random.randint(0, 10)  # We'll generate an arrival time between 0 and 10
        burst_time = random.randint(1, 10)    # We'll generate a burst time between 1 and 10
        processes.append(Process(i + 1, arrival_time, burst_time)) # Instantiate the process and append it to the list with it's arrival time and burst time
    return processes

def get_arrival_time(process):
    return process.arrival_time


# The simulation process was inspired by the paper: https://irepos.unijos.edu.ng/jspui/bitstream/123456789/3136/1/V8I5201935.pdf

#  We generate a n simulations and m processes (between min_p and max_p)



def run_simulations(num_simulations, min_p, max_p):
    fcfs_results = [] 
    cpu_utilizations = []  

    fcfs_processes = []
    

    for _ in range(num_simulations):
        num_processes = random.randint(min_p, max_p)  
    
        processes = generate_processes(num_processes)
        
        # We'll instantiate the processes with their properties (read above) and store them in fcfs_process
        fcfs_process = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]

        # Perform the first come first serve scheduling
        fcfs_processes.append(calculate_fcfs(fcfs_process))
        
        # Calculate average waiting and turnaround times for each simulation
        fcfs_avg_waiting = sum(p.waiting_time for p in fcfs_process) / num_processes
        fcfs_avg_turnaround = sum(p.turnaround_time for p in fcfs_process) / num_processes
        fcfs_results.append((fcfs_avg_waiting, fcfs_avg_turnaround))

    return fcfs_results, fcfs_processes, cpu_utilizations

"""
Check for these Edge Cases to handle:
    - Multiple processes arriving at the same time
    - Idle CPU time 
    - Empty list of processes

Also test for varying numbers of processes, arrival and burst times

Optimize the efficiency of fcfs code 
 
"""

def calculate_fcfs(processes):
    n = len(processes)
    
    # We'll sort the processes based on the arrival times
    processes.sort(key=get_arrival_time)
    
    current_time = processes[0].arrival_time
    
    # O(n) where n is the number of processes
    
    for i in range(n):
        process = processes[i]
        
        # Here we calculate the necessary metrics intuitively based on our chapter's information
        process.start_time = max(current_time, process.arrival_time)
        process.response_time = process.start_time - process.arrival_time 
        process.waiting_time = process.start_time - process.arrival_time
        process.completion_time = process.start_time + process.burst_time   
        process.turnaround_time = process.completion_time - process.arrival_time  
        current_time = process.completion_time

    return processes


def print_process_info(processes):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    n = len(processes)

    # We'll create a table of the times associate with each process using the tabulate module for proper visualization
    
    table_data = [
        [process.pid, process.arrival_time, process.burst_time, process.waiting_time, process.turnaround_time]
        for process in processes
    ]
    
    headers = ["PID", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid")) 
    
    print("\nAverage Waiting Time:", round(total_waiting_time / n, 2))
    print("Average Turnaround Time:", round(total_turnaround_time / n, 2))

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

    fig, axes = plt.subplots(1, 2, figsize=(12, 6)) 

    axes[0].bar(pids, turnaround_times, color='green')
    axes[0].set_xlabel('Process ID')
    axes[0].set_ylabel('Turnaround Time')
    axes[0].set_title('Turnaround Time per Process')

    axes[1].bar(pids, waiting_times, color='orange')
    axes[1].set_xlabel('Process ID')
    axes[1].set_ylabel('Waiting Time')
    axes[1].set_title('Waiting Time per Process')

    plt.tight_layout()
    plt.show()