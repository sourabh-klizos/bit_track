import hashlib
import zlib
import sys
import time
from pathlib import Path
from bit_track.objects import ObjectManager
from bit_track.bit_ignore import BitIgnore

from bit_track.staging import BitTrackStaging





class BitTrackAdd:

    resent_staged = list()

    @staticmethod
    def hash_object(data: bytes) -> str:
        return ObjectManager.hash_object(data)
    
    @staticmethod
    def write_object(data, file_name, obj_type="blob"):
        """Write an object (blob or tree) to the objects directory, avoiding duplicates."""


        bit_track_dir = Path.cwd() / ".bit_track"
        if not bit_track_dir.exists():
            sys.stderr.write("Error: .bit_track directory does not exist. Please run 'bit_track init' first.\n")
            return None

        object_id, compressed_data = BitTrackAdd.hash_object(data)
        objects_dir = bit_track_dir / "objects"
        obj_dir = objects_dir / object_id[:2]
        obj_file = obj_dir / object_id[2:]



        if obj_file.exists():
            return object_id 

        

        BitTrackStaging.update_index(file_name,object_id)

        BitTrackAdd.resent_staged.append(file_name)


        obj_dir.mkdir(parents=True, exist_ok=True)
        with obj_file.open("wb") as f:
            f.write(compressed_data)
        


        return object_id
    
    # existing func
    @staticmethod
    def create_blob(file_path: str) -> str:
        """Create a blob object for a file and store it."""
        try:
            file_path = Path(file_path)
            if not file_path.is_file():
                return

            with file_path.open("rb") as file:
                content = file.read()

            object_id = BitTrackAdd.write_object(content,file_path ,"blob")
            # sys.stdout.write(f"Blob created: {file_path} -> {object_id}\n")
            return object_id
        except Exception as e:
            sys.stderr.write(f"Error creating blob: {e}\n")
            return None


    
    @staticmethod
    def add_all_files():
        ignore_patterns = BitIgnore.load_ignored_patterns()
        tracked_files = []

        for file_path in sorted(Path.cwd().rglob("*")):
        # for file_path in sorted(Path.cwd().iterdir()):
            if ".bit_track" in file_path.parts:  # Always ignore the repo folder
                continue
            if BitIgnore.is_ignored(file_path, ignore_patterns):
                # print(f"Ignoring: {file_path}")
                continue

            BitTrackAdd.create_blob(file_path)
            tracked_files.append(file_path)

        # for recent_staged_file in BitTrackAdd.resent_staged:
        #     sys.stdout.write(f"{recent_staged_file}  \n")

        return tracked_files
    


    
