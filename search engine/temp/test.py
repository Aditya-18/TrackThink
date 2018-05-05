from readability import Document
import os
import requests
from bs4 import BeautifulSoup

# from openerp import api
from flask import Flask, jsonify, request
app = Flask(__name__)
import requests.exceptions

@app.route("/output", methods=['GET'])
def output():
    # obj = request.get_json()
    # print(request)
    target = request.args.get('data')
    try:
        r = requests.get(target,timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        # print ("Http Error:",errh)
        return ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        # print ("Error Connecting:",errc)
        return ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        # print ("Timeout Error:",errt)
        return ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        # print ("OOps: Something Else",err)
        return ("OOps: Something Else",err)
    finally:
        # print ("FAILED")
        return ("FAILED")
        
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
    # print(text)
    return text
    # return request.args.get('data')
    # return jsonify(toString(request.data))


if __name__ == "__main__":
    app.run()
