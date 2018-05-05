from flask import Flask, render_template, request

app = Flask(__name__)

#!/usr/bin/python
import os
import logging
import twitter
import indexer
import pandas as pd
import json
import compileSiteDetails

from collections import defaultdict
# Log initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

CUR_DIR             = os.path.dirname(os.path.realpath(__file__))
CATALOG_FILENAME    = CUR_DIR + "/data/input_file.csv"
STOP_WORDS_FILENAME = CUR_DIR + "/data/stop_words.txt"

def execute_index():
    """Create an index of quality from tf-idf variables to enable rank ordering."""
    query = None
    tw = twitter.Twitter(CATALOG_FILENAME, STOP_WORDS_FILENAME)
    logging.info("[Main] Initializing ...")
    tw.load_tweets_and_build_index()
    docs_number = tw.tweets_count()
    logging.info("[Main] Initialized. %s docs indexed.", "{:,}".format(docs_number))

def execute_search(query):
    """Capture query from STDIN and display the result on STDOUT.

    The query of terms is executed against an indexed data structure
    containing tweets' information.

    """
    tw = twitter.Twitter(CATALOG_FILENAME, STOP_WORDS_FILENAME)    
    logging.info("[Main] Initializing ...")
    tw.load_tweets_and_load_index()
    logging.info("[Main] Initialized. %s docs loaded.", "{:,}".format(tw.tweets_count()))
    search_results = tw.search_tweets(query)
    return search_results

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/Search", methods=['POST'])
def Search():
    read_input=request.form['query']
    search_results=execute_search(read_input)
    data=[]
    if "Sorry, no results." in search_results:
        return str("<h1 style='color=red;'>No url found</h1>") 
    for result in search_results:
        #print(result)
        result=str(result).split(',')
        row=[]
        for x in result:
            x=x.split('~')
            c=0
            for y in x:
                if c==1:
                    row.append(y.strip())
                c+=1
        data.append(row)
    df = pd.DataFrame(data,columns=['Keyword_Matching_Score','Doc_Id','Content','URL','User_Id','Time_Of_Visit','Relevance','Keywords'])
    grouped=df.groupby('User_Id')
    result=''
    for name,group in grouped:
        result=result+"<h1>"+name+"</h1><br>"
        result+="<hr height=35 width=100%>"
        group.sort_values(by='Time_Of_Visit')
        for key,value in group.iterrows():
            #print(value['URL'])
            result+="<p style='font-family:Arial;color:white;background-color:DodgerBlue; border-left: 3px solid DarkBlue;'>"
            result=result+value['Content']+"<br>"
            result=result+"<a href='"+value['URL']+"'>"+value['URL']+"</a><br>"
            result=result+"Keyword_Matching_Score : "+value['Keyword_Matching_Score']+"<br>"
            result=result+"Relevance : "+value['Relevance']+"<br>"
            result=result+"Keywords : "+value['Keywords']+"<br>"
            #result+="<hr height=35 width=100%>"
            result+="</p>"
        #result+="<br>"
    return str(result)

if __name__ == "__main__":

	compileSiteDetails.compileSiteDetails()
	execute_index()
	app.run()