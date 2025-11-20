from schedulers.scheduler_base import Scheduler

class SJFScheduler(Scheduler):
    """
    Shortest Job First (Non-preemptive)
    Runs processes in order of shortest burst time.
    When a process arrives, the scheduler picks the process with the shortest burst time.
    """

    def run(self):
        """
        Execute SJF on the list of processes
        """
        # Sort by arrival time first
        self.processes.sort(key=lambda p: p.arrival_time)

        current_time = 0
        remaining_processes = self.processes.copy()
        scheduled = []

        while remaining_processes:
            # Find all processes that have arrived by current_time
            available = [p for p in remaining_processes if p.arrival_time <= current_time]

            if not available:
                # No process available, jump to next arrival
                current_time = min(p.arrival_time for p in remaining_processes)
                available = [p for p in remaining_processes if p.arrival_time <= current_time]

            # Select process with shortest burst time
            process = min(available, key=lambda p: p.burst_time)

            start = max(current_time, process.arrival_time)
            end = start + process.burst_time

            self.timeline.append((process.pid, start, end))

            process.start_time = start
            process.completion_time = end

            current_time = end
            remaining_processes.remove(process)
            scheduled.append(process)
    
    def compute_metrics(self):
        """
        Compute waiting time, turnaround time and throughput
        """
        n = len(self.processes)

        waiting = sum(process.start_time - process.arrival_time for process in self.processes) / n
        turnaround = sum(process.completion_time - process.arrival_time for process in self.processes) / n

        total_time = max(process.completion_time for process in self.processes)
        throughput = n / total_time

        return {
            "avg_waiting": waiting,
            "avg_turnaround": turnaround,
            "throughput": throughput
        }
