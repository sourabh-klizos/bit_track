
from pathlib import Path
import sys
import hashlib
import zlib
from bit_track.bit_ignore import BitIgnore
from bit_track.bit_track_repository import BitTrackRepository
from bit_track.staging import BitTrackStaging
from bit_track.utils.file_handler import FileHandler

from datetime import datetime






class ObjectManager:
    objects_dir = BitTrackRepository.objects_dir
    main_file = BitTrackRepository.main_file

    commit_message = ""



    @staticmethod
    def hash_object(data, obj_type="blob"):
        """Generate SHA-1 hash for a given object."""
        header = f"{obj_type} {len(data)}".encode() + b"\0"
        store_data = header + data
        object_id = hashlib.sha1(store_data).hexdigest()
        # print(data)
        return object_id, zlib.compress(data)

    @staticmethod
    def write_object(data, obj_type="blob"):
        """Write an object (blob or tree) to the objects directory."""
        bit_track_dir = Path.cwd() / ".bit_track"

        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None

        object_id, compressed_data = ObjectManager.hash_object(data, obj_type)
        objects_dir = ObjectManager.objects_dir
        obj_dir = objects_dir / object_id[:2]
        obj_dir.mkdir(parents=True, exist_ok=True)
        obj_file = obj_dir / object_id[2:]

        

        if not obj_file.exists():# not exists in dir 
            # #check in index

            # print("obj_file not exists ",obj_file)

            # index_path = BitTrackRepository.index_file
            # content = FileHandler.read_file(index_path)
            
            

            # # content = FileHandler.read_file(index_path)
            # # # print("=======================================================")
            # print(content)
            # # # print("=======================================================")

            # if obj_type == "tree":
            #     with obj_file.open("wb") as f:
            #         f.write(compressed_data)
            #         return  object_id
                
            # # if not content:
            # #     print("Nothing to commit ")
            # #     return
                 

            # if  object_id in content:
            #     with obj_file.open("wb") as f:
            #         f.write(compressed_data)
            #     return  object_id

            with obj_file.open("wb") as f:
                f.write(compressed_data)
        return object_id
        # return None


    @staticmethod
    def set_commit_message(message:str) -> None:
        # print(message, "args  ==========================================")
        ObjectManager.commit_message = message


        # print(ObjectManager.commit_message, " cls val------------------------------------------------")
        return


    @staticmethod
    def create_blob(file_path: str) -> str:
        """Create a blob object for a file and store it."""
        try:
            
            # index_path = BitTrackRepository.index_file
            # content = FileHandler.read_file(index_path)

            file_path = Path(file_path)
            if not file_path.is_file():
                raise FileNotFoundError(f"Error: {file_path} is not a valid file.")

            with file_path.open("rb") as file:
                content = file.read()

            object_id = ObjectManager.write_object(content, "blob")
            # sys.stdout.write(f"Blob created: {file_path} -> {object_id}\n")
            return object_id
        except Exception as e:
            sys.stderr.write(f"Error creating blob: {e}\n")
            return None

    @staticmethod
    def create_tree(directory: str ) -> str:
        """Recursively create a tree object for a directory."""



        directory = Path(directory)
        entries = []

        bit_track_dir = directory / ".bit_track"
        # if not bit_track_dir.exists():
        #     sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
        #     return None


        index_path = BitTrackRepository.index_file
        content = FileHandler.read_file(index_path)

        if not content:
            sys.stdout.write("Nothing to commit please add first \n")
            return None



        ignore_patterns = BitIgnore.load_ignored_patterns()

        for path in sorted(directory.iterdir()):
        # for path in sorted(Path.cwd().rglob("*")):
        # for path in Path.cwd().rglob("*"):

            
            if ".bit_track" in path.parts:
                continue
            if BitIgnore.is_ignored(path, ignore_patterns):
                # print(f"Ignoring: {file_path}")
                continue



            # if ".bit_track" in path.parts:
            #     continue
            # if BitIgnore.is_ignored(path, ignore_patterns):
            #     continue


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

        # sys.stdout.write(f"Tree created: {directory} -> {tree_object_id}\n")


        # print(entries)

        # for item in entries:
        #     print(item.decode())



        # ObjectManager.store_snapshot_and_commit(tree_object_id,commit_message)


        # BitTrackStaging.clear_staging_only_from_index()

        return tree_object_id


  
    

    @staticmethod
    def read_object(object_id: str) -> bytes:
        """Read an object (blob, tree, or commit) from the objects directory and return its content."""
        bit_track_dir = Path.cwd() / ".bit_track"
        
        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None

        objects_dir = ObjectManager.objects_dir
        obj_dir = objects_dir / object_id[:2]
        obj_file = obj_dir / object_id[2:]

        if not obj_file.exists():
            sys.stderr.write(f"Error: Object {object_id} not found.\n")
            return None

        with obj_file.open("rb") as f:
            compressed_data = f.read()

        decompressed_data = zlib.decompress(compressed_data)
        return decompressed_data.decode()



    @staticmethod
    def get_latest_commit() -> str:
        """Retrieve the latest commit hash from HEAD (if any), decompressing it."""
        head_file = ObjectManager.main_file

        if head_file.exists():
            try:
                with head_file.open("r") as file: 
                    commit_hash_parent = file.read().strip()

                return commit_hash_parent if commit_hash_parent else None

            except Exception as e:
                sys.stderr.write(f"Error reading HEAD: {e}\n")
                return None
        return None
    

    # @staticmethod
    # def store_snapshot_and_commit(tree_hash: str, commit_message: str) -> str:
    #     """Creates and stores a commit object, updating HEAD in a compressed format."""

    #     head_file = BitTrackRepository.main_file
    #     parent_commit = ObjectManager.get_latest_commit()

    #     print(parent_commit, " ===============================")

    #     name, email = BitTrackRepository.get_user_config()

    #     commit_data = f"tree {tree_hash}\n"
    #     if parent_commit:
    #         commit_data += f"parent {parent_commit}\n"

    #     if name and email:
    #         commit_data += f"author {name} <{email}>\n"

    #     commit_data += f"time {datetime.now()} \n"
    #     commit_data += f"message {commit_message}\n"


        
    #     commit_bytes = commit_data.encode()
    #     compressed_commit = zlib.compress(commit_bytes)

   
    #     commit_hash = ObjectManager.hash_object(compressed_commit)[0]

    #     commit_file = ObjectManager.objects_dir / commit_hash[:2] / commit_hash[2:]

    #     commit_file.parent.mkdir(parents=True, exist_ok=True)

    #     try:
    #         with commit_file.open("wb") as file:
    #             file.write(compressed_commit)

    #         compressed_head = zlib.compress(commit_hash.encode())

    #         with head_file.open("w") as file:
    #             file.write(commit_hash)

    #         print(f"Commit {commit_hash} stored successfully.")
    #         return commit_hash

    #     except Exception as e:
    #         sys.stderr.write(f"Error writing commit: {e}\n")
    #         return None



    @staticmethod
    def store_snapshot_and_commit(tree_hash: str, commit_message: str) -> str:
        """Creates and stores a commit object, updating HEAD in a compressed format."""
        head_file = BitTrackRepository.main_file
        parent_commit = ObjectManager.get_latest_commit()

        print(f"DEBUG: Latest commit found: {type(parent_commit) }  : {parent_commit}")  # Debugging

        name, email = BitTrackRepository.get_user_config()

        commit_data = f"tree {tree_hash}\n"
        
        # Ensure the parent commit is only added if valid
        # if parent_commit and parent_commit.strip():
        #     commit_data += f"parent {parent_commit}\n"

        if parent_commit != None:
            commit_data += f"parent {parent_commit}\n"

        # if parent_commit != "None":
        #     commit_data += f"parent string None {parent_commit}\n"
            
            
        # if not parent_commit:
        #     print("Not Parent " *5)
            



        if name and email:
            commit_data += f"author {name} <{email}>\n"

        commit_data += f"time {datetime.now()} \n"
        commit_data += f"message {commit_message}\n"

        # Debug: Print final commit data before storing
        # print("final commit data before writing:\n", commit_data)

        commit_bytes = commit_data.encode()
        compressed_commit = zlib.compress(commit_bytes)

        commit_hash = ObjectManager.hash_object(compressed_commit)[0]
        commit_file = ObjectManager.objects_dir / commit_hash[:2] / commit_hash[2:]

        commit_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with commit_file.open("wb") as file:
                file.write(compressed_commit)

            compressed_head = zlib.compress(commit_hash.encode())

            with head_file.open("w") as file:
                file.write(commit_hash)

            print(f"Commit {commit_hash} stored successfully.")
            return commit_hash

        except Exception as e:
            sys.stderr.write(f"Error writing commit: {e}\n")
            return None