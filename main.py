#!/usr/bin python3

import requests
import os
import urllib.request
import re
import time
import cmd
import sys
import argparse
import threading
from bs4 import BeautifulSoup

def Directory_Exists(uri):
    if os.path.exists(uri) == True:
        return True
    else:
        return False

#-------------------------------------------------------------------------------	
	
	
def GetFileType(string):
    index = string.rfind('.')

    return string[index:]


def GetHrefValue(string):
    indexStart = string.find('href="')+8
    hrefStartString = string[indexStart:]
    indexEnd = hrefStartString.find('"')

    return string[indexStart:indexStart+indexEnd]


def DownloadContent(url, destination):
    urllib.request.urlretrieve("https://" + url, destination)



def DownloadListOfLinks(links, directory, filename):
    for i in links:
        s = str(i)
        print(str(filename) + GetFileType(s))
        DownloadContent(s, directory + '/' + str(filename) + GetFileType(s))
        filename += 1




def GetHrefsFromHtml(array):
    returnValues = []

    for i in array:
        s = str(i)
        hrefValue = GetHrefValue(s)
        returnValues.append(hrefValue)

    return returnValues




def DownloadThreadAttachments(album, SaveDirectory):
    a = album.find_all(class_="fileThumb")
    filename = 0 # The name given to the file. So 0.jpg, 1.gif, etc... (iterative)
    
    total_time = 0

    print("Starting download")
    
    if (not Directory_Exists(SaveDirectory)):
        print("Save directory doesn't exist, creating it now...")
        os.mkdir(SaveDirectory)
    
    
    start_time = time.time()
    print("-------------------------------------")

    links = GetHrefsFromHtml(a)
    length = len(links)

    Thread1 = threading.Thread(target=DownloadListOfLinks, args = (links[:length//2], SaveDirectory, 0))
    Thread2 = threading.Thread(target=DownloadListOfLinks, args = (links[length//2:], SaveDirectory, length//2))

    Thread1.start()
    Thread2.start()
    
    Thread1.join()
    Thread2.join()

    end_time = time.time()
    total_time = end_time-start_time
    
    print("-------------------------------------")
    print("Download complete! Total time elapsed - " + str(round(total_time, 2)) + " seconds")
    




def AddArguments(parser):
    parser.add_argument('-d', metavar='DIR', type=str, nargs=1,
            help='sets the directory for image storage.')

    parser.add_argument('-t', metavar='URL', type=str, nargs=1,
            help='downloads images from URL thread.')



def HandleArgs():
    parser = argparse.ArgumentParser(
            description="4Chan thread image downloader.")
    
    AddArguments(parser)
    args = parser.parse_args()
    args = vars(args)

    return args


def FourChan_Start():
    args = HandleArgs()

    if (ListToString(args['t']) != ''):
        Url = requests.get(ListToString(args['t']), auth=('user', 'pass'))
        Html = BeautifulSoup(Url.text, 'html.parser')

        DownloadThreadAttachments(Html, ListToString(args['d']))

def ListToString(v):
    return ''.join(v)

FourChan_Start()    




