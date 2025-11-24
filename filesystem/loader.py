from filesystem.file_system import FileSystem
from filesystem.permissions import Permissions


def load_filesystem_from_file(filepath: str) -> FileSystem:
    """
    Load a filesystem from a configuration file
    
    Format (CSV):
        user,username,uid,group1,group2,...
        dir,/path/to/directory,perms,owner
        file,/path/to/file.txt,perms,owner,file content
    """
    fs = FileSystem()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                parts = [p.strip() for p in line.split(',')]
                
                if len(parts) < 2:
                    print(f"[WARN] Line {line_num}: Invalid format, skipping")
                    continue
                
                entry_type = parts[0].lower()
                
                try:
                    if entry_type == 'user':
                        if len(parts) < 3:
                            print(f"[WARN] Line {line_num}: User needs username,uid")
                            continue
                        
                        username = parts[1]
                        uid = int(parts[2])
                        groups = parts[3:] if len(parts) > 3 else [username]
                        
                        if username != "root":
                            fs.add_user(username, uid, groups)
                            print(f"[OK] Created user: {username} (uid={uid})")
                    
                    elif entry_type == 'dir':
                        if len(parts) < 4:
                            print(f"[WARN] Line {line_num}: Dir needs path,perms,owner")
                            continue
                        
                        path = parts[1]
                        perms = parts[2]
                        owner = parts[3]
                        
                        _create_directory(fs, path, perms, owner)
                        print(f"[OK] Created directory: {path}")
                    
                    elif entry_type == 'file':
                        if len(parts) < 4:
                            print(f"[WARN] Line {line_num}: File needs path,perms,owner")
                            continue
                        
                        path = parts[1]
                        perms = parts[2]
                        owner = parts[3]
                        content = parts[4] if len(parts) > 4 else ""
                        
                        _create_file(fs, path, perms, owner, content)
                        print(f"[OK] Created file: {path}")
                    
                    else:
                        print(f"[WARN] Line {line_num}: Unknown type '{entry_type}'")
                
                except Exception as e:
                    print(f"[ERROR] Line {line_num}: {e}")
                    continue
    
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        raise
    except Exception as e:
        print(f"[ERROR] Failed to load filesystem: {e}")
        raise
    
    fs.cd("/")
    return fs


def _create_directory(fs: FileSystem, path: str, perms: str, owner_name: str) -> None:
    """
    Create a directory at specified path
    """
    if path == "/":
        return
    
    parts = path.strip('/').split('/')
    parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
    dir_name = parts[-1]
    
    current = fs.pwd()
    fs.cd(parent_path)
    
    try:
        fs.mkdir(dir_name)
    except FileExistsError:
        pass
    
    fs.chmod(dir_name, perms)
    if owner_name != "root":
        fs.chown(dir_name, owner_name)
    
    fs.cd(current)


def _create_file(fs: FileSystem, path: str, perms: str, owner_name: str, content: str) -> None:
    """
    Create a file at specified path
    """
    parts = path.strip('/').split('/')
    parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
    file_name = parts[-1]
    
    current = fs.pwd()
    fs.cd(parent_path)
    
    fs.touch(file_name)
    if content:
        fs.echo(file_name, content + "\n")
    
    fs.chmod(file_name, perms)
    if owner_name != "root":
        fs.chown(file_name, owner_name)
    
    fs.cd(current)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        fs = load_filesystem_from_file(sys.argv[1])
        print("\n" + "="*60)
        print(" FILESYSTEM LOADED ".center(60, "="))
        print("="*60)
        print()
        print(fs.tree())
    else:
        print("Usage: python loader.py <config_file>")
