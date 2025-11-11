from collections import deque
from models.process import Process
from models.pcb import ProcessState

class ProcessManager:
    """
    The ProcessManager class simulates the operating system's process managements unit.
    It is responsible for creating, scheduling and tracking processes throughout their lifecycle.
    """
    
    def __init__(self):
        self.ready_queue = deque()
        self.blocked_queue = deque()
        self.terminated_list = []
        self.current_process = None
    
    def create_process(self, pid:int, burst_time:int, arrival_time:int=0, priority:int=0, user:str="system") -> Process:
        """
        Creates a new process, initializes its PCB and appends it to the READY queue.
        """
        
        process = Process(pid, burst_time, arrival_time, priority, user)
        process.change_state(ProcessState.READY)
        self.ready_queue.append(process)
        return process
    
    def get_current_process(self) -> Process | None:
        """
        Returns the actual process in CPU
        """
        return self.current_process

    def context_switch(self):
        """
        Perform a context switch between processes.
        """

        if self.current_process:
            if self.current_process.pcb.state != ProcessState.TERMINATED:
                self.current_process.change_state(ProcessState.READY)
                self.ready_queue.append(self.current_process)
        
        if self.ready_queue:
            self.current_process = self.ready_queue.popleft()
            self.current_process.change_state(ProcessState.RUNNING)
        else:
            self.current_process = None

    def terminate_current_process(self, current_time:int):
        """
        Finishes the actual process and append it to terminated_list
        """

        if self.current_process:
            self.current_process.change_state(ProcessState.TERMINATED, current_time)
            self.terminated_list.append(self.current_process)
            self.current_process = None
    
    def block_current_process(self):
        """
        Blocks the actual process
        """
        if self.current_process:
            self.current_process.change_state(ProcessState.BLOCKED)
            self.blocked_queue.append(self.current_process)
            self.current_process = None

    def unblock_process(self, process:Process):
        """
        Moves a blocked process to READY again
        """

        if process in self.blocked_queue:
            self.blocked_queue.remove(process)
            process.change_state(ProcessState.READY)
            self.ready_queue.append(process)