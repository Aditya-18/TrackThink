import pandas as pd

raw_data = {'URL': ['url1','url3','https://www.google.co.in/?gfe_rd=cr&dcr=0&ei=xmDLWvnnCeiK8QfOqqeIAg','https://www.google.co.in/?gfe_rd=cr&dcr=0&ei=xmDLWvnnCeiK8QfOqqeIAg','https://www.google.co.in/?gfe_rd=cr&dcr=0&ei=xmDLWvnnCeiK8QfOqqeIAg','url5'], 
        'User_Id': ['user1','user2','user3','user3','user1','user3'], 
        'Time_Of_Visit': ['t1','t1','t1','t3','t3','t2'], 
        'Content': ['abc zyx jfkdj kdlkdl','content2','content2','content3','content1','content3'],
        'Relevance':['1','2','2','1','3','3'],
        'Keywords':['a b','b c','d e','g t','a g','x y']
        }
df = pd.DataFrame(raw_data, columns = ['URL', 'User_Id', 'Time_Of_Visit', 'Content','Relevance','Keywords'])
#df.to_csv('input_file.csv')
print(df)

df=pd.read_csv('input_file.csv',encoding = "ISO-8859-1")
print(df)