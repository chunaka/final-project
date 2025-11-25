# OS Simulator v1.0

A comprehensive operating system simulator implementing process scheduling algorithms and a virtual file system with Unix-style permissions.

##  Features

### Process Scheduling (Modules 1 & 2)
- **FCFS** - First Come First Served scheduling
- **SJF** - Shortest Job First scheduling  
- **Round Robin** - Preemptive with configurable quantum
- **Context Switching** - Full process state management
- **Performance Metrics** - Turnaround, waiting, and response times
- **Gantt Chart** - Visual timeline representation

### File System (Module 3)
- **Unix Permissions** - Full rwx permission system (owner/group/others)
- **User Management** - Multiple users with UIDs and groups
- **Hierarchical Structure** - Tree-based directory organization
- **18+ Commands** - Linux-like CLI (ls, cd, chmod, chown, cat, echo, tree, etc.)
- **File Operations** - Create, read, write, delete files and directories
- **Configuration Files** - Load filesystem state from config files
- **Dual Interface** - Both CLI and GUI available

## 📁Project Structure

```
os-simulator/
├── models/
│   ├── process.py          # Process class with PCB
│   ├── pcb.py              # Process Control Block
│   └── process_manager.py  # Process lifecycle manager
├── schedulers/
│   ├── scheduler_base.py   # Base scheduler class
│   ├── fcfs.py             # FCFS implementation
│   ├── sjf.py              # SJF implementation
│   └── round_robin.py      # Round Robin implementation
├── filesystem/
│   ├── user.py             # User class with UID and groups
│   ├── permissions.py      # Unix-style permissions (rwx)
│   ├── node.py             # Node, File, and Directory classes
│   ├── file_system.py      # FileSystem orchestrator
│   ├── commands.py         # CLI with 18+ commands
│   └── loader.py           # Config file loader
├── ui/
│   ├── console.py          # Console UI for schedulers
│   └── filesystem_gui.py   # GUI for filesystem
├── tests/
│   ├── processes_example.txt    # Example process config
│   └── filesystem_example.txt   # Example filesystem config
└── main.py                 # Main entry point
```

##  Installation

**Prerequisites:** Python 3.10 or higher

### Setup

```bash
# Clone repository
git clone https://github.com/chunaka/final-project.git
cd os-simulator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run simulator
python main.py
```

##  Usage

### Main Menu

Run `python main.py` to access the main menu with two modules:
1. Process Scheduling
2. File System

### Process Scheduling Module

1. Select scheduling algorithm (FCFS, SJF, or Round Robin)
2. For Round Robin, specify quantum value
3. Load process configuration file (see format below)
4. Execute scheduler and view results
5. Analyze performance metrics

**Process File Format:**
```
# pid,arrival,burst,priority,user
1,0,5,0,alice
2,1,3,1,bob
3,2,8,0,root
```

**Metrics Provided:**
- Turnaround Time
- Waiting Time
- Response Time
- Context Switch Count

### File System Module

Choose initialization method:
- Load from configuration file
- Use demo structure

Select interface mode:
- **CLI** - Command-line with Linux-like commands
- **GUI** - Graphical interface with visual navigation

#### CLI Commands

| Command | Description |
|---------|-------------|
| `ls [-a] [-l] [path]` | List directory contents |
| `cd [path]` | Change directory |
| `pwd` | Print working directory |
| `mkdir <dir>` | Create directory |
| `touch <file>` | Create empty file |
| `rm [-r] <file>` | Remove file/directory |
| `cat <file>` | Display file content |
| `echo <text> > <file>` | Write to file |
| `echo <text> >> <file>` | Append to file |
| `chmod <perms> <file>` | Change permissions |
| `chown <user> <file>` | Change owner |
| `tree [-L<n>] [path]` | Display directory tree |
| `whoami` | Show current user |
| `su [user]` | Switch user |
| `adduser <user> <uid>` | Add user (root only) |
| `help` | Show all commands |
| `exit` | Exit filesystem |

#### GUI Interface

**Layout:**
- Left: Directory tree for navigation
- Center: File list with details (permissions, owner, size, date)
- Right: Properties and permission editor

**Operations:**
- Navigate by clicking directories
- Double-click files to edit content
- Use toolbar or right-click menus for actions
- Edit permissions with checkboxes (rwx for owner/group/others)
- Switch users via User menu

**Filesystem Config Format:**
```
# Comments start with #
user,username,uid,group1,group2,...
dir,/path/to/directory,perms,owner
file,/path/to/file.txt,perms,owner,content

# Example:
user,alice,1000,users,developers
dir,/home/alice,755,alice
file,/home/alice/readme.txt,644,alice,Welcome!
```

## Examples

### Process Scheduling

```bash
$ python main.py
# Select: 1 (Process Scheduling)
# Choose: FCFS
# Load: tests/processes_example.txt
# Execute and view metrics
```

### File System - CLI

```bash
$ python main.py
# Select: 2 (File System)
# Init: 2 (Demo)
# Interface: 1 (CLI)

root@os-sim:/# ls
etc  home  tmp

root@os-sim:/# cd home/alice

root@os-sim:/home/alice# ls -l
rw-r--r-- alice        36 readme.txt

root@os-sim:/home/alice# cat readme.txt
Welcome to Alice's home directory!

root@os-sim:/home/alice# touch myfile.txt
root@os-sim:/home/alice# echo "Hello World" > myfile.txt

root@os-sim:/home/alice# chmod 600 myfile.txt
root@os-sim:/home/alice# ls -l myfile.txt
rw------- alice        12 myfile.txt
```

### File System - GUI

```bash
$ python main.py
# Select: 2 (File System)
# Init: 2 (Demo)
# Interface: 2 (GUI)

# Interact visually:
# - Click directories in tree to navigate
# - Double-click files to edit
# - Select files and use "Permissions" button
# - Use toolbar for common operations
```

##  Development

### Architecture

**Process Scheduling:**
- `ProcessManager` centralizes all process lifecycle operations
- `context_switch()` handles state transitions
- Schedulers implement algorithms using ProcessManager API

**File System:**
- Abstract `Node` class for files and directories
- Permission checks enforced at operation level
- Tree structure with parent pointers
- Single backend for both CLI and GUI

### Code Style

- English docstrings with type hints
- Descriptive naming conventions
- Minimal comments (self-documenting code)

### Implementation Status

**Module 1 - Process Management:**
- Process class with PCB
- ProcessManager with context switching
- Process states (NEW, READY, RUNNING, TERMINATED)

**Module 2 - Scheduling Algorithms:**
- FCFS, SJF, Round Robin
- Performance metrics calculation
- Timeline visualization

**Module 3 - File System:**
- User management with UID/groups
- Unix-style permissions (rwx)
- Hierarchical directory structure
- 18+ Linux-like commands
- CLI and GUI interfaces
- Config file loader


## Authors

**Juan Camilo Castro Montoya** - [chunaka](https://github.com/chunaka)


## Acknowledgments

- Operating Systems course materials
- Unix/Linux documentation
- Process scheduling algorithm textbooks