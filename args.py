import argparse

import globals as GLOBALS

# Takes a list with one element and extracts to object for easier handling
def list_2_obj(list):
	return list[0]



def init_args(parser):
	parser.add_argument('--dir', metavar='DIR', type=str, nargs=1, help='sets the directory for image storage.')
	parser.add_argument('--thread', metavar='URL', type=str, nargs=1, help='downloads images from URL thread.')
	parser.add_argument('--single-threaded', action="store_true", help='forces the program to run in a single thread.')


def get_args():
    parser = argparse.ArgumentParser(
        description=GLOBALS.DESCRIPTION)

    init_args(parser)
    args = parser.parse_args()

    return parser, args