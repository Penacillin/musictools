import argparse
from append_genre import append_genre


def main(tool, remaining_args):
    if tool == 'append_genre':
        append_genre(remaining_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work with music files')
    parser.add_argument('tool', type=str, metavar='tool')
    args, unknowns = parser.parse_known_args()
    main(args.tool, unknowns)
