from nlp_rake import rake
import csv

def extractKeywords():
    stoppath = 'data/stoplists/SmartStoplist.txt'

    rake_object = rake.Rake(stoppath, 5, 3, 4)

    # sample_file = open("data/docs/fao_test/w2167e.txt", 'r', encoding="iso-8859-1")
    # text = sample_file.read()
    mydict = {}
    with open('siteContent.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        # next(reader)
        mydict = dict(reader)

    keywords_details = []
    for k, v in mydict.items():
        keywords = rake_object.run(v)

        det = []
        # 3. print results
        # print("Keywords:", keywords)
        words = []
        for word in keywords:
            words.append(word[0])
            # print (word[0], "   ")
            # print ("\n")
       # print (words)
        det.append(k)
        det.append(v)
        det.append(words)
        keywords_details.append(det)
        # keywords_details[k].append(words)


    with open('siteContentNew.csv', 'w', newline='') as csv_file:     
        writer = csv.writer(csv_file)
        for key in keywords_details:
            writer.writerow(key)

# extractkeywords()