#!/usr/bin python3

import requests
import os
import urllib.request
import re
import time
import cmd
import sys
import argparse
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

def DownloadThreadAttachments(album, SaveDirectory):
    a = album.find_all(class_="fileThumb")
    returnArray = {}
    filename = 0 # The name given to the file. So 0.jpg, 1.gif, etc... (iterative)
    
    total_time = 0

    print("Starting download")
    
    if (not Directory_Exists(SaveDirectory)):
        print("Save directory doesn't exist, creating it now...")
        os.mkdir(SaveDirectory)

    print("-------------------------------------")
    for i in a:
        s = str(i)
        hrefValue = GetHrefValue(s) # Get image link to request download

        start_time = time.time()
        
        try:
            print(str(filename) + GetFileType(hrefValue), end = '')
            DownloadContent(hrefValue, SaveDirectory + "/" + str(filename) + GetFileType(hrefValue))

        except:
            print("\t\t failed")
            filename += 1
            continue
        
        end_time = time.time() - start_time
        total_time += end_time
        filename += 1
        print("\t\t" + str(round(end_time, 2)), " seconds")

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




