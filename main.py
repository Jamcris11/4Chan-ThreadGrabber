import requests
import os
import urllib.request
import re
import time
import cmd
import sys
import threading
from bs4 import BeautifulSoup

import args as ARG
import html_parsing as HTML
import util as UTIL

#-------------------------------------------------------------------------------

def download_file(url, dest):
    urllib.request.urlretrieve("https://" + url, dest)
    print(url + " -- DONE")


def download_files(urls, dir):
    for url in urls:
        download_file(str(url), dir + '/' + UTIL.file_name_from_url(url))


def download_files_multithreaded(urls, dir):
    t1_urls, t2_urls = UTIL.split_array(urls)

    t1 = threading.Thread(target=download_files, args = (t1_urls, dir))
    t2 = threading.Thread(target=download_files, args = (t2_urls, dir))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def four_chan_get_urls(html_parser):
    return HTML.parse_urls(html_parser.find_all(class_="fileThumb"))


def start_thread_download(url, dir, single_threaded=False):
    req = requests.get(url, auth=('user', 'pass'))
    html_parser = BeautifulSoup(req.text, 'html.parser')
    thread_file_urls = four_chan_get_urls(html_parser)


    if (not os.path.exists(dir)):
        print("Output directory doesn't exist, creating it now...")
        os.mkdir(dir)


    start_time = time.time()

    if (single_threaded is True):
        download_files(thread_file_urls, dir)
    else:
        download_files_multithreaded(thread_file_urls, dir)

    end_time = time.time()
    total_time = end_time-start_time

    return round(total_time, 2)


# Entry point
def start():
    parser, args = ARG.get_args()

    if (args.thread is None or args.dir is None):
        parser.print_help()
        exit()

    print("Starting download...")
    print("-------------------------------------")
    time_elapsed = start_thread_download(args.thread[0], args.dir[0], bool(args.single_threaded))
    print("-------------------------------------")
    print("Download complete! Total time elapsed - " + str(time_elapsed) + " seconds")


if __name__ == '__main__':
    start()
