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



# Gets the url of the file
def GetHrefValue(string):
    indexStart = string.find('href="')+8
    hrefStartString = string[indexStart:]
    indexEnd = hrefStartString.find('"')

    return string[indexStart:indexStart+indexEnd]



# Downloads a file from a url and places it at "destination"
def DownloadContent(url, destination):
    urllib.request.urlretrieve("https://" + url, destination)



# Takes a list of links, downloads them
def DownloadListOfLinks(links, directory):
    for i in links:
        s = str(i)
        print(s)
        DownloadContent(s, directory + '/' + s[s.rfind("/")+1:])



# Grabs the threads image/video urls
def GetFileUrls(array):
    returnValues = []

    for i in array:
        hrefValue = GetHrefValue(str(i))
        returnValues.append(hrefValue)

    return returnValues



# Splits the array into two so that both threads can handle a portion
def SplitArray(a):
    midpoint = len(a)//2
    return a[:midpoint], a[midpoint:]



# Takes the threads HTML and downloads all the images/videos
def DownloadThreadFiles(Html, SaveDirectory):
    a = Html.find_all(class_="fileThumb")
    filename = 0 # The name given to the file. So 0.jpg, 1.gif, etc... (iterative)
    
    total_time = 0

    print("Starting download")
    
    if (not os.path.exists(SaveDirectory)):
        print("Save directory doesn't exist, creating it now...")
        os.mkdir(SaveDirectory)
    
    
    
    print("-------------------------------------")
    start_time = time.time()

    links = GetFileUrls(a)
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
    



# Initialises the arguments for the program
def InitArgs(parser):
    parser.add_argument('-d', metavar='DIR', type=str, nargs=1,
            help='sets the directory for image storage.')

    parser.add_argument('-t', metavar='URL', type=str, nargs=1,
            help='downloads images from URL thread.')



# Gets the arguments provider by the user
def GetArgs():
    parser = argparse.ArgumentParser(
            description="4Chan thread image downloader.")
    
    InitArgs(parser)
    args = parser.parse_args()
    args = vars(args)

    return args




def ListToString(v):
    return ''.join(v)



# Entry point
def FourChan_Start():
    args = GetArgs()

    if (ListToString(args['t']) != '' and ListToString(args['d']) != ''):
        Url = requests.get(ListToString(args['t']), auth=('user', 'pass'))
        Html = BeautifulSoup(Url.text, 'html.parser')

        DownloadThreadFiles(Html, ListToString(args['d']))

if __name__ == '__main__':
    FourChan_Start()    




