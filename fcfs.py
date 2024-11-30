import matplotlib.pyplot as plt
import random
from tabulate import tabulate

class Process:
    """
    This class when instantiated will provide attributes for a defined process which include (process id, arrival time,
    burst time, start time, completion time, waiting time, response time and turnaround time)
     - pid: Process ID.
     - arrival_time: Time at which the process arrives.
     - burst_time: CPU time required by the process.
     - waiting_time: Time spent waiting before execution.
     - turnaround_time: Total time from arrival to completion.
     - start_time: Time when the process begins execution.
     - response_time: Time from arrival to the start of execution.
     - completion_time: Time at which the process finishes execution.

    """
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_time = 0
        self.response_time = 0
        self.completion_time = 0

# Declaring global variables used to store processes and results
processes = []
fcfs_results = []

def predefined_test_cases():
    """
    Provides an interface for selecting and running predefined test cases for FCFS scheduling, as documented in the
    project paper.

    This function presents a menu of predefined test cases, each representing different scheduling scenarios,
    intended to represent real-world example cases with a best case, good case, average case, bad case, and worst case.
    Upon selecting a test case, the function will:

    - Clears the current global `processes` and `fcfs_results` lists.
    - Populates `processes` with predefined arrival and burst times for the selected case.
    - Run the FCFS scheduling algorithm using `calculate_fcfs`.
    - Displays the results in tabular format.
    - Generate a Gantt chart and histograms for the results.

    Test Cases:
        1. Best Case: Processes arrive with well-spaced arrival times and low burst times, minimizing waiting time.
        2. Good Case: Arrival times are moderately spaced with varying burst times, resulting in small waiting times.
        3. Average Case: Mix of arrival and burst times, leading to moderate waiting and turnaround times.
        4. Bad Case: Long processes arriving first delay shorter ones, increasing waiting times (convoy effect).
        5. Worst Case: A single long process at the start causes significant delays for subsequent short processes.

    Option 6 allows returning to the main menu without running a test case.

    Global Variables:
        processes (list): Updated with the predefined processes for the selected test case.
        fcfs_results (list): Updated with the results of the FCFS scheduling algorithm for the selected test case.

    :param: None
    :return: None
    """
    global processes, fcfs_results
    test_cases = {
        "1": ("Best Case", [0, 1, 3, 6, 10, 12, 15, 18, 22, 25], [2, 1, 3, 2, 4, 2, 3, 2, 3, 2]),
        "2": ("Good Case", [0, 2, 4, 6, 8, 10, 12, 14, 16, 18], [2, 1, 4, 3, 2, 1, 5, 2, 3, 1]),
        "3": ("Average Case", [0, 1, 3, 5, 7, 9, 10, 12, 14, 16], [5, 3, 4, 2, 6, 4, 3, 5, 2, 4]),
        "4": ("Bad Case", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [15, 1, 2, 1, 2, 3, 2, 1, 1, 2]),
        "5": ("Worst Case", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [20, 1, 2, 1, 2, 3, 2, 1, 1, 2])
    }

    print("\n--- Predefined Test Cases ---")
    for key, (name, _, _) in test_cases.items():
        print(f"{key}. {name}")
    print("6. Back to Main Menu")

    choice = input("Select a test case: ")

    if choice in test_cases:
        name, arrival_times, burst_times = test_cases[choice]
        print(f"\nRunning {name}...")
        processes.clear()
        fcfs_results.clear()
        processes.extend([Process(i + 1, arrival_times[i], burst_times[i]) for i in range(len(arrival_times))])
        fcfs_results.extend(calculate_fcfs(processes))
        print("\nProcess Information:")
        print_process_info(fcfs_results)
        print("\nGantt Chart:")
        create_gantt_chart(fcfs_results)
        print("\nHistograms:")
        plot_histograms(fcfs_results)
    elif choice == "6":
        return
    else:
        print("Invalid choice. Please try again.")

