
from readability import Document
import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import request
import urllib
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

def summary(target):
    
    # try:
    #     r = requests.get(target,timeout=3)
    #     r.raise_for_status()
    # except requests.exceptions.HTTPError as errh:
    #     print ("Http Error:",errh)
    #     return
    # except requests.exceptions.ConnectionError as errc:
    #     print ("Error Connecting:",errc)
    #     return
    # except requests.exceptions.Timeout as errt:
    #     print ("Timeout Error:",errt)
    #     return
    # except requests.exceptions.RequestException as err:
    #     print ("OOps: Something Else",err)
    #     return
    # finally:
    #     print ("FAILED")
    #     return
    # f = urlopen(target).code
    # if(f / 100 >= 4):
    #     return ("URL Doesn't exist")
    # if(f == 200):
    #     print ("URL exist")
    try:
      f = urlopen(target)
      deadLinkFound = False
    except:
      deadLinkFound = True
      return("Invalid URL")
    response = requests.get(target)
    
    doc = Document(response.text)
    html = doc.summary()
    soup = BeautifulSoup(html, "lxml")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    print(text)
    return text

summary('https://en.wikipedia.org/wiki/Firmware')


