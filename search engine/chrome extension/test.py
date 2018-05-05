from readability import Document
import os
import requests
from bs4 import BeautifulSoup
import csv
# from openerp import api
from flask import Flask, jsonify, request
app = Flask(__name__)

from urllib.request import urlopen
# import requests.exceptions

@app.route("/output", methods=['GET'])
def output():
    target = request.args.get('data')
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
    site_content = {}
    site_content[target] = text
    with open('siteContent.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in site_content.items():
            writer.writerow([key, value])
    return "SUCCESS"


if __name__ == "__main__":
    app.run()
