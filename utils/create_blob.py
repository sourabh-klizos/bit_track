from pathlib import Path
import shutil
import sys
import hashlib
import zlib


def create_blob(file_path:str) -> str:

    current_working_dir = Path.cwd()
    file_exists = current_working_dir  / file_path


    if not file_exists.is_file():
        return

    with file_exists.open("rb") as file:
        content = file.read()

    header = f"blob {len(content)}".encode() + b"\0"

    hash_content =   hashlib.sha1(header + content).hexdigest()


    objects_fir =  current_working_dir / ".bit_track"/ "objects"
    

    blob_dir_hash = objects_fir/ hash_content[:2]
    blob_dir_hash.mkdir(parents=True, exist_ok=True) 

 

    blob_file = blob_dir_hash  / hash_content[2:]

    if not blob_file.exists():
        blob_file.touch()  
    

    compress_content = zlib.compress(content)

    # print(compress_content)

    with blob_file.open("wb")  as file:
        file.write(compress_content)


    # print(content)
    return hash_content






