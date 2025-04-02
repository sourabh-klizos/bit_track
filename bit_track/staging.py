import sys
from pathlib import Path
import zlib
import os
from bit_track.bit_track_repository import BitTrackRepository
import colorama
from colorama import Fore, Style

# from bit_track.objects import ObjectManager
from bit_track.utils.file_handler import FileHandler

from bit_track.bit_ignore import BitIgnore
import hashlib


class BitTrackStaging:
    """Handles staging operations for BitTrack."""

    BIT_TRACK_DIR = BitTrackRepository.worktree
    INDEX_FILE = BitTrackRepository.index_file
    OBJECTS_DIR = BitTrackRepository.objects_dir

    @staticmethod
    def check_repo():
        """Ensure the .bit_track repository exists."""
        if not BitTrackStaging.BIT_TRACK_DIR.exists():
            sys.stderr.write(
                "Error: Repository not initialized. Run `bit_init` first.\n"
            )
            sys.exit(1)

    @staticmethod
    def update_index(file_path: str, object_id: str):
        """Update the index file with the full relative path and object hash."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE
        index_entries = {}

        hash_ids = list()

        repo_root = BitTrackStaging.BIT_TRACK_DIR.parent
        absolute_path = Path(file_path).resolve()

        try:
            relative_path = absolute_path.relative_to(repo_root)
        except ValueError:
            # sys.stderr.write(f"Error: '{file_path}' is outside the repository.\n")
            return

        if index_file.exists():
            with index_file.open("rb") as f:
                compressed_data = f.read()
                if compressed_data:
                    try:
                        decompressed_data = zlib.decompress(compressed_data).decode()
                        for line in decompressed_data.splitlines():
                            mode, obj_id, path = line.strip().split(" ", 2)
                            index_entries[path] = (mode, obj_id)
                            hash_ids.append(obj_id)
                    except zlib.error:
                        sys.stdout.write("Error: Corrupted index file.\n")
                        return

        index_entries[str(relative_path)] = ("100644", object_id)

        index_content = "\n".join(
            f"{mode} {obj_id} {path}" for path, (mode, obj_id) in index_entries.items()
        )
        compressed_content = zlib.compress(index_content.encode())

        with index_file.open("wb") as f:
            f.write(compressed_content)

        sys.stdout.write(f"{Fore.YELLOW} Files added  ")
        # sys.stdout.write(f"\t {relative_path}\n")
        sys.stdout.write(f"\t {Fore.CYAN}{relative_path}{Style.RESET_ALL}\n ")

    @staticmethod
    def show_staging():
        """Display the staged files from the index."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE

        if not index_file.exists():
            sys.stdout.write("No files staged.\n")
            return

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

        sys.stdout.write("Staged files:\n")
        for line in decompressed_data.splitlines():
            mode, obj_id, path = line.strip().split(" ", 2)
            # sys.stdout.write(f"  {mode} {obj_id} {path}\n")
            sys.stdout.write(
                f" {Fore.CYAN}{mode}{Style.RESET_ALL} "
                f"{Fore.YELLOW}{obj_id}{Style.RESET_ALL} "
                f"{Fore.MAGENTA}{path}{Style.RESET_ALL}\n"
            )

    @staticmethod
    def clear_staging():
        """Clear all staged files without deleting the index file, and remove corresponding objects."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE
        objects_dir = BitTrackStaging.OBJECTS_DIR

        if not index_file.exists() or index_file.stat().st_size == 0:
            sys.stdout.write("No files staged.\n")
            return

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

    @staticmethod
    def clear_staging_only_from_index():
        """Clear all staged files without deleting the index file, and keep corresponding objects."""
        BitTrackStaging.check_repo()
        index_file = BitTrackStaging.INDEX_FILE

        if not index_file.exists() or index_file.stat().st_size == 0:
            sys.stdout.write("No files staged.\n")
            return

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

        # Clear the index file without deleting objects
        with index_file.open("wb") as f:
            f.write(zlib.compress(b""))

        # sys.stdout.write("Staging area cleared, but objects are retained.\n")
