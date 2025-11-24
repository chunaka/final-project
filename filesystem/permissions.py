class Permissions:
    """
    Unix-style permissions (rwx for owner/group/others)
    """
    
    READ = 4
    WRITE = 2
    EXECUTE = 1
    
    def __init__(self, owner: int, group: int, others: int) -> None:
        self.owner = owner & 7
        self.group = group & 7
        self.others = others & 7
    
    @classmethod
    def from_octal(cls, octal_str: str):
        """
        Create permissions from octal string (e.g., "644", "755")
        """
        if len(octal_str) != 3:
            raise ValueError("Octal must be 3 digits (e.g., '644')")
        
        owner = int(octal_str[0])
        group = int(octal_str[1])
        others = int(octal_str[2])
        
        return cls(owner, group, others)
    
    def to_octal(self) -> str:
        """
        Convert permissions to octal notation
        """
        return f"{self.owner}{self.group}{self.others}"
    
    def to_string(self) -> str:
        """
        Convert permissions to string notation (rwx)
        """
        def perms_to_str(perm: int) -> str:
            r = 'r' if perm & self.READ else '-'
            w = 'w' if perm & self.WRITE else '-'
            x = 'x' if perm & self.EXECUTE else '-'
            return r + w + x
        
        return perms_to_str(self.owner) + perms_to_str(self.group) + perms_to_str(self.others)
    
    def can_read(self, user, owner, owner_groups: list[str]) -> bool:
        """
        Check if user can read
        """
        if user.is_root():
            return True
        
        if user.username == owner.username:
            return bool(self.owner & self.READ)
        
        for group in owner_groups:
            if user.in_group(group):
                return bool(self.group & self.READ)
        
        return bool(self.others & self.READ)
    
    def can_write(self, user, owner, owner_groups: list[str]) -> bool:
        """
        Check if user can write
        """
        if user.is_root():
            return True
        
        if user.username == owner.username:
            return bool(self.owner & self.WRITE)
        
        for group in owner_groups:
            if user.in_group(group):
                return bool(self.group & self.WRITE)
        
        return bool(self.others & self.WRITE)
    
    def can_execute(self, user, owner, owner_groups: list[str]) -> bool:
        """
        Check if user can execute
        """
        if user.is_root():
            return True
        
        if user.username == owner.username:
            return bool(self.owner & self.EXECUTE)
        
        for group in owner_groups:
            if user.in_group(group):
                return bool(self.group & self.EXECUTE)
        
        return bool(self.others & self.EXECUTE)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"Permissions('{self.to_octal()}')"
