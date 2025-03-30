


import sys
from pathlib import Path
import zlib





class BitTrackStaging:
    """Handles staging operations for BitTrack."""
    
    BIT_TRACK_DIR = Path.cwd() / ".bit_track"
    INDEX_FILE = BIT_TRACK_DIR / "index"
    OBJECTS_DIR = BIT_TRACK_DIR / "objects"

    @staticmethod
    def check_repo():
        """Ensure the .bit_track repository exists."""
        if not BitTrackStaging.BIT_TRACK_DIR.exists():
            sys.stderr.write("Error: Repository not initialized. Run `bit_init` first.\n")
            sys.exit(1)



    # @staticmethod
    # def update_index(file_name: str, object_id: str):
    #     """Update the index file with the filename and its object hash."""
    #     BitTrackStaging.check_repo()
    #     index_file = BitTrackStaging.INDEX_FILE
    #     index_entries = {}

    #     # Read existing index
    #     if index_file.exists():
    #         with index_file.open("r") as f:
    #             for line in f:
    #                 mode, obj_id, path = line.strip().split(" ", 2)
    #                 index_entries[path] = (mode, obj_id)

    #     # Update index with new file
    #     index_entries[file_name] = ("100644", object_id)

    #     # Write back to index
    #     with index_file.open("w") as f:
    #         for path, (mode, obj_id) in index_entries.items():
    #             f.write(f"{mode} {obj_id} {path}\n")
        
    #     print(f"File '{file_name}' staged successfully.")



    @staticmethod
    def update_index(file_name: str, object_id: str):
        """Update the index file with the filename and its object hash."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE
        index_entries = {}

        # Read existing index
        if index_file.exists():
            with index_file.open("rb") as f:  # Read in binary mode
                compressed_data = f.read()
                if compressed_data:
                    try:
                        decompressed_data = zlib.decompress(compressed_data).decode()
                        for line in decompressed_data.splitlines():
                            mode, obj_id, path = line.strip().split(" ", 2)
                            index_entries[path] = (mode, obj_id)
                    except zlib.error:
                        sys.stdout.write("Error: Corrupted index file.\n")
                        return

        # Update index with new file
        index_entries[file_name] = ("100644", object_id)

        # Prepare compressed data
        index_content = "\n".join(f"{mode} {obj_id} {path}" for path, (mode, obj_id) in index_entries.items())
        compressed_content = zlib.compress(index_content.encode())

        # Write back compressed index
        with index_file.open("wb") as f:  # Write in binary mode
            f.write(compressed_content)

        # sys.stdout.write(f"File '{file_name}' staged successfully.\n")



    # @staticmethod
    # def update_index(file_path: str, object_id: str):
    #     """Update the index file with the full relative path and object hash."""
    #     BitTrackStaging.check_repo()
    #     index_file = BitTrackStaging.INDEX_FILE
    #     index_entries = {}

    #     # Normalize path (store relative path from repo root)
    #     repo_root = BitTrackStaging.BIT_TRACK_DIR.parent
    #     relative_path = str(Path(file_path).relative_to(repo_root))

    #     # Read existing index
    #     if index_file.exists():
    #         with index_file.open("rb") as f:  # Read in binary mode
    #             compressed_data = f.read()
    #             if compressed_data:
    #                 try:
    #                     decompressed_data = zlib.decompress(compressed_data).decode()
    #                     for line in decompressed_data.splitlines():
    #                         mode, obj_id, path = line.strip().split(" ", 2)
    #                         index_entries[path] = (mode, obj_id)  # Key is now full relative path
    #                 except zlib.error:
    #                     sys.stdout.write("Error: Corrupted index file.\n")
    #                     return

    #     # Update index with new file (store full relative path)
    #     index_entries[relative_path] = ("100644", object_id)

    #     # Prepare compressed data
    #     index_content = "\n".join(f"{mode} {obj_id} {path}" for path, (mode, obj_id) in index_entries.items())
    #     compressed_content = zlib.compress(index_content.encode())

    #     # Write back compressed index
    #     with index_file.open("wb") as f:  # Write in binary mode
    #         f.write(compressed_content)

    #     sys.stdout.write(f"File '{relative_path}' staged successfully.\n")






    # @staticmethod
    # def show_staging():
    #     """Show all staged files."""
    #     BitTrackStaging.check_repo()
    #     index_file = BitTrackStaging.INDEX_FILE

    #     if not index_file.exists() or index_file.stat().st_size == 0:
    #         print("No files staged.")
    #         return

    #     print("Staged files:")
    #     with index_file.open("r") as f:
    #         for line in f:
    #             mode, obj_id, path = line.strip().split(" ", 2)
    #             print(f"{path} -> {obj_id}")

    @staticmethod
    def show_staging():
        """Display the staged files from the index."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE

        if not index_file.exists():
            sys.stdout.write("No files staged.\n")
            return

        # Read and decompress the index file
        with index_file.open("rb") as f:
            compressed_data = f.read()
            if not compressed_data:
                sys.stdout.write("No files staged.\n")
                return

            try:
                decompressed_data = zlib.decompress(compressed_data).decode()
            except zlib.error:
                sys.stdout.write("Error: Corrupted index file.\n")
                return

        # Display the staged files
        sys.stdout.write("Staged files:\n")
        for line in decompressed_data.splitlines():
            mode, obj_id, path = line.strip().split(" ", 2)
            sys.stdout.write(f"  {mode} {obj_id} {path}\n")


    # @staticmethod
    # def clear_staging():
    #     """Clear all staged files without deleting the index file, and remove corresponding objects."""
    #     BitTrackStaging.check_repo()
    #     index_file = BitTrackStaging.INDEX_FILE
    #     objects_dir = BitTrackStaging.OBJECTS_DIR

    #     if not index_file.exists() or index_file.stat().st_size == 0:
    #         print("No files staged.")
    #         return
        
    #     # Read all object IDs from index and remove them from objects directory
    #     with index_file.open("r") as f:
    #         for line in f:
    #             _, obj_id, _ = line.strip().split(" ", 2)
    #             obj_path = objects_dir / obj_id
    #             if obj_path.exists():
    #                 obj_path.unlink()  # Delete the object file
        
    #     # Clear index file content
    #     with index_file.open("w") as f:
    #         pass  # Writing nothing clears the file
        
    #     print("Staging area cleared, and corresponding objects deleted.")



    # @staticmethod
    # def clear_staging():
    #     """Clear all staged files without deleting the index file, and remove corresponding objects."""
    #     BitTrackStaging.check_repo()
    #     index_file = BitTrackStaging.INDEX_FILE
    #     root_dir = BitTrackStaging.BIT_TRACK_DIR
    #     objects_dir = root_dir / BitTrackStaging.OBJECTS_DIR

    #     if not index_file.exists() or index_file.stat().st_size == 0:
    #         sys.stdout.write("No files staged.\n")
    #         return

    #     # Read and decompress the index file
    #     try:
    #         with index_file.open("rb") as f:
    #             compressed_data = f.read()
    #             if not compressed_data:
    #                 sys.stdout.write("No files staged.\n")
    #                 return

    #             decompressed_data = zlib.decompress(compressed_data).decode()
    #     except zlib.error:
    #         sys.stdout.write("Error: Corrupted index file.\n")
    #         return

    #     # Remove corresponding object files
    #     for line in decompressed_data.splitlines():
    #         _, obj_id, _ = line.strip().split(" ", 2)
    #         obj_path = objects_dir / obj_id
    #         if obj_path.exists():
    #             obj_path.unlink()  # Delete the object file

    #     # Clear index by writing empty compressed content
    #     with index_file.open("wb") as f:
    #         f.write(zlib.compress(b""))  # Empty compressed file

    #     sys.stdout.write("Staging area cleared, and corresponding objects deleted.\n")





    @staticmethod
    def clear_staging():
        """Clear all staged files without deleting the index file, and remove corresponding objects."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE
        objects_dir = BitTrackStaging.OBJECTS_DIR  

        if not index_file.exists() or index_file.stat().st_size == 0:
            sys.stdout.write("No files staged.\n")
            return

        # Read and decompress the index file
        try:
            with index_file.open("rb") as f:
                compressed_data = f.read()
                if not compressed_data:
                    sys.stdout.write("No files staged.\n")
                    return

                decompressed_data = zlib.decompress(compressed_data).decode()
        except zlib.error:
            sys.stdout.write("Error: Corrupted index file.\n")
            return


        # Remove corresponding object files
        for line in decompressed_data.splitlines():
            parts = line.strip().split(" ", 2)
            if len(parts) != 3:
                print(f"Skipping malformed line: {line}")  # Debugging
                continue

            _, obj_id, file_name = parts

            if len(obj_id) < 3:
                print(f"Invalid object ID: {obj_id}")  # Debugging
                continue

            obj_subdir = obj_id[:2]  
            obj_filename = obj_id[2:] 

            obj_path = objects_dir / obj_subdir / obj_filename 

            

            if obj_path.exists():
                try:
                    obj_path.unlink()
                    sys.stdout.write(f"Unstaged : {file_name} \n")

                    obj_subdir_path = objects_dir / obj_subdir
                    if obj_subdir_path.exists() and not any(obj_subdir_path.iterdir()):
                        obj_subdir_path.rmdir()
                except Exception as e:
                    print(f"Error deleting {obj_path}: {e}")


        with index_file.open("wb") as f:
            f.write(zlib.compress(b""))

        sys.stdout.write("Staging area cleared, and corresponding objects deleted.\n")


