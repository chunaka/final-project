from schedulers.scheduler_base import Scheduler

class RoundRobinScheduler(Scheduler):
    """
    Round Robin (Preemptive)
    Runs processes in a circular queue with a fixed time quantum.
    Each process gets a time slice, and if not completed, goes back to the end of the queue.
    """

    def __init__(self, quantum=2):
        """
        Initialize Round Robin scheduler with a time quantum.
        
        Args:
            quantum (int): Time quantum for each process slice (default: 2)
        """
        super().__init__()
        self.quantum = quantum

    def run(self):
        """
        Execute Round Robin on the list of processes
        """
        # Sort by arrival time first
        self.processes.sort(key=lambda p: p.arrival_time)

        current_time = 0
        ready_queue = []
        remaining_burst = {p.pid: p.burst_time for p in self.processes}
        process_dict = {p.pid: p for p in self.processes}
        completed = set()
        process_index = 0
        
        # Track first start time for each process
        first_start = {}

        while len(completed) < len(self.processes):
            # Add newly arrived processes to ready queue
            while process_index < len(self.processes) and self.processes[process_index].arrival_time <= current_time:
                ready_queue.append(self.processes[process_index])
                process_index += 1

            if not ready_queue:
                # No process in queue, jump to next arrival
                if process_index < len(self.processes):
                    current_time = self.processes[process_index].arrival_time
                    continue
                else:
                    break

            # Get next process from queue
            process = ready_queue.pop(0)
            
            # Record first start time
            if process.pid not in first_start:
                first_start[process.pid] = current_time
                process.start_time = current_time

            # Execute for quantum or remaining burst time, whichever is smaller
            execution_time = min(self.quantum, remaining_burst[process.pid])
            start = current_time
            end = start + execution_time

            self.timeline.append((process.pid, start, end))

            current_time = end
            remaining_burst[process.pid] -= execution_time

            # Add newly arrived processes after this quantum
            while process_index < len(self.processes) and self.processes[process_index].arrival_time <= current_time:
                ready_queue.append(self.processes[process_index])
                process_index += 1

            # Check if process is completed
            if remaining_burst[process.pid] == 0:
                process.completion_time = current_time
                completed.add(process.pid)
            else:
                # Process not completed, add back to queue
                ready_queue.append(process)
    
    def compute_metrics(self):
        """
        Compute waiting time, turnaround time and throughput
        """
        n = len(self.processes)

        # Waiting time = start_time - arrival_time
        waiting = sum(process.start_time - process.arrival_time for process in self.processes) / n
        
        # Turnaround time = completion_time - arrival_time
        turnaround = sum(process.completion_time - process.arrival_time for process in self.processes) / n

        total_time = max(process.completion_time for process in self.processes)
        throughput = n / total_time

        return {
            "avg_waiting": waiting,
            "avg_turnaround": turnaround,
            "throughput": throughput
        }
