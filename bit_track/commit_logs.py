from bit_track.bit_track_repository import BitTrackRepository
from bit_track.objects import ObjectManager
import sys
from pathlib import Path

# class BitTrackLogs():

#     main_file = BitTrackRepository.main_file
#     object_dir = BitTrackRepository.objects_dir

#     # latest_commit = ObjectManager.get_latest_commit()

#     @staticmethod
#     def get_latest_commit():
#         return ObjectManager.get_latest_commit()


#     def show_commit_logs():

#         get_latest_commit = BitTrackLogs.get_latest_commit()



class BitTrackLogs:
    main_file = BitTrackRepository.main_file
    object_dir = BitTrackRepository.objects_dir

    @staticmethod
    def get_latest_commit():
        print(ObjectManager.get_latest_commit(), "==========================")
        return ObjectManager.get_latest_commit()

    @staticmethod
    def get_commit_object(commit_hash):
        """Read the commit object from the object directory using the commit hash."""
        print(ObjectManager.read_object(commit_hash))
        return ObjectManager.read_object(commit_hash)

    @classmethod
    def show_commit_logs(cls):
        """Fetch the latest commit, its parent, and show the commit logs."""
        latest_commit_hash = cls.get_latest_commit()
        if not latest_commit_hash:
            sys.stdout.write("No latest commit found.\n")
            return
        
        commit_data = cls.get_commit_object(latest_commit_hash)
        if not commit_data:
            sys.stdout.write(f"Commit {latest_commit_hash} not found in objects directory.\n")
            return
        
        logs = []
        parent_commit = None
        
        # Parse the latest commit data
        for line in commit_data.splitlines():
            if line.startswith("parent "):
                parent_commit = line.split(" ")[1].strip()
            
            elif line.startswith("message "):
                commit_message = line.split(" ", 1)[1].strip()
            elif line.startswith("author "):
                author = line.split(" ", 1)[1].strip()
            elif line.startswith("time "):
                timestamp = line.split(" ", 1)[1].strip()
        
        # Store the commit log information in the list
        logs.append({
            "commit": latest_commit_hash,
            "parent": parent_commit,
            "author": author,
            "time": timestamp,
            "message": commit_message
        })
        
        # Print the logs
        sys.stdout.write(f"Commit Logs:\n")
        for log in logs:
            sys.stdout.write(f"Commit: {log['commit']}\n")
            sys.stdout.write(f"Parent: {log['parent']}\n")
            sys.stdout.write(f"Author: {log['author']}\n")
            sys.stdout.write(f"Time: {log['time']}\n")
            sys.stdout.write(f"Message: {log['message']}\n")
            sys.stdout.write("-" * 50 + "\n")

        # Optionally, you can continue fetching the parent commit recursively if needed
        # and print that commit log as well.
        if parent_commit:
            sys.stdout.write(f"Fetching parent commit {parent_commit}...\n")
            # Call the show_commit_logs again to print the parent commit
            BitTrackLogs.show_commit_logs()








