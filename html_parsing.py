import requests
from bs4 import BeautifulSoup

def get_html(url):
    req = requests.get(url, auth=('user', 'pass'))
    return BeautifulSoup(req.text, 'html.parser')

# Gets the url of the file
def parse_href(string):
    indexStart = string.find('href="')+8
    hrefStartString = string[indexStart:]
    indexEnd = hrefStartString.find('"')

    return string[indexStart:indexStart+indexEnd]


# Grabs the threads image/video urls
def parse_urls(array):
    returnValues = []

    for i in array:
        hrefValue = parse_href(str(i))
        returnValues.append(hrefValue)

    return returnValues