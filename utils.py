from pathlib import Path
import logging
from sys import stdout, stdin




def flush_info(s):
    logging.info(s)
    stdout.flush()  # Remember to flush


def filename_to_url(f):
    import json

    stem = f.name.split('.', 1)[0]
    meta = f.parent / f'{stem}.info.json'
    if meta.exists():
        with open(meta, encoding='utf-8') as m:
            url = json.load(m)['webpage_url']
            return url


def list_part_files(root):
    return {f.name: filename_to_url(f) for f in Path(root).glob('*.part')}

def list_downloaded_files(root):
    for f in Path(root).glob('*.mp4'):
        flush_info(f'- {f.name}')


def rename(root):
    # root = Path(r'Z:\video\youtube')
    for f in root.glob("NA*.*"):
        new_ = f.name.replace('NA.', '')
        new_ = root / new_
        try:
            f.rename(new_)
        except:
            print(f)