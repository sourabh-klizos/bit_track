import argparse
from bit_track.bit_track_repository import BitTrackRepository
from bit_track.objects import ObjectManager
import difflib
import sys
from pathlib import Path

from bit_track.index import BitTrackAdd
from bit_track.staging import BitTrackStaging



import argparse
import sys
import difflib

class BitTrackCLI:
    COMMANDS = {
        "init": BitTrackRepository.init,
        "add": ObjectManager.create_tree,
        "cat-file -p": ObjectManager.read_object,
        "status": BitTrackStaging.show_staging,
        "reset": BitTrackStaging.clear_staging 
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
                sys.stdout.write(content + "\n")

        elif command == "status":
            BitTrackStaging.show_staging()  # Call the status function

        elif command == "reset":
            BitTrackStaging.clear_staging()

        else:
            suggestions = difflib.get_close_matches(command, BitTrackCLI.COMMANDS.keys())
            suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            sys.stderr.write(f"Error: Unknown command '{command}'.{suggestion_text}\n")
            sys.exit(1)

