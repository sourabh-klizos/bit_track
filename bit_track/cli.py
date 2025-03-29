import argparse
from bit_track.bit_track_repository import BitTrackRepository
import difflib
import sys





class BitTrackCLI:
    COMMANDS = {
        "init": BitTrackRepository.init,
    }

    @staticmethod
    def handle_command():
        parser = argparse.ArgumentParser(description="BitTrack - A simple version control system")
        parser.add_argument("command", help="Command to execute")
        args = parser.parse_args()
        


        command = args.command.lower()
        if command in BitTrackCLI.COMMANDS:
            BitTrackCLI.COMMANDS[command]()
        else:
            # Suggest similar commands if an invalid command is given
            suggestions = difflib.get_close_matches(command, BitTrackCLI.COMMANDS.keys())
            suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
            sys.stderr.write(f"Error: Unknown command '{command}'.{suggestion_text}\n")
            sys.exit(1)

