import argparse
from sys import exit as sys_exit

def parse_args():

    parser = argparse.ArgumentParser(description="Process directories renaming subtitle files based on the names of the corresponding chapter video files")

    parser.add_argument(
        "directories",
        nargs="*",
        help="List of directories to process"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively process directories"
    )

    parser.add_argument(
        "-p", "--preview",
        action="store_true",
        help="Preview mode (asks for confirmation for each file)"
    )

    parser.add_argument(
        "-n", "--no-log",
        action="store_true",
        help="Disables logging"
    )

    return parser.parse_args()

def validate_args(args):
    if not args.directories:
        print("Usage: python main.py [OPTIONS] <directory> or <directory_1> <directory_2> ... <directory_n>")
        print("Options:")
        print("  --recursive, -r  Recursively rename files in subdirectories")
        print("  --preview, -p    Preview the changes before renaming")
        sys_exit(1)

def get_args():
    args = parse_args()
    validate_args(args)
    return args.recursive, args.preview, args.no_log, args.directories
