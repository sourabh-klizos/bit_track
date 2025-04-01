from pathlib import Path
from bit_track.objects import ObjectManager

import colorama
from colorama import Fore, Style
import sys
from bit_track.bit_track_repository import BitTrackRepository


class Revert:
    
    object_dir = BitTrackRepository.objects_dir

    





    @staticmethod
    def revert_to_old_tree(commit_hash: str) -> None:

        content = ObjectManager.read_object(commit_hash)
        # print(content, " commit content")
        tree_hash = content.splitlines()[0].split()[1]

        commit_exists = ObjectManager.read_object(tree_hash)

        if commit_exists == None:
            return "Provide A Valid Commit Hash"
        

        Revert.make_changes_in_dir(tree_hash)
        

        return tree_hash  


    @staticmethod
    def make_changes_in_dir(tree_hash):
        tree_content = ObjectManager.read_object(tree_hash)

        if not tree_content:
            return "Yo have Deleted the BitTrack  Blobs"
        
        for item in tree_content.splitlines():
            # print(item, " =================")
            permission , obj_type , path , hash = item.split()

            if obj_type == "blob":
                pass
                # create a function to write in path actual content

                Revert.write_file(path, hash)

            print(obj_type)
            


    @staticmethod
    def write_file(path, blob_hash):

        current_working_dir = Path.cwd()

        file_path = current_working_dir / path

        print(file_path)


