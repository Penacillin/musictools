import eyed3
import os
import argparse
from typing import Callable, Dict, List


def _TITLE_TRACKNO_ARTIST(filename: str):
    str_parts = filename.split(' - ')
    return {
        "title": str_parts[0],
        "track_no": str_parts[1],
        "artist": str_parts[2]
    }

EXTRACT_FUNCTIONS: Dict[str, Callable[[str], Dict]] = {
    "TITLE_TRACKNO_ARTIST": _TITLE_TRACKNO_ARTIST
}

def extract_metadata_from_filename(extract_func_name: str, filename: str) -> Dict:
    if extract_func_name not in EXTRACT_FUNCTIONS:
        raise ValueError(f"{extract_func_name} not valid")
    filename = os.path.splitext(filename)[0]
    return EXTRACT_FUNCTIONS[extract_func_name](filename)


def main(file_patterns: List[str]):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract metadata from filename and apply to ID tags')
    parser.add_argument('files', nargs='*', metavar='FILES')
    args = parser.parse_args()
    print(args.files)
    main(args.files)
