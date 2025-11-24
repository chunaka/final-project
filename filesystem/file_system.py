from filesystem.user import User
from filesystem.permissions import Permissions
from filesystem.node import Node, File, Directory


class FileSystem:
    """
    Virtual filesystem with hierarchical tree, users and permissions
    """
    
    def __init__(self) -> None:
        root_user = User("root", 0, ["root", "wheel"])
        
        self.users: dict[str, User] = {
            "root": root_user
        }
        
        root_perms = Permissions.from_octal("755")
        self.root = Directory("/", root_user, root_perms, parent=None)
        
        self.current_dir = self.root
        self.current_user = root_user
    
    def add_user(self, username: str, uid: int, groups: list[str] = None) -> User:
        """
        Add a new user to the system
        """
        if username in self.users:
            raise ValueError(f"User '{username}' already exists")
        
        user = User(username, uid, groups if groups else [username])
        self.users[username] = user
        return user
    
    def switch_user(self, username: str) -> None:
        """
        Switch current user (similar to 'su')
        """
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist")
        
        self.current_user = self.users[username]
    
    def get_user(self, username: str) -> User:
        """Get user by name"""
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist")
        return self.users[username]
    
    def pwd(self) -> str:
        """
        Returns current working directory (Print Working Directory)
        """
        return self.current_dir.get_path()
    
    def cd(self, path: str) -> None:
        """
        Change current directory
        """
        target = self.resolve_path(path)
        
        if not isinstance(target, Directory):
            raise NotADirectoryError(f"Not a directory: '{path}'")
        
        self.current_dir = target
    
    def resolve_path(self, path: str) -> Node:
        """
        Resolve absolute or relative path to a node
        """
        if path.startswith("/"):
            current = self.root
            if path == "/":
                return current
            parts = path[1:].split("/")
        else:
            current = self.current_dir
            parts = path.split("/")
        
        for part in parts:
            if not part or part == ".":
                continue
            elif part == "..":
                if current.parent is not None:
                    current = current.parent
            else:
                if not isinstance(current, Directory):
                    raise NotADirectoryError(f"Not a directory in path: '{path}'")
                current = current.get_child(part)
        
        return current
    
    def touch(self, filename: str) -> None:
        """
        Create empty file or update timestamp if exists
        """
        try:
            node = self.current_dir.get_child(filename)
            if isinstance(node, File):
                node.touch()
            else:
                raise FileExistsError(f"'{filename}' is a directory")
        except FileNotFoundError:
            perms = Permissions.from_octal("644")
            new_file = File(filename, self.current_user, perms)
            self.current_dir.add_child(new_file)
    
    def mkdir(self, dirname: str) -> None:
        """
        Create a new directory
        """
        perms = Permissions.from_octal("755")
        new_dir = Directory(dirname, self.current_user, perms, parent=self.current_dir)
        self.current_dir.add_child(new_dir)
    
    def rm(self, name: str, recursive: bool = False) -> None:
        """
        Remove a file or directory
        """
        node = self.current_dir.get_child(name)
        
        if not self.current_dir.permissions.can_write(self.current_user, 
                                                       self.current_dir.owner,
                                                       self.current_dir.owner.groups):
            raise PermissionError(f"Permission denied: cannot delete '{name}'")
        
        if isinstance(node, Directory):
            if not recursive and len(node.children) > 0:
                raise IsADirectoryError(f"'{name}' is a directory (use -r to delete)")
        
        self.current_dir.remove_child(name)
    
    def cat(self, filename: str) -> str:
        """
        Read file content
        """
        node = self.current_dir.get_child(filename)
        
        if not isinstance(node, File):
            raise IsADirectoryError(f"'{filename}' is a directory")
        
        return node.read(self.current_user)
    
    def echo(self, filename: str, content: str, append: bool = False) -> None:
        """
        Write content to a file
        """
        try:
            node = self.current_dir.get_child(filename)
            
            if not isinstance(node, File):
                raise IsADirectoryError(f"'{filename}' is a directory")
            
            if append:
                node.append(self.current_user, content)
            else:
                node.write(self.current_user, content)
        except FileNotFoundError:
            self.touch(filename)
            node = self.current_dir.get_child(filename)
            node.write(self.current_user, content)
    
    def chmod(self, name: str, perms: str) -> None:
        """
        Change file/directory permissions
        """
        node = self.current_dir.get_child(name)
        
        if not (self.current_user.is_root() or 
                self.current_user.username == node.owner.username):
            raise PermissionError(f"Permission denied: cannot chmod '{name}'")
        
        node.permissions = Permissions.from_octal(perms)
        node.touch()
    
    def chown(self, name: str, new_owner_name: str) -> None:
        """
        Change file/directory owner
        """
        if not self.current_user.is_root():
            raise PermissionError("Only root can change ownership")
        
        node = self.current_dir.get_child(name)
        new_owner = self.get_user(new_owner_name)
        
        node.owner = new_owner
        node.touch()
    
    def ls(self, path: str = ".", show_hidden: bool = False, long_format: bool = False) -> list:
        """
        List directory contents
        """
        if path == ".":
            target_dir = self.current_dir
        else:
            node = self.resolve_path(path)
            if not isinstance(node, Directory):
                raise NotADirectoryError(f"Not a directory: '{path}'")
            target_dir = node
        
        children = target_dir.list_children(show_hidden)
        
        if long_format:
            return [str(child) for child in children]
        else:
            return [child.name for child in children]
    
    def tree(self, start_path: str = ".", depth: int = None, _current_depth: int = 0, _prefix: str = "") -> str:
        """
        Generate directory tree visualization
        """
        if depth is not None and _current_depth >= depth:
            return ""
        
        if _current_depth == 0:
            node = self.resolve_path(start_path) if start_path != "." else self.current_dir
        else:
            node = start_path
        
        if not isinstance(node, Directory):
            return f"{_prefix}{node.name}\n"
        
        result = f"{_prefix}{node.name}/\n" if _current_depth > 0 else f"{node.get_path()}\n"
        
        children = node.list_children(show_hidden=False)
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            connector = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "
            
            if isinstance(child, Directory):
                result += f"{_prefix}{connector}{child.name}/\n"
                result += self.tree(child, depth, _current_depth + 1, _prefix + extension)
            else:
                result += f"{_prefix}{connector}{child.name}\n"
        
        return result
    
    def find(self, name: str, start_dir: Directory = None) -> list[str]:
        """
        Search for files/directories by name
        """
        if start_dir is None:
            start_dir = self.current_dir
        
        results = []
        
        for child in start_dir.children.values():
            if child.name == name:
                results.append(child.get_path() if isinstance(child, Directory) else 
                             start_dir.get_path() + "/" + child.name)
            
            if isinstance(child, Directory):
                results.extend(self.find(name, child))
        
        return results
