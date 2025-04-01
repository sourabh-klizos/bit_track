from pathlib import Path
from bit_track.objects import ObjectManager

import colorama
from colorama import Fore, Style
import sys
from bit_track.bit_track_repository import BitTrackRepository


# class Revert:
    
#     object_dir = BitTrackRepository.objects_dir


#     @staticmethod
#     def revert_to_old_tree(commit_hash: str) -> None:

#         content = ObjectManager.read_object(commit_hash)
#         # print(content, " commit content")
#         tree_hash = content.splitlines()[0].split()[1]

#         commit_exists = ObjectManager.read_object(tree_hash)

#         if commit_exists == None:
#             return "Provide A Valid Commit Hash"
        

#         Revert.make_changes_in_dir(tree_hash)
        

#         return tree_hash  


#     @staticmethod
#     def make_changes_in_dir(tree_hash):
#         tree_content = ObjectManager.read_object(tree_hash)

#         if not tree_content:
#             return "Yo have Deleted the BitTrack  Blobs"
        
#         for item in tree_content.splitlines():
#             # print(item, " =================")
#             permission , obj_type , path , hash = item.split()

#             if obj_type == "blob":
#                 pass
#                 # create a function to write in path actual content

#                 Revert.write_file(path, hash)

#             print(obj_type)
            


#     @staticmethod
#     def write_file(path, blob_hash):

#         current_working_dir = Path.cwd()

#         file_path = current_working_dir / path

#         print(file_path)




# class Revert:
    
#     object_dir = BitTrackRepository.objects_dir

#     @staticmethod
#     def revert_to_old_tree(commit_hash: str):
#         """Revert repository to an older tree state based on a commit hash."""
#         content = ObjectManager.read_object(commit_hash)
#         if not content:
#             return "Provide a valid commit hash"
        
#         tree_hash = content.splitlines()[0].split()[1]

#         print(tree_hash, " ----------------------tree hash snapsort")

#         commit_exists = ObjectManager.read_object(tree_hash)
#         if commit_exists is None:
#             return "Provide a valid commit hash"
        
#         Revert.make_changes_in_dir(tree_hash)
#         return tree_hash  

#     @staticmethod
#     def make_changes_in_dir(tree_hash):
#         """Apply the changes from the given tree hash to the working directory."""
#         tree_content = ObjectManager.read_object(tree_hash)

#         print("tree_content", tree_content)
#         if not tree_content:
#             return "You have deleted the BitTrack blobs"
        
#         for item in tree_content.splitlines():
#             permission, obj_type, path, obj_hash = item.split()

#             if obj_type == "blob":
#                 Revert.write_file(path, obj_hash)

#             if obj_type == "tree":
#                 Revert.make_changes_in_dir(obj_hash)


            
#             print(f"Processing {obj_type}: {path}")

#     @staticmethod
#     def write_file(path, blob_hash):
#         """Writes file content from a blob object to the filesystem."""
#         file_path = Path.cwd() / path
#         file_content = ObjectManager.read_object(blob_hash)

#         print(file_content)

#         if file_content is None:
#             print(f"Warning: Blob {blob_hash} for {path} not found.")
#             return
        
#         file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

#         with open(file_path, "w") as file:
#             file.write(file_content)
#         print(f"Restored: {file_path}")

import zlib

# class Revert:
#     object_dir = BitTrackRepository.objects_dir

#     @staticmethod
#     def revert_to_old_tree(commit_hash: str):
#         """Revert repository to an older tree state based on a commit hash."""
#         content = ObjectManager.read_object(commit_hash)
#         if not content:
#             sys.stderr.write("Error: Provide a valid commit hash.\n")
#             return None
        
#         tree_hash = content.splitlines()[0].split()[1]
#         commit_exists = ObjectManager.read_object(tree_hash)
        
#         if not commit_exists:
#             sys.stderr.write("Error: Provide a valid commit hash.\n")
#             return None
        
#         Revert.make_changes_in_dir(tree_hash)
#         return tree_hash  

#     @staticmethod
#     def make_changes_in_dir(tree_hash):
#         """Apply the changes from the given tree hash to the working directory."""
#         tree_content = ObjectManager.read_object(tree_hash)
        
#         if not tree_content:
#             sys.stderr.write("Error: You have deleted the BitTrack blobs.\n")
#             return
        
#         for item in tree_content.splitlines():
#             parts = item.split()
#             if len(parts) != 4:
#                 continue  # Skip invalid entries

