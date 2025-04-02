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
from bit_track.revert import Revert


class BitTrackCLI:
    COMMANDS = {
        "init": "Initialize a new BitTrack repository (No arguments)",
        "add": "Add all files to the staging area (No arguments)",
        "cat-file": "Display the content of a stored object (-p <object_id>)",
        "status": "Show the current staging status (No arguments)",
        "reset": "Clear the staging area (No arguments)",
        "commit": "Commit staged changes with a message (-m 'message')",
        "log": "Display the commit log (No arguments)",
        "revert": "Revert to a previous commit (<commit_hash>)",
        "help": "Display help information for available commands",
    }

    @staticmethod
    def handle_command():
        parser = argparse.ArgumentParser(
            description=Fore.CYAN
            + "BitTrack - A simple version control system"
            + Style.RESET_ALL,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            "command", help=f"{Fore.YELLOW}Command to execute{Style.RESET_ALL}"
        )
        parser.add_argument(
            "args",
            nargs=argparse.REMAINDER,
            help=Fore.GREEN + "Additional arguments for the command" + Style.RESET_ALL,
        )

        if len(sys.argv) == 1:
            print(Fore.RED + "Error: No command provided!" + Style.RESET_ALL)
            parser.print_help()
            sys.exit(1)

        if "--help" in sys.argv or "-h" in sys.argv:
            print(Fore.CYAN + "Available Commands:" + Style.RESET_ALL)
            for cmd, desc in BitTrackCLI.COMMANDS.items():
                print(Fore.YELLOW + f"{cmd}: " + Fore.GREEN + desc + Style.RESET_ALL)
            sys.exit(0)

        args = parser.parse_args()
        command = args.command.lower()
        command_args = args.args

        if command == "init":
            BitTrackRepository.init()

        elif command == "add":
            BitTrackAdd.add_all_files()

        elif command == "cat-file":
            if len(command_args) != 2 or command_args[0] != "-p":
                sys.stderr.write(
                    Fore.RED
                    + "Usage: bit_track cat-file -p <object_id>\n"
                    + Style.RESET_ALL
                )
                sys.exit(1)
            object_id = command_args[1]
            content = ObjectManager.read_object(object_id)
            if content:
                sys.stdout.write(Fore.GREEN + "Object Content:\n" + Style.RESET_ALL)
                sys.stdout.write(Fore.YELLOW + content + "\n" + Style.RESET_ALL)

        elif command == "status":
            BitTrackStaging.show_staging()

        elif command == "reset":
            BitTrackStaging.clear_staging()

        elif command == "commit":
            if len(command_args) != 2 or command_args[0] != "-m":
                sys.stderr.write(
                    Fore.RED
                    + "Usage: bit_track commit -m 'example message'\n"
                    + Style.RESET_ALL
                )
                sys.exit(1)
            tree_object_id = ObjectManager.create_tree(Path.cwd())
            if tree_object_id:
                ObjectManager.store_snapshot_and_commit(tree_object_id, command_args[1])
                BitTrackStaging.clear_staging_only_from_index()

        elif command == "log":
            latest_commit_hash = BitTrackLogs.get_latest_commit()
            BitTrackLogs.show_commit_logs(latest_commit_hash)

        elif command == "revert":
            if len(command_args) != 1:
                sys.stderr.write(
                    Fore.RED
                    + "Usage: bit_track revert <commit_hash>\n"
                    + Style.RESET_ALL
                )
                sys.exit(1)
            commit_hash = command_args[0]
            if commit_hash:
                Revert.revert_to_old_tree(commit_hash)

        else:
            suggestions = difflib.get_close_matches(
                command, BitTrackCLI.COMMANDS.keys()
            )
            suggestion_text = (
                f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            )
            sys.stderr.write(
                Fore.RED
                + f"Error: Unknown command '{command}'.{suggestion_text}\n"
                + Style.RESET_ALL
            )
            sys.exit(1)


if __name__ == "__main__":
    BitTrackCLI.handle_command()
