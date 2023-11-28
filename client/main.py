import argparse
import sys

import fetch
import publish
    
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#fetch parser
fetch_parser = subparser.add_parser("fetch", help="Fetch parser")
fetch_parser.add_argument("fname", help="file name to fetch")
fetch_parser.set_defaults(func=fetch.fetch)

#publish parser
publish_parser = subparser.add_parser("publish", help="Publish parser")
publish_parser.add_argument("lname", help="path to the file")
publish_parser.add_argument("fname", help="alias file name when published")
publish_parser.set_defaults(func=publish.publish_print)

while True:
    user_input = input("> ")
    if user_input == "exit":
        sys.exit(0)
    args = parser.parse_args(user_input.split())
    args.func(args)