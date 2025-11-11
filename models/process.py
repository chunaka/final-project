from models.pcb import PCB, ProcessState

class Process:
    """
    High_level representation of a process that wraps its PCB.
    """

    def __init__(self, pid:int, burst_time:int, arrival_time:int=0, priority:int=0, user:str=None):
        self.pcb = PCB(pid, burst_time, arrival_time, priority)
        self.user = user
    
    
    def change_state(self, new_state:ProcessState, current_time:int=0) -> None:
        """
        Change the process state
        """

        self.pcb.state = new_state

        if new_state == ProcessState.RUNNING and self.pcb.start_time == -1 and current_time != 0:
            self.pcb.start_time = current_time
        
        if new_state == ProcessState.TERMINATED:
            self.pcb.completion_time = current_time
            self.update_times(current_time)
    
    
    def execute(self, time_units:int) -> None:
        """ 
        Simulate execution on CPU
        """

        self.pcb.remaining_time = max(0, self.pcb.remaining_time - time_units)
        self.pcb.program_counter += time_units

    def update_times(self, current_time:int) -> None:
        """
        Update waiting time, turnaround time, and response time.
        """

        pcb = self.pcb
        pcb.turnaround_time = current_time - pcb.arrival_time
        pcb.waiting_time = pcb.turnaround_time - pcb.arrival_time

        if pcb.response_time == -1 and pcb.start_time != -1:
            pcb.response_time = pcb.start_time - pcb.arrival_time

    def is_completed(self) -> bool:
        """
        Check if process has finished
        """

        return self.pcb.remaining_time <= 0 

    def __str__(self) -> str:
        pcb = self.pcb
        return (f"Process(PID={pcb.pid}, User={self.user}, "
                f"State={pcb.state.value}, Remaining={pcb.remaining_time}, "
                f"Priority={pcb.priority})")
