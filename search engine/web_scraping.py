from readability import Document
import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import request
import urllib
from readability import Document
import os
import requests
from bs4 import BeautifulSoup
import csv
# from openerp import api
from flask import Flask, jsonify, request
app = Flask(__name__)

from urllib.request import urlopen
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

def summary(target):
    text = ""
    try:
        f = urlopen(target)
        deadLinkFound = False
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
    except:
        deadLinkFound = True
        text = "Can't scrape this URL!"
        # return("Invalid URL")
    # text = "\n\n\n.....\n\n\n"
    text = str(text)
    text = text.replace('\n', ' ')
    if "\n" in text:
        print ("====================")
    #print(text)
    site_content = {}
    site_content[target] = text
    with open('siteContent.csv', 'a', newline='', errors='ignore') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in site_content.items():
            writer.writerow([key, value])
    # return text

def web_scraper():
    # os.remove('siteContent.csv')
    f = open("filename.csv", "w")
    f.truncate()
    f.close()
    # with open('siteContent.csv', 'a', newline='') as csv_file
    site_details = {}
    with open('site_details.csv','rU') as f: 
        reader = csv.reader(f)
        site_details = {rows[0]:rows[1:] for rows in reader}

    for site_detail in site_details.keys():
        # print(site_detail)
        summary(site_detail)


# summary('https://en.wikipedia.org/wiki/Firmware')
# web_scraper()