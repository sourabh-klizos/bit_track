import argparse
from bit_track.bit_track_repository import BitTrackRepository
from bit_track.objects import ObjectManager
import difflib
import sys
from pathlib import Path

from bit_track.index import BitTrackAdd
from bit_track.staging import BitTrackStaging
from bit_track.commit_logs import BitTrackLogs

import colorama
from colorama import Fore, Style

import argparse
import sys
import difflib

class BitTrackCLI:
    COMMANDS = {
        "init": BitTrackRepository.init,
        "add": ObjectManager.create_tree,
        "cat-file -p": ObjectManager.read_object,
        "status": BitTrackStaging.show_staging,
        "reset": BitTrackStaging.clear_staging ,
        "logs" :BitTrackLogs.show_commit_logs,
    }

    @staticmethod
    def handle_command():
        parser = argparse.ArgumentParser(description="BitTrack - A simple version control system")
        parser.add_argument("command", help="Command to execute")
        parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the command")

        args = parser.parse_args()
        command = args.command.lower()
        command_args = args.args  # Extra arguments after the command

        if command == "init":
            BitTrackRepository.init()

        elif command == "add":
            BitTrackAdd.add_all_files()

        elif command == "cat-file":
            if len(command_args) != 2 or command_args[0] != "-p":
                sys.stderr.write("Usage: bit_track cat-file -p <object_id>\n")
                sys.exit(1)
            
            object_id = command_args[1]
            content = ObjectManager.read_object(object_id)
            if content:
                # sys.stdout.write(content + "\n")
                sys.stdout.write(Fore.GREEN + "Object Content:\n" + Style.RESET_ALL)
                sys.stdout.write(Fore.YELLOW + content + "\n" + Style.RESET_ALL)

        elif command == "status":
            BitTrackStaging.show_staging()  # Call the status function

        elif command == "reset":
            BitTrackStaging.clear_staging()

        elif command == "commit":
            if len(command_args) != 2 or command_args[0] != "-m":
                sys.stderr.write("Usage: bit_track commit -m 'example message' ")
                
                sys.exit(1)
            # print(Path.cwd())

            # tree_object_id = ObjectManager.create_tree(Path.cwd(),command_args[1] )
            tree_object_id = ObjectManager.create_tree(Path.cwd())
            # print(command_args[1])
            # ObjectManager.set_commit_message(command_args[1])


            # print("tree_object_id == ",tree_object_id)

            if tree_object_id:
                ObjectManager.store_snapshot_and_commit(tree_object_id,command_args[1])
                BitTrackStaging.clear_staging_only_from_index()

        elif command == "log":
            latest_commit_hash = BitTrackLogs.get_latest_commit()
            BitTrackLogs.show_commit_logs(latest_commit_hash)


        else:
            suggestions = difflib.get_close_matches(command, BitTrackCLI.COMMANDS.keys())
            suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            sys.stderr.write(f"Error: Unknown command '{command}'.{suggestion_text}\n")
            sys.exit(1)

