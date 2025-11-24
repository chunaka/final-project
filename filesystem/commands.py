from filesystem.file_system import FileSystem


class FileSystemCLI:
    """
    Command-line interface for the file system
    Simulates Linux/Unix-like commands
    """
    
    def __init__(self, filesystem: FileSystem) -> None:
        self.fs = filesystem
        self.running = True
    
    def get_prompt(self) -> str:
        """Generate the terminal prompt"""
        user = self.fs.current_user.username
        pwd = self.fs.pwd()
        if pwd.startswith(f"/home/{user}"):
            pwd = "~" + pwd[len(f"/home/{user}"):]
        
        symbol = "#" if self.fs.current_user.is_root() else "$"
        return f"{user}@os-sim:{pwd}{symbol} "
    
    def cmd_ls(self, args: list[str]) -> None:
        """List files and directories"""
        show_hidden = "-a" in args
        long_format = "-l" in args
        
        paths = [arg for arg in args if not arg.startswith("-")]
        path = paths[0] if paths else "."
        
        try:
            items = self.fs.ls(path, show_hidden, long_format)
            for item in items:
                print(item)
        except Exception as e:
            print(f"ls: {e}")
    
    def cmd_cd(self, args: list[str]) -> None:
        """Change the current directory"""
        if not args:
            home = f"/home/{self.fs.current_user.username}"
            try:
                self.fs.cd(home)
            except:
                self.fs.cd("/")
        else:
            try:
                self.fs.cd(args[0])
            except Exception as e:
                print(f"cd: {e}")
    
    def cmd_pwd(self, args: list[str]) -> None:
        """Print working directory"""
        print(self.fs.pwd())
    
    def cmd_mkdir(self, args: list[str]) -> None:
        """Create a directory"""
        if not args:
            print("mkdir: missing operand")
            return
        
        for dirname in args:
            try:
                self.fs.mkdir(dirname)
            except Exception as e:
                print(f"mkdir: {e}")
    
    def cmd_touch(self, args: list[str]) -> None:
        """Create an empty file"""
        if not args:
            print("touch: missing file operand")
            return
        
        for filename in args:
            try:
                self.fs.touch(filename)
            except Exception as e:
                print(f"touch: {e}")
    
    def cmd_rm(self, args: list[str]) -> None:
        """Remove files or directories"""
        if not args:
            print("rm: missing operand")
            return
        
        recursive = "-r" in args or "-rf" in args
        names = [arg for arg in args if not arg.startswith("-")]
        
        for name in names:
            try:
                self.fs.rm(name, recursive=recursive)
            except Exception as e:
                print(f"rm: {e}")
    
    def cmd_cat(self, args: list[str]) -> None:
        """Display file content"""
        if not args:
            print("cat: missing file operand")
            return
        
        for filename in args:
            try:
                content = self.fs.cat(filename)
                print(content)
            except Exception as e:
                print(f"cat: {e}")
    
    def cmd_echo(self, args: list[str]) -> None:
        """Write text to a file"""
        if len(args) < 3:
            print("Usage: echo <text> > <file>")
            print("       echo <text> >> <file>")
            return
        
        if ">" in args:
            idx = args.index(">")
            append = False
        elif ">>" in args:
            idx = args.index(">>")
            append = True
        else:
            print(" ".join(args))
            return
        
        text = " ".join(args[:idx])
        filename = args[idx + 1] if idx + 1 < len(args) else None
        
        if not filename:
            print("echo: missing filename")
            return
        
        try:
            self.fs.echo(filename, text + "\n", append=append)
        except Exception as e:
            print(f"echo: {e}")
    
    def cmd_chmod(self, args: list[str]) -> None:
        """Change file permissions"""
        if len(args) < 2:
            print("Usage: chmod <perms> <file>")
            return
        
        perms = args[0]
        filename = args[1]
        
        try:
            self.fs.chmod(filename, perms)
        except Exception as e:
            print(f"chmod: {e}")
    
    def cmd_chown(self, args: list[str]) -> None:
        """Change file owner"""
        if len(args) < 2:
            print("Usage: chown <user> <file>")
            return
        
        new_owner = args[0]
        filename = args[1]
        
        try:
            self.fs.chown(filename, new_owner)
        except Exception as e:
            print(f"chown: {e}")
    
    def cmd_tree(self, args: list[str]) -> None:
        """Show directory tree"""
        depth = None
        path = "."
        
        for arg in args:
            if arg.startswith("-L"):
                try:
                    depth = int(arg[2:])
                except:
                    print(f"tree: invalid depth '{arg[2:]}'")
                    return
            elif not arg.startswith("-"):
                path = arg
        
        try:
            tree_output = self.fs.tree(path, depth)
            print(tree_output, end="")
        except Exception as e:
            print(f"tree: {e}")
    
    def cmd_whoami(self, args: list[str]) -> None:
        """Show current user"""
        print(self.fs.current_user.username)
    
    def cmd_su(self, args: list[str]) -> None:
        """Switch user"""
        if not args:
            username = "root"
        else:
            username = args[0]
        
        try:
            self.fs.switch_user(username)
            print(f"Switched to user '{username}'")
        except Exception as e:
            print(f"su: {e}")
    
    def cmd_adduser(self, args: list[str]) -> None:
        """Add a new user"""
        if not self.fs.current_user.is_root():
            print("adduser: only root can add users")
            return
        
        if len(args) < 2:
            print("Usage: adduser <username> <uid> [groups...]")
            return
        
        username = args[0]
        try:
            uid = int(args[1])
        except ValueError:
            print(f"adduser: invalid uid '{args[1]}'")
            return
        
        groups = args[2:] if len(args) > 2 else [username]
        
        try:
            self.fs.add_user(username, uid, groups)
            print(f"User '{username}' added successfully")
        except Exception as e:
            print(f"adduser: {e}")
    
    def cmd_clear(self, args: list[str]) -> None:
        """Clear the screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cmd_help(self, args: list[str]) -> None:
        """Show help for commands"""
        print("Available commands:")
        print()
        print("  Navigation:")
        print("    ls [-a] [-l] [path]    List directory contents")
        print("    cd [path]              Change directory")
        print("    pwd                    Print working directory")
        print()
        print("  File Operations:")
        print("    touch <file>           Create empty file")
        print("    mkdir <dir>            Create directory")
        print("    rm [-r] <file>         Remove file/directory")
        print("    cat <file>             Display file content")
        print("    echo <text> > <file>   Write to file")
        print("    echo <text> >> <file>  Append to file")
        print()
        print("  Permissions:")
        print("    chmod <perms> <file>   Change permissions (e.g., chmod 644 file)")
        print("    chown <user> <file>    Change owner")
        print()
        print("  Utilities:")
        print("    tree [-L<n>] [path]    Display directory tree")
        print("    whoami                 Show current user")
        print("    su [user]              Switch user")
        print("    adduser <user> <uid>   Add new user (root only)")
        print()
        print("  System:")
        print("    clear                  Clear screen")
        print("    help                   Show this help")
        print("    exit                   Exit file system")
        print()
    
    def cmd_exit(self, args: list[str]) -> None:
        """Exit the file system"""
        self.running = False
        print("Exiting file system...")
    
    def parse_command(self, line: str) -> tuple[str, list[str]]:
        """
        Parse a command line
        
        Returns:
            (command, args)
        """
        parts = line.strip().split()
        if not parts:
            return ("", [])
        
        cmd = parts[0]
        args = parts[1:]
        
        return (cmd, args)
    
    def execute(self, cmd: str, args: list[str]) -> None:
        """
        Execute a command
        """
        commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "pwd": self.cmd_pwd,
            "mkdir": self.cmd_mkdir,
            "touch": self.cmd_touch,
            "rm": self.cmd_rm,
            "cat": self.cmd_cat,
            "echo": self.cmd_echo,
            "chmod": self.cmd_chmod,
            "chown": self.cmd_chown,
            "tree": self.cmd_tree,
            "whoami": self.cmd_whoami,
            "su": self.cmd_su,
            "adduser": self.cmd_adduser,
            "clear": self.cmd_clear,
            "help": self.cmd_help,
            "exit": self.cmd_exit,
        }
        
        if cmd in commands:
            commands[cmd](args)
        else:
            print(f"{cmd}: command not found")
    
    def run(self) -> None:
        """
        Run the CLI REPL loop
        """
        print("=" * 60)
        print(" OS SIMULATOR - FILE SYSTEM ".center(60, "="))
        print("=" * 60)
        print()
        print("Type 'help' for available commands")
        print()
        
        while self.running:
            try:
                line = input(self.get_prompt())
                cmd, args = self.parse_command(line)
                
                if cmd:
                    self.execute(cmd, args)
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


def create_demo_filesystem() -> FileSystem:
    """
    Create a demo filesystem with users and basic structure
    """
    fs = FileSystem()
    
    fs.add_user("alice", 1000, ["users", "developers"])
    fs.add_user("bob", 1001, ["users"])
    
    fs.mkdir("home")
    fs.mkdir("tmp")
    fs.mkdir("etc")
    
    fs.cd("home")
    fs.mkdir("alice")
    fs.mkdir("bob")
    
    fs.chown("alice", "alice")
    fs.chown("bob", "bob")
    
    fs.cd("alice")
    fs.touch("readme.txt")
    fs.echo("readme.txt", "Welcome to Alice's home directory!\n")
    fs.chmod("readme.txt", "644")
    
    fs.cd("/")
    
    return fs


if __name__ == "__main__":
    fs = create_demo_filesystem()
    cli = FileSystemCLI(fs)
    cli.run()