#             permission, obj_type, path, obj_hash = parts

#             if len(obj_hash) == 41:
#                 obj_hash = obj_hash[1:]
          
            
#             print(f"Processing {obj_type}: {path} ({obj_hash})")
            
#             if obj_type == "blob":
#                 print(path, "------------>")
#                 Revert.write_file(path, obj_hash.strip())
#             elif obj_type == "tree":

#                 # print("tree path------------------>", path)
#                 # dir_path = Path.cwd() / path
#                 # dir_path.mkdir(parents=True, exist_ok=True)
#                 print(len(obj_hash))
#                 Revert.make_changes_in_dir(obj_hash)

#     @staticmethod
#     def write_file(path, blob_hash):
#         """Writes file content from a blob object to the filesystem."""
#         file_path = Path.cwd() / path
        
#         print(f"Attempting to restore file: {file_path} from blob {blob_hash}")
        
#         file_content = ObjectManager.read_object(blob_hash)
        
#         if file_content is None:
#             sys.stderr.write(f"Warning: Blob {blob_hash} for {path} not found.\n")
#             return
        
#         file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
#         with open(file_path, "w") as file:
#             file.write(file_content)
#         print(f"Restored: {file_path}")
























class Revert:
    object_dir = BitTrackRepository.objects_dir  # Assuming the objects dir is set correctly

    @staticmethod
    def revert_to_old_tree(commit_hash: str):
        """Revert repository to an older tree state based on a commit hash."""
        content = ObjectManager.read_object(commit_hash)
        if not content:
            sys.stderr.write("Error: Provide a valid commit hash.\n")
            return None
        
        tree_hash = content.splitlines()[0].split()[1]
        commit_exists = ObjectManager.read_object(tree_hash)
        
        if not commit_exists:
            sys.stderr.write("Error: Provide a valid commit hash.\n")
            return None
        
        Revert.make_changes_in_dir(tree_hash, "")
        return tree_hash  

    @staticmethod
    def make_changes_in_dir(tree_hash, parent_dir):
        """Apply the changes from the given tree hash to the working directory."""
        tree_content = ObjectManager.read_object(tree_hash)
        
        if not tree_content:
            sys.stderr.write("Error: You have deleted the BitTrack blobs.\n")
            return
        
        for item in tree_content.splitlines():
            parts = item.split()
            if len(parts) != 4:
                continue  # Skip invalid entries

            permission, obj_type, path, obj_hash = parts

            if len(obj_hash) == 41:
                obj_hash = obj_hash[1:]

            # Construct full path for the current item
            full_path = Path(parent_dir) / path
            
            print(f"Processing {obj_type}: {full_path} ({obj_hash})")
            
            if obj_type == "blob":
                Revert.write_file(full_path, obj_hash.strip())
            elif obj_type == "tree":
                # Recursively process subdirectories
                Revert.make_changes_in_dir(obj_hash, full_path)

    @staticmethod
    def write_file(path, blob_hash):
        """Writes file content from a blob object to the filesystem."""
        print(f"Attempting to restore file: {path} from blob {blob_hash}")
        
        file_content = ObjectManager.read_object(blob_hash)
        
        if file_content is None:
            sys.stderr.write(f"Warning: Blob {blob_hash} for {path} not found.\n")
            return
        
        # Ensure the parent directory exists before writing the file
        path.parent.mkdir(parents=True, exist_ok=True)  # Create the parent directories if needed
        
        with open(path, "w") as file:
            file.write(file_content)
        
        print(f"Restored: {path}")














    # @staticmethod
    # def read_object(object_id: str) -> str:
    #     """Read an object (blob, tree, or commit) from the objects directory and return its content."""
    #     obj_dir = Revert.object_dir / object_id[:2]
    #     obj_file = obj_dir / object_id[2:]

    #     if not obj_file.exists():
    #         sys.stderr.write(f"Error: Object {object_id} not found at {obj_file}.\n")
    #         return None

    #     try:
    #         with obj_file.open("rb") as f:
    #             compressed_data = f.read()
    #         decompressed_data = zlib.decompress(compressed_data).decode()
    #         return decompressed_data
    #     except zlib.error as e:
    #         sys.stderr.write(f"Error: Failed to decompress object {object_id} - {e}.\n")
    #         return None
    #     except Exception as e:
    #         sys.stderr.write(f"Error: Unexpected error reading object {object_id} - {e}.\n")
    #         return None
