import csv
import pprint

def merge_csv():
    mydict = {}
    with open('siteContentNew.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        # next(reader)
        # mydict = dict(reader)
        mydict = {rows[0]:rows[1:] for rows in reader}

    # print (mydict)
    all_details = {}
    site_details = {}
    with open('site_details.csv','rU') as f: 
        reader = csv.reader(f)
        site_details = {rows[0]:rows[1:] for rows in reader}
        # print(site_details)

    for site_detail, detail in site_details.items():
        all_details[site_detail] = detail
        all_details[site_detail].append(mydict[site_detail][0])
        all_details[site_detail].append(mydict[site_detail][1])
            
    #print (all_details)
    new_details = {}
    header = ["", "URL", "Relevance", "Time_Of_Visit", "Content", "Keywords", "User_Id"]
    counter = 0    
    with open('data/input_file.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for key, value in all_details.items():
            det = []
            det.append(str(counter))
            det.append(key)
            det = det + value
            det.append("User_1")
            writer.writerow(det)
            counter = counter + 1

# merge_csv() 