from pathlib import Path
import sys

def init_bit_track():
    current_dir = Path.cwd()
    bit_track = ".bit_track"

    bit_track_dir = current_dir / bit_track
    print(bit_track_dir)

    if bit_track_dir.is_dir():
        sys.stderr.write("Error: .bit_track already exists" + "\n")
    else:
        bit_track_dir.mkdir()
        objects = bit_track_dir / "objects"
        head = bit_track_dir / "Head"
        objects.mkdir()
        head.touch()
        
        sys.stdout.write("Created an empty .bit_track  repository" + "\n")