from datetime import datetime
from abc import ABC, abstractmethod
from filesystem.user import User
from filesystem.permissions import Permissions


class Node(ABC):
    """
    Abstract base class for filesystem nodes (files and directories)
    """
    
    def __init__(self, name: str, owner: User, permissions: Permissions) -> None:
        self.name = name
        self.owner = owner
        self.permissions = permissions
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    @abstractmethod
    def is_directory(self) -> bool:
        """Returns True if node is a directory"""
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        """Returns node size in bytes"""
        pass
    
    def touch(self) -> None:
        """Update modification timestamp"""
        self.modified_at = datetime.now()
    
    def __str__(self) -> str:
        perms = str(self.permissions)
        owner = self.owner.username
        size = self.get_size()
        return f"{perms} {owner:8} {size:6} {self.name}"


class File(Node):
    """
    File with text content
    """
    
    def __init__(self, name: str, owner: User, permissions: Permissions, content: str = "") -> None:
        super().__init__(name, owner, permissions)
        self._content = content
    
    def is_directory(self) -> bool:
        return False
    
    def get_size(self) -> int:
        """Returns content size in bytes"""
        return len(self._content)
    
    def read(self, user: User) -> str:
        """
        Read file content
        """
        if not self.permissions.can_read(user, self.owner, self.owner.groups):
            raise PermissionError(f"Permission denied: {user.username} cannot read {self.name}")
        
        return self._content
    
    def write(self, user: User, content: str) -> None:
        """
        Overwrite file content
        """
        if not self.permissions.can_write(user, self.owner, self.owner.groups):
            raise PermissionError(f"Permission denied: {user.username} cannot write to {self.name}")
        
        self._content = content
        self.touch()
    
    def append(self, user: User, content: str) -> None:
        """
        Append content to file
        """
        if not self.permissions.can_write(user, self.owner, self.owner.groups):
            raise PermissionError(f"Permission denied: {user.username} cannot write to {self.name}")
        
        self._content += content
        self.touch()


class Directory(Node):
    """
    Directory that can contain other nodes
    """
    
    def __init__(self, name: str, owner: User, permissions: Permissions, parent=None) -> None:
        super().__init__(name, owner, permissions)
        self.children: dict[str, Node] = {}
        self.parent: Directory | None = parent
    
    def is_directory(self) -> bool:
        return True
    
    def get_size(self) -> int:
        """Returns number of children"""
        return len(self.children)
    
    def add_child(self, node: Node) -> None:
        """
        Add a child node to directory
        """
        if node.name in self.children:
            raise FileExistsError(f"File or directory '{node.name}' already exists")
        
        self.children[node.name] = node
        
        if isinstance(node, Directory):
            node.parent = self
        
        self.touch()
    
    def remove_child(self, name: str) -> None:
        """
        Remove a child node from directory
        """
        if name not in self.children:
            raise FileNotFoundError(f"No such file or directory: '{name}'")
        
        del self.children[name]
        self.touch()
    
    def get_child(self, name: str) -> Node:
        """
        Get a child node by name
        """
        if name not in self.children:
            raise FileNotFoundError(f"No such file or directory: '{name}'")
        
        return self.children[name]
    
    def has_child(self, name: str) -> bool:
        """Check if child with given name exists"""
        return name in self.children
    
    def list_children(self, show_hidden: bool = False) -> list[Node]:
        """
        List all children in directory
        """
        children = list(self.children.values())
        
        if not show_hidden:
            children = [c for c in children if not c.name.startswith('.')]
        
        return sorted(children, key=lambda x: (not x.is_directory(), x.name))
    
    def get_path(self) -> str:
        """
        Get full path of directory
        """
        if self.parent is None:
            return "/"
        
        path_parts = []
        current = self
        
        while current.parent is not None:
            path_parts.append(current.name)
            current = current.parent
        
        if not path_parts:
            return "/"
        
        return "/" + "/".join(reversed(path_parts))
