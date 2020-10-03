from email.mime import audio
import eyed3
import os
import re
import argparse
import glob
from typing import Callable, Dict, List

from eyed3.core import AudioFile


_REMOVE_TRACKNO_RE = r"\d+\."
_REMOVE_TRACKNO_PROG = re.compile(_REMOVE_TRACKNO_RE)
def _REMOVE_TRACKNO(tag: str) -> str:
    re_res = _REMOVE_TRACKNO_PROG.search(tag)
    if re_res is None:
        return tag
    # print(len(re_res.group()))
    return tag[len(re_res.group()):]

EXTRACT_FUNCTIONS: Dict[str, Callable[[str], str]] = {
    "REMOVE_TRACKNO": _REMOVE_TRACKNO
}

def remove_trackno(extract_func_name: str, tag: str) -> str:
    if extract_func_name not in EXTRACT_FUNCTIONS:
        raise ValueError(f"{extract_func_name} not valid")
    return EXTRACT_FUNCTIONS[extract_func_name](tag)


def main(file_patterns: List[str], dry_run: bool):
    if dry_run:
        print("Running in dry mode.")
    for file_pat in file_patterns:
        for filename in glob.glob(file_pat):
            print(filename)
            if os.path.splitext(filename)[1] not in ['.mp3', '.flac', '.wav', '.ma4']:
                print("Warning: Skipping:", filename)
                continue
            audiofile = eyed3.load(filename)
            if audiofile is None:
                print("Warning: Skipping:", filename)
            new_title = remove_trackno('REMOVE_TRACKNO', audiofile.tag.title).strip()
            print(f"'{audiofile.tag.title}' -> '{new_title}'")
            if not dry_run:
                audiofile.tag.title = new_title
                audiofile.tag.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract metadata from filename and apply to ID tags')
    parser.add_argument('-n', '--dry-run', action='store_true', help="Don't edit files, outputs changes")
    parser.add_argument('files', nargs='*', metavar='FILES', help="file patters to glob for files")
    args = parser.parse_args()
    main(args.files, args.dry_run)
