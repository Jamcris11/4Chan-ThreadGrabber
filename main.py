import os
import time
import sys
import threading
from bs4 import BeautifulSoup

import args as ARG
import html_parsing as HTML
import util as UTIL
import download as DL

#-------------------------------------------------------------------------------

def get_download_urls(html_parser):
    return UTIL.four_chan_get_urls(html_parser)


def start_download(url, dir, single_threaded=False):
    urls = get_download_urls(HTML.get_html(url))

    if (not os.path.exists(dir)):
        print("Output directory doesn't exist, creating it now...")
        os.mkdir(dir)


    start_time = time.time()

    if (single_threaded is True):
        DL.download_files(urls, dir)
    else:
        DL.download_files_multithreaded(urls, dir)

    end_time = time.time()
    total_time = end_time-start_time

    return round(total_time, 2)


def start():
    parser, args = ARG.get_args()

    if (args.thread is None or args.dir is None):
        parser.print_help()
        exit()

    print("Starting download...")
    print("-------------------------------------")
    time_elapsed = start_download(args.thread[0], args.dir[0], bool(args.single_threaded))
    print("-------------------------------------")
    print("Download complete! Total time elapsed - " + str(time_elapsed) + " seconds")


if __name__ == '__main__':
    start()
