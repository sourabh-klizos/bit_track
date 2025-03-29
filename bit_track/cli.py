import argparse
from bit_track.bit_track_repository import BitTrackRepository
from bit_track.objects import ObjectManager
import difflib
import sys
from pathlib import Path

from bit_track.index import GitAdd




class BitTrackCLI:
    COMMANDS = {
        "init": BitTrackRepository.init,
        "add" : ObjectManager.create_tree,
        "cat-file -p" :  ObjectManager.read_object,
    }

    @staticmethod
    def handle_command():
        parser = argparse.ArgumentParser(description="BitTrack - A simple version control system")
        parser.add_argument("command", help="Command to execute")
        parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the command")
        
        args = parser.parse_args()
        command = args.command.lower()
        command_args = args.args  # Extra arguments after the command

        # print(command_args)  # Debugging: Check how args are parsed

        if command == "init":
            BitTrackRepository.init()

        elif command == "add":
            # ObjectManager.create_tree(Path.cwd())
            GitAdd.add_all_files()

        elif command == "cat-file":
            if len(command_args) != 2 or command_args[0] != "-p":
                sys.stderr.write("Usage: bit_track cat-file -p <object_id>\n")
                sys.exit(1)
            
            object_id = command_args[1]
            content = ObjectManager.read_object(object_id)
            # sys.stdout.write(content + "\n") 
            # print(content)
            if content:
                sys.stdout.write(content + "\n") 
        
        else:
            suggestions = difflib.get_close_matches(command, BitTrackCLI.COMMANDS.keys())
            suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            sys.stderr.write(f"Error: Unknown command '{command}'.{suggestion_text}\n")
            sys.exit(1)


