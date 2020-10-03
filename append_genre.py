import argparse
import glob
import sys
import itertools
from typing import Sequence, Text
import eyed3
import os


def _driver(file: str, genre_tag: str):
    print('Processing: "' + file + '"')
    audio_file = eyed3.core.load(file)
    previous_genre = audio_file.tag.genre
    new_genre = previous_genre.name.strip() + f"; {genre_tag}"
    print(f"\"{previous_genre.name}\" -> \"{new_genre}\"")
    audio_file.tag.genre = eyed3.id3.Genre.parse(new_genre)
    audio_file.tag.save()


def append_genre(args: Sequence[Text]):
    parser = argparse.ArgumentParser(description='append genre tag')
    parser.add_argument(
        "file_path", metavar="path", type=str,
        help="Path to files to be add genre to; enclose in quotes, accepts * as wildcard for directories or filenames")
    parser.add_argument(
        "genre", metavar="genre", type=str,
        help="genre tag to add")
    parsed_args = parser.parse_args(args)
    files = glob.iglob(parsed_args.file_path)

    try:
        first_file = next(files)
    except StopIteration:
        print('File does not exist: ' + parsed_args.file_path, file=sys.stderr)
        sys.exit(1)
    for filename in itertools.chain([first_file], files):
        if os.path.splitext(filename)[1] not in ['.mp3', '.flac', '.wav', '.ma4']:
            print("Warning: Skipping:", filename)
            continue
        _driver(filename, parsed_args.genre)
        print("")
