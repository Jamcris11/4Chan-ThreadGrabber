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

#----------------------------------------------------------------------------------------------------------------------------------	
	
	
def FourChan_GetFileType(string, num):
    if string[num-4:num] == ".jpg":
        return ".jpg"
    elif string[num-4:num] == ".png":
        return ".png"
    elif string[num-5:num] == ".webm":
        return ".webm"
    elif string[num-4:num] == ".gif":
        return ".gif"




def DownloadThreadAttachments(album, SaveDirectory):
    a = album.find_all(class_="fileThumb")
    returnArray = {}
    filename = 0
    
    print("Starting download")

    for i in a:
        
        s = str(i)
        num1 = s.find('href="')+8
        href = s[num1:]
        num2 = href.find('"')

        start_time = time.time()
        
        try:
            if (Directory_Exists(SaveDirectory)): # Checks if the directory we want to save our photos to exists.
                print(str(filename) + FourChan_GetFileType(s[num1:num1+num2], num2), end = '')

                urllib.request.urlretrieve("https://"+ s[num1:num1+num2], SaveDirectory + "/" + str(filename) +
                        FourChan_GetFileType(s[num1:num1+num2], num2))
                
            else: # If the directory doesn't exist, create it.      
                print("Save directory doesn't exist, creating now...")
                os.mkdir(SaveDirectory)
                print(str(filename) + FourChan_GetFileType(s[num1:num1+num2], num2), end = '')

                urllib.request.urlretrieve("https://"+ s[num1:num1+num2], SaveDirectory + "/" + str(filename) +
                        FourChan_GetFileType(s[num1:num1+num2], num2))

            filename = filename + 1
        except:
            print("\t\t failed")
            filename = filename + 1
            continue
        
        end_time = time.time() - start_time
        print("\t\t" + str(round(end_time, 2)), " seconds")
        

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



