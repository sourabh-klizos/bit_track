from pathlib import Path
from bit_track.objects import ObjectManager

import colorama
from colorama import Fore, Style
import sys
from bit_track.bit_track_repository import BitTrackRepository


class Revert:
    object_dir = BitTrackRepository.objects_dir

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
                continue

            permission, obj_type, path, obj_hash = parts

            if len(obj_hash) == 41:
                obj_hash = obj_hash[1:]

            full_path = Path(parent_dir) / path

            if obj_type == "blob":
                Revert.write_file(full_path, obj_hash.strip())
            elif obj_type == "tree":
                Revert.make_changes_in_dir(obj_hash, full_path)

    @staticmethod
    def write_file(path, blob_hash):
        """Writes file content from a blob object to the filesystem."""

        file_content = ObjectManager.read_object(blob_hash)

        if file_content is None:
            sys.stderr.write(f"Warning: Blob {blob_hash} for {path} not found.\n")
            return

        path.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create the parent directories if needed

        with open(path, "w") as file:
            file.write(file_content)

        sys.stdout.write(
            f"{Fore.GREEN}Changes successfully reverted: {path}{Style.RESET_ALL}\n"
        )
