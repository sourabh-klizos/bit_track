from utils.create_blob import  create_blob

from pathlib import Path



async def call_recursive():

    ignores = []

    current_dir = Path.cwd()

    bit_track = ".bit_track" # need to ignore this if ignore file doest exists

    bit_ignore = current_dir / ".bitignore"

    if bit_ignore.exists():

        with bit_ignore.open("r") as file:
            ignores = file.read().split("\n")

        # print(content)

    files = [file for file in current_dir.iterdir() if file.is_file()]
    #files = list(current_dir.rglob("*")) it return recursive 

    for file in files:
        # name_of_file = file.split("")
        if not file.name in   ignores:
            print(file.name)
            print(ignores)
            await create_blob(file)





