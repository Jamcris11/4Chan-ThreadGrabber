import argparse

import globals as GLOBALS

# Takes a list with one element and extracts to object for easier handling
def list_2_obj(list):
	return list[0]



def init_args(parser):
	parser.add_argument('-d', '--dir', metavar='DIR', default='thread/', type=str, nargs=1, help='the directory for attachments to go (default thread/)')
	parser.add_argument('--single-threaded', action="store_true", help='forces the program to run in a single thread')
	parser.add_argument('thread', metavar='URL', type=str, help='url to download attachments from (required)')


def get_args():
    parser = argparse.ArgumentParser(
        description=GLOBALS.DESCRIPTION)

    init_args(parser)
    args = parser.parse_args()

    if args.dir is list:
        args.dir = str(args.dir)

    return parser, args
