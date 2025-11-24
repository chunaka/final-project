class User:
    """
    System user with UID and groups
    """
    
    def __init__(self, username: str, uid: int, groups: list[str] = None) -> None:
        self.username = username
        self.uid = uid
        self.groups = groups if groups is not None else [username]
    
    def is_root(self) -> bool:
        """
        Check if user is root (uid = 0)
        """
        return self.uid == 0
    
    def in_group(self, group: str) -> bool:
        """
        Check if user belongs to a group
        """
        return group in self.groups
    
    def __str__(self) -> str:
        groups_str = ",".join(self.groups)
        return f"{self.username}(uid={self.uid}, groups={groups_str})"
    
    def __repr__(self) -> str:
        return f"User('{self.username}', {self.uid}, {self.groups})"
