import argparse
import asyncio.runners
import shutil
import os
import sys
from utils.init_bit_track import init_bit_track 
from utils.create_blob import create_blob
from utils.read_blob import read_blob
import asyncio
from utils.add import call_recursive



def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="commands")

    # parser.add_argument("init", help="Create an empty Git repository or reinitialize an existing one" )
    init = subparser.add_parser("init",help="Create an empty Git repository or reinitialize an existing one" )

    blob = subparser.add_parser("blob",help="" )

    blob_parser = subparser.add_parser("cat-file", help="Show the contents of a blob")
    blob_parser.add_argument("-p", metavar="HASH", required=True, help="Hash of the blob to display")

    add  = subparser.add_parser("add", help="Show the contents of a blob")

    

    args =  parser.parse_args()


    if args.commands == "init":
        init_bit_track()
    elif args.commands == "blob":
        create_blob("test.txt")
    elif args.commands == "cat-file" :
        read_blob(args.p)
    elif args.commands == "add" :
        call_recursive()










if __name__ == "__main__":

    main()


    

    
    # # print(args.init)
    # if args.init:
    #     value = init_bit_track()
    #     # sys.stdout.write(value)