import hashlib
import zlib
import sys
import time
from pathlib import Path
from bit_track.objects import ObjectManager
from bit_track.bit_ignore import BitIgnore






class GitAdd:
    @staticmethod
    def hash_object(data: bytes) -> str:
        """Generate SHA-1 hash for a given object."""
        header = f"{"blob"} {len(data)}".encode() + b"\0"
        store_data = header + data
        object_id = hashlib.sha1(store_data).hexdigest()
        return object_id, zlib.compress(data)
    
    @staticmethod
    def write_object(data, file_name, obj_type="blob"):
        """Write an object (blob or tree) to the objects directory, avoiding duplicates."""

        print("file name")
        bit_track_dir = Path.cwd() / ".bit_track"
        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None

        object_id, compressed_data = GitAdd.hash_object(data)
        objects_dir = bit_track_dir / "objects"
        obj_dir = objects_dir / object_id[:2]
        obj_file = obj_dir / object_id[2:]

        if obj_file.exists():
            return object_id
        

        GitAdd.update_index(file_name,object_id)


        obj_dir.mkdir(parents=True, exist_ok=True)
        with obj_file.open("wb") as f:
            f.write(compressed_data)
        


        return object_id
    

    @staticmethod
    def create_blob(file_path: str) -> str:
        """Create a blob object for a file and store it."""
        try:
            file_path = Path(file_path)
            if not file_path.is_file():
                # raise FileNotFoundError(f"Error: {file_path} is not a valid file.")
                return

            with file_path.open("rb") as file:
                content = file.read()

            object_id = GitAdd.write_object(content,file_path.name ,"blob")
            sys.stdout.write(f"Blob created: {file_path} -> {object_id}\n")
            return object_id
        except Exception as e:
            sys.stderr.write(f"Error creating blob: {e}\n")
            return None
        
    
    @staticmethod
    def add_all_files():
        ignore_patterns = BitIgnore.load_ignored_patterns()
        tracked_files = []

        for file_path in Path.cwd().rglob("*"):
            if ".bit_track" in file_path.parts:  # Always ignore the repo folder
                continue
            if BitIgnore.is_ignored(file_path, ignore_patterns):
                # print(f"Ignoring: {file_path}")
                continue

            GitAdd.create_blob(file_path)
            tracked_files.append(file_path)

        return tracked_files
    


    @staticmethod
    def update_index(file_name: str, object_id: str):
        """Update the index file with the filename and its object hash."""
        index_file = Path.cwd() / ".bit_track" / "index"
        index_entries = {}
        
        if index_file.exists():
            with index_file.open("r") as f:
                for line in f:
                    mode, obj_id, path = line.strip().split(" ", 2)
                    index_entries[path] = (mode, obj_id)
        
        index_entries[file_name] = ("100644", object_id)
        
        with index_file.open("w") as f:
            for path, (mode, obj_id) in index_entries.items():
                f.write(f"{mode} {obj_id} {path}\n")
    
