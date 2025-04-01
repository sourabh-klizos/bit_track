from bit_track.bit_track_repository import BitTrackRepository
from bit_track.objects import ObjectManager
import sys

import colorama
from colorama import Fore, Style


class BitTrackLogs:
    main_file = BitTrackRepository.main_file
    object_dir = BitTrackRepository.objects_dir

    @staticmethod
    def get_latest_commit():
        return ObjectManager.get_latest_commit()

    @staticmethod
    def get_commit_object(commit_hash):
        """Read the commit object from the object directory using the commit hash."""
        return ObjectManager.read_object(commit_hash)

    @classmethod
    def show_commit_logs(cls, latest_commit_hash):
        """Fetch the latest commit, its parent, and show the commit logs."""
        # latest_commit_hash = cls.get_latest_commit()
        if not latest_commit_hash:
            sys.stdout.write("No latest commit found.\n")
            return

        commit_data = cls.get_commit_object(latest_commit_hash)

        if not commit_data:
            sys.stdout.write(
                f"Commit {latest_commit_hash} not found in objects directory.\n"
            )
            return

        logs = []
        parent_commit = None

        for line in commit_data.splitlines():

            if line.startswith("parent "):
                parent_commit = line.split(" ")[1].strip()
            elif line.startswith("message "):
                commit_message = line.split(" ", 1)[1].strip()
            elif line.startswith("author "):
                author = line.split(" ", 1)[1].strip()
            elif line.startswith("time "):
                timestamp = line.split(" ", 1)[1].strip()

        logs.append(
            {
                "commit": latest_commit_hash,
                "parent": parent_commit,
                "author": author,
                "time": timestamp,
                "message": commit_message,
            }
        )

        sys.stdout.write(f"Commit Logs:\n")
        for log in logs:
            sys.stdout.write(Fore.YELLOW + f"Commit: {Fore.CYAN}{log['commit']}\n")
            sys.stdout.write(
                Fore.YELLOW + f"Parent: {Fore.CYAN}{log['parent'] or 'None'}\n"
            )
            sys.stdout.write(Fore.YELLOW + f"Author: {Fore.MAGENTA}{log['author']}\n")
            sys.stdout.write(Fore.YELLOW + f"Time: {Fore.BLUE}{log['time']}\n")
            sys.stdout.write(Fore.YELLOW + f"Message: {Fore.WHITE}{log['message']}\n")
            sys.stdout.write(Fore.LIGHTBLACK_EX + "-" * 50 + "\n")
        if parent_commit:
            BitTrackLogs.show_commit_logs(parent_commit)

        sys.stdout.write(Style.RESET_ALL + "\n")
