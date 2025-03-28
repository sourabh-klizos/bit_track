from pathlib import Path
import sys
import zlib


def read_blob(blob_hash):
    current_working_dir = Path.cwd()

    blob_dir = current_working_dir / ".bit_track" / "objects" / blob_hash[:2]

    if not blob_dir.exists():
        sys.stderr.write("Wrong Hash Given ")

    blob_file = blob_dir / blob_hash[2:]

    if not  blob_file.exists():
        sys.stderr.write("Wrong Hash Given ")

    with blob_file.open("rb") as file:
        content = file.read()

    
    actual_content = zlib.decompress(content)
    
    print(actual_content.decode())

        

