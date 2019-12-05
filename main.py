#!/opt/conda/bin/python3
"""
synology: /usr/local/bin/python3
anaconda docker: /opt/conda/bin/python3
"""

import os
from sys import stdout, stdin
from time import sleep
import subprocess
import logging
import enable_logging
from pathlib import Path

from utils import list_part_files, list_downloaded_files, flush_info, filename_to_url

DOWNLOAD_TO = Path(os.environ.get('DOWNLOAD_TO', (r'/download')))
YDL_PROXY = os.environ.get('YDL_PROXY')

g_cache = Path(__file__).parent.absolute() / 'history.txt'
g_urls = set()


def run_one(url):
    import threading

    flush_info('done queuing ' + url)
    cmd = ['youtube-dl',
           #    url, '--output', rf'{DOWNLOAD_TO}/%(release_date)s.%(title)s.%(ext)s',
           url, '--output', rf'{DOWNLOAD_TO}/%(title)s.%(id)s.%(ext)s',
           # meta
           '--write-info-json',
           #    '--write-description',
           #    '--write-annotations',
           # sub
           '--all-subs',
           '--embed-subs'
           ]

    if YDL_PROXY:
        cmd += ['--proxy', YDL_PROXY]
    subprocess.call(cmd)

    flush_info('done with' + cmd)


def timed_flush(seconds):
    import threading
    from datetime import datetime

    def logged_flush():
        stdout.flush()
        flush_info(str(datetime.now()))

    threading.Timer(seconds, logged_flush).start()


def persist(s):
    s = s.strip()
    global g_urls
    g_urls.add(s)
    flush_info('added ' + s + ('[new]' if s in g_urls else ''))
    flush_info('Historical Items:')
    for i, u in enumerate(g_urls):
        flush_info(f'  {i+1}. {u}')

    g_cache.write_text('\n'.join(g_urls), encoding='utf-8')


def main():
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=8) as executor:
        # timed_flush()
        executor.submit(timed_flush, 60)
        while True:
            s = input(
                f"Input youtube url below:\n").lstrip()
            if s.startswith('https://'):
                executor.submit(run_one, s)
                persist(s)
            elif s == 'resume':
                for name, url in list_part_files(DOWNLOAD_TO).items():
                    flush_info(f'- {name}')
                    if url:
                        executor.submit(run_one, url)
            elif s == 'ls-part':
                list_part_files(DOWNLOAD_TO)
            elif s == 'ls-a':
                list_downloaded_files(DOWNLOAD_TO)
            else:
                pass


def print_help():
    cmds = {
        'resume':      "Resume downloading",
        'ls-part':     "List partially downloaded files",
        'ls-complete': "List fully downloaded files"
    }
    return '\n'.join(f'- {cmd}, {desc}' for cmd, desc in cmds.items())


if __name__ == "__main__":

    enable_logging.init()
    flush_info(f"\nProxy: {YDL_PROXY}, Download folder: {DOWNLOAD_TO}.\nCommands:\n{print_help()}\n")
    print_help()

    main()
