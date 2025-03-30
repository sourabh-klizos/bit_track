
from pathlib import Path
import sys
import hashlib
import zlib
from bit_track.bit_ignore import BitIgnore
from bit_track.bit_track_repository import BitTrackRepository

from bit_track.utils.file_handler import FileHandler



class ObjectManager:
    @staticmethod
    def hash_object(data, obj_type="blob"):
        """Generate SHA-1 hash for a given object."""
        header = f"{obj_type} {len(data)}".encode() + b"\0"
        store_data = header + data
        object_id = hashlib.sha1(store_data).hexdigest()
        print(data)
        return object_id, zlib.compress(data)

    @staticmethod
    def write_object(data, obj_type="blob"):
        """Write an object (blob or tree) to the objects directory."""
        bit_track_dir = Path.cwd() / ".bit_track"
        # print("==================================",bit_track_dir)
        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None

        object_id, compressed_data = ObjectManager.hash_object(data, obj_type)
        objects_dir = bit_track_dir / "objects"
        obj_dir = objects_dir / object_id[:2]
        obj_dir.mkdir(parents=True, exist_ok=True)
        obj_file = obj_dir / object_id[2:]

        if not obj_file.exists():# not exists in dir 
            #check in index
            index_path = BitTrackRepository.index_file

            content = FileHandler.read_file(index_path)
            print(content,"=======================================================")
            print(content)
            print(content,"=======================================================")

            if obj_type == "tree":
                with obj_file.open("wb") as f:
                    f.write(compressed_data)
                    return  object_id
                 

            if not object_id in content:
                return

            with obj_file.open("wb") as f:
                f.write(compressed_data)
        return object_id

    @staticmethod
    def create_blob(file_path: str) -> str:
        """Create a blob object for a file and store it."""
        try:
            file_path = Path(file_path)
            if not file_path.is_file():
                raise FileNotFoundError(f"Error: {file_path} is not a valid file.")

            with file_path.open("rb") as file:
                content = file.read()

            object_id = ObjectManager.write_object(content, "blob")
            sys.stdout.write(f"Blob created: {file_path} -> {object_id}\n")
            return object_id
        except Exception as e:
            sys.stderr.write(f"Error creating blob: {e}\n")
            return None

    @staticmethod
    def create_tree(directory: str) -> str:
        """Recursively create a tree object for a directory."""
        directory = Path(directory)
        entries = []
        # print("dr -===================================",directory)

        bit_track_dir = directory / ".bit_track"
        # if not bit_track_dir.exists():
        #     sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
        #     return None

        ignore_patterns = BitIgnore.load_ignored_patterns()

        for path in sorted(directory.iterdir()):
            print(path.name)

            if ".bit_track" in path.parts:
                continue
            if BitIgnore.is_ignored(path, ignore_patterns):
                continue


            if path.is_file():
                object_id = ObjectManager.create_blob(str(path))
                if object_id:
                    entries.append(f"100644 blob {path.name} ".encode() + b"\0" + object_id.encode() + b"\n")

            elif path.is_dir():
                object_id = ObjectManager.create_tree(str(path))
                if object_id:
                    entries.append(f"40000  tree {path.name} ".encode() + b"\0" + object_id.encode() + b"\n")

        tree_data = b"".join(entries)
        tree_object_id = ObjectManager.write_object(tree_data, "tree")
        sys.stdout.write(f"Tree created: {directory} -> {tree_object_id}\n")
        return tree_object_id

    @staticmethod
    def ignores():
        """Read .bitignore file and return ignored patterns."""
        print(BitIgnore.list_tracked_files(), " =============================")
        return

        return BitIgnore.list_tracked_files()

        current_dir = Path.cwd()
        # print("ignore dir ==========" , current_dir)
        bit_ignore_file = current_dir / ".bitignore"

        ignores = set([".bit_track"])  # Always ignore .bit_track



        if bit_ignore_file.exists():
            with bit_ignore_file.open("r") as file:
                ignores.update(line.strip() for line in file if line.strip())

        # print("ignore dir ==========" , ignores)

        return ignores
    

    @staticmethod
    def read_object(object_id: str) -> bytes:
        """Read an object (blob, tree, or commit) from the objects directory and return its content."""
        bit_track_dir = Path.cwd() / ".bit_track"
        
        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None
        
        objects_dir = bit_track_dir / "objects"
        obj_dir = objects_dir / object_id[:2]
        obj_file = obj_dir / object_id[2:]

        if not obj_file.exists():
            sys.stderr.write(f"Error: Object {object_id} not found.\n")
            return None

        with obj_file.open("rb") as f:
            compressed_data = f.read()

        decompressed_data = zlib.decompress(compressed_data)
        # print(decompressed_data, "===========================")
        return decompressed_data.decode()

        try:
            header, content = decompressed_data.split(b"\0", 1)
            obj_type, size = header.split(b" ", 1)
            
            if obj_type == b"blob":
                return content
            else:
                sys.stderr.write(f"Error: Object {object_id} is not a blob (found {obj_type.decode()}).\n")
                return None
        except ValueError:
            sys.stderr.write(f"Error: Malformed object {object_id}.\n")
            return None