def generate_processes(num_processes):
    """
    Generates a list of processes with random arrival and burst times.

    This function creates a specified number of processes, each process is assigned the following:
    - A unique process ID (starting from 1).
    - A random arrival time between 0 and 10.
    - A random burst time between 1 and 10.

    :param num_processes (int): The number of processes to generate.
    :return: list: A list of `Process` objects, each initialized with a unique ID, random arrival time, and random
    burst time.
    """

    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, 10)  # Random arrival time between 0 and 10
        burst_time = random.randint(1, 10)  # Random burst time between 1 and 10
        processes.append(Process(i + 1, arrival_time, burst_time))
    return processes


def run_simulations(num_simulations, min_p, max_p):
    """
    Runs multiple simulations of the FCFS scheduling algorithm with randomly generated processes.

    This function performs the following steps:
    1. Determines the number of processes for each simulation, randomly chosen between `min_p` and `max_p`.
    2. Generates random processes for each simulation using the `generate_processes` function.
    3. Creates a deep copy of the generated processes to simulate the FCFS scheduling algorithm.
    4. Calculates average waiting and turnaround times for the FCFS algorithm.
    5. Collects the results of all simulations for analysis.

    :param num_simulations: (int) The number of simulations to run.
    :param min_p: (int) The minimum number of processes in each simulation.
    :param max_p: (int) The maximum number of processes in each simulation.
    :return: tuple:
                - fcfs_results (list of tuple): A list containing the average waiting time and
                  turnaround time for each simulation as `(avg_waiting_time, avg_turnaround_time)`.
                - fcfs_processes (list of list): A list of lists where each sublist contains `Process`
                  objects with calculated scheduling metrics for a single simulation.
    """

    fcfs_results = []
    num_processes = random.randint(min_p, max_p)

    fcfs_processes = []

    for _ in range(num_simulations):
        processes = generate_processes(num_processes)

        # Deep copy the process list to simulate separately for FCFS and SJF
        fcfs_process = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]

        # Run FCFS and collect average metrics
        fcfs_processes.append(calculate_fcfs(fcfs_process))
        fcfs_avg_waiting = sum(p.waiting_time for p in fcfs_process) / num_processes
        fcfs_avg_turnaround = sum(p.turnaround_time for p in fcfs_process) / num_processes
        fcfs_results.append((fcfs_avg_waiting, fcfs_avg_turnaround))

    return fcfs_results, fcfs_processes


def calculate_fcfs(processes):
    """
    Calculates scheduling metrics for a list of processes using the First-Come, First-Served (FCFS) algorithm.

    This function simulates the FCFS scheduling algorithm and computes the following metrics for each process:
    - Start time: The time when the process begins execution.
    - Response time: The time from the process arrival to the start of execution.
    - Waiting time: The time spent waiting in the queue before execution.
    - Completion time: The time when the process finishes execution.
    - Turnaround time: The total time from arrival to completion.

    The processes are sorted by their arrival times before calculation, ensuring that they execute in the order
    of arrival.

    :param processes: (list of Process) A list of `Process` objects with initialized `arrival_time` and `burst_time`.
    :return: list of Process: The input list of processes with updated scheduling metrics.
    """

    n = len(processes)

    # Sort processes based on arrival time
    processes.sort(key=lambda x: x.arrival_time)

    # Initialize the start time for the first process
    current_time = processes[0].arrival_time

    # O(n) where n is the number of processes

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
    """
    Displays process scheduling metrics in a tabular format and calculates average metrics.

    This function outputs a table showing the following metrics for each process:
    - Process ID (PID)
    - Arrival Time
    - Burst Time
    - Waiting Time
    - Turnaround Time

    Additionally, it calculates and prints the average waiting time and average turnaround time for the given list of processes.

    :param processes (list of Process): A list of `Process` objects with calculated scheduling metrics.
    :return: None
    """
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    n = len(processes)

    # Prepare data for tabulate
    table_data = [
        [process.pid, process.arrival_time, process.burst_time, process.waiting_time, process.turnaround_time]
        for process in processes
    ]

    # Define column headers
    headers = ["PID", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))  # Call tabulate function correctly

    # Print average metrics
    print("\nAverage Waiting Time:", round(total_waiting_time / n, 2))
    print("Average Turnaround Time:", round(total_turnaround_time / n, 2))


