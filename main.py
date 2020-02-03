#!/usr/bin python3

import requests
import os
import urllib.request
import re
import time
import cmd
import sys
import argparse
from multiprocessing import Process
from bs4 import BeautifulSoup

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



def DownloadListOfLinks(links, directory):
    for i in links:
        s = str(i)
        print(s)
        DownloadContent(s, directory + '/' + s[s.rfind("/")+1:])




def GetHrefsFromHtml(array):
    returnValues = []

    for i in array:
        s = str(i)
        hrefValue = GetHrefValue(s)
        returnValues.append(hrefValue)

    return returnValues




def SplitArray(a):
    midpoint = len(a)//2
    return a[:midpoint], a[midpoint:]




def DownloadThreadAttachments(Html, SaveDirectory):
    a = Html.find_all(class_="fileThumb")
    filename = 0 # The name given to the file. So 0.jpg, 1.gif, etc... (iterative)
    
    total_time = 0

    print("Starting download")
    
    if (not os.path.exists(SaveDirectory)):
        print("Save directory doesn't exist, creating it now...")
        os.mkdir(SaveDirectory)
    
    
    
    print("-------------------------------------")
    start_time = time.time()

    links = GetHrefsFromHtml(a)
    length = len(links)

    p1a, p2a = SplitArray(links)

    Process1 = Process(target=DownloadListOfLinks, args = (p1a, SaveDirectory))
    Process2 = Process(target=DownloadListOfLinks, args = (p2a, SaveDirectory))

    Process1.start()
    Process2.start()
    
    Process1.join()
    Process2.join()

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




def ListToString(v):
    return ''.join(v)




def FourChan_Start():
    args = HandleArgs()

    if (ListToString(args['t']) != ''):
        Url = requests.get(ListToString(args['t']), auth=('user', 'pass'))
        Html = BeautifulSoup(Url.text, 'html.parser')

        DownloadThreadAttachments(Html, ListToString(args['d']))



FourChan_Start()    




