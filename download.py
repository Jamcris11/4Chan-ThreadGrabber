import urllib.request
import threading

import util as UTIL

def download_file(url, dest):
    urllib.request.urlretrieve("https://" + url, dest)
    print(url + "\t-- DONE")


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