def create_gantt_chart(processes):
    """
    Creates and displays a Gantt chart for the FCFS scheduling algorithm.

    This function generates a Gantt chart visualization which shows the execution timeline of processes in the
    simulation. Each process is represented as a horizontal bar which spans from its start time to its completion time
    (the total burst time for the process).
    y-axis = the process IDs
    x-axis = time.

    :param processes: (list of Process): A list of `Process` objects with calculated `start_time` and `burst_time`.
    :return: None
    """

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
    """
    Generates histograms for waiting time and turnaround time of processes.

    This function creates two  bar charts:
    1. A histogram showing the waiting time for each process.
    2. A histogram showing the turnaround time for each process.

    Each bar represents an individual process, identified by process ID, the height of the bar
    corresponds to the waiting time or turnaround time (depending on the chart).

    :param processes (list of Process): A list of `Process` objects with calculated `waiting_time` and `turnaround_time`.
    :return:
    """

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

def main():
    global processes, fcfs_results
    print("\n--- FCFS Scheduling Simulation ---")
    print("\nOptions 1-5 can be used to randomly generate a set of processes and output results step-by-step")
    print("Options 6 & 7 can be used to run all the steps at once either using pre-defined test cases as noted in")
    print("the project paper (6), or a set of randomly generated processes (7)")
    while True:
        print("\n1. Generate Processes")
        print("2. Run FCFS Simulation")
        print("3. View Process Details")
        print("4. Generate Gantt Chart")
        print("5. Plot Histograms")
        print("6. Run Predefined Test Cases")
        print("7. Run Full Simulations & Results in Batch")
        print("8. Clear Processes")
        print("9. Exit")
        print()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Generate processes
            num_processes = int(input("Enter the number of processes to generate: "))
            processes.clear()
            processes.extend(generate_processes(num_processes))
            print("\nProcesses generated successfully!")
            print_process_info(processes)

        elif choice == "2":
            # Run FCFS simulation
            if not processes:
                print("No processes available. Please generate processes first (Option 1).")
                continue
            fcfs_results.clear()
            fcfs_results.extend(calculate_fcfs(processes))
            print("\nFCFS Simulation completed successfully!")
            print_process_info(fcfs_results)

        elif choice == "3":
            # View process details
            if not fcfs_results:
                print("No simulation results available. Please run a simulation first (Option 2).")
                continue
            print("\nProcess Information:")
            print_process_info(fcfs_results)

        elif choice == "4":
            # Generate Gantt chart
            if not fcfs_results:
                print("No simulation results available. Please run a simulation first (Option 2).")
                continue
            print("\nGenerating Gantt Chart...")
            create_gantt_chart(fcfs_results)

        elif choice == "5":
            # Plot histograms
            if not fcfs_results:
                print("No simulation results available. Please run a simulation first (Option 2).")
                continue
            print("\nGenerating Histograms...")
            plot_histograms(fcfs_results)

        elif choice == "6":
            # Run predefined test cases
            predefined_test_cases()


        elif choice == "7":
            # Run batch simulations
            num_simulations = int(input("Enter the number of simulations to run: "))
            min_p = int(input("Enter the minimum number of processes per simulation: "))
            max_p = int(input("Enter the maximum number of processes per simulation: "))
            results, batch_processes = run_simulations(num_simulations, min_p, max_p)

            # Display results
            print("\nBatch Simulations Results:")
            for i, (avg_waiting, avg_turnaround) in enumerate(results, start=1):
                print(
                    f"Simulation {i}: Avg Waiting Time = {avg_waiting:.2f}, Avg Turnaround Time = {avg_turnaround:.2f}")
            # Display details for each simulation

            for i, processes in enumerate(batch_processes, start=1):
                print(f"\nDetails of Simulation {i}:")
                print_process_info(processes)
                print(f"\nGenerating Gantt Chart for Simulation {i}")
                create_gantt_chart(processes)
                print(f"\nGenerating Histograms for Simulation {i}")

                plot_histograms(processes)

        elif choice == "8":
            # Clear processes
            processes.clear()
            fcfs_results.clear()
            print("Processes and simulation results have been cleared.")

        elif choice == "9":
            # Exit the program
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()