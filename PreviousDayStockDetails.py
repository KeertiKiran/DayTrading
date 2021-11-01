import requests
import datetime     
import os
import zipfile
from datetime import date
from calendar import monthrange
import datetime     
import uuid
import pandas as pd
import os
import glob
from pathlib import Path
import shutil

NoOfPreviousDays=5

totcount=1
folderName=uuid.uuid4()

for intYears in range(date.today().year,date.today().year-1,-1):
    for intMonths in range(date.today().month,date.today().month-1,-1):
        for intDays in range(date.today().day,1,-1):
            dayvar=date(day=intDays, month=intMonths, year=intYears).strftime('%A')
            if (dayvar in ['Saturday','Sunday']):
                continue
            else:
                if (totcount>NoOfPreviousDays):
                    break;
                else:
                    
                    finalDate=datetime.date(intYears,intMonths,intDays)
                    YEAR=finalDate.strftime("%Y")
                    MONTH=finalDate.strftime("%b").upper()
                    DAY=finalDate.strftime("%d")
                    fileUrl="https://archives.nseindia.com/content/historical/EQUITIES/" + YEAR +"/"+MONTH+"/cm"+DAY+MONTH+YEAR+"bhav.csv.zip"
                    print(fileUrl)
                    try:
                        r = requests.get(fileUrl,timeout=3) # create HTTP response object
                        r.raise_for_status()
                        with open("temp.zip",'wb') as f:
                            f.write(r.content)                        
                        with zipfile.ZipFile("temp.zip", 'r') as zip_ref:
                            zip_ref.extractall(str(folderName))                    
                        os.remove("temp.zip")
                        print(YEAR +"/"+MONTH+"/cm"+DAY+MONTH+YEAR+"-Success")
                        totcount+=1
                    except requests.exceptions.HTTPError as err:
                        print(YEAR +"/"+MONTH+"/cm"+DAY+MONTH+YEAR+"-File Not Found")
                    except requests.exceptions.Timeout as errt:
                        print(YEAR +"/"+MONTH+"/cm"+DAY+MONTH+YEAR+"-File Not Found")
                    
data = pd.DataFrame()
data1=pd.DataFrame()
# use glob to get all the csv files 
# in the folder
path = os.getcwd()
csv_files = glob.glob(os.path.join(str(folderName), "*.csv"))
i=0
  
# loop over the list of csv files
for f in csv_files:
    
    if (i==0):
        data = pd.read_csv(f)
        
    else:
        data1=pd.read_csv(f)
        data=data.append(data1, ignore_index = True,sort=False)
    i=i+1
    print(data.describe)
    
data.to_csv(str(folderName)+'/Combined.csv')


pd.get_option("display.max_columns")
def extractDFfromFile(fileUrl):
    data = pd.read_csv(fileUrl)
    data = data.iloc[: , :-1]
    rslt_df = data[(data['SERIES'] == 'EQ')]
    #rslt_df = rslt_df[rslt_df['CLOSE'] > 100]
    #rslt_df = rslt_df[rslt_df['TOTTRDQTY'] > 100000]
    rslt_df['PIVOT']=(rslt_df['HIGH']+rslt_df['CLOSE']+rslt_df['LOW'])/3
    rslt_df['BC']=(rslt_df['HIGH']+rslt_df['LOW'])/2
    rslt_df['TC']=(rslt_df['PIVOT']-rslt_df['BC'])+rslt_df['PIVOT']
    rslt_df['TC-BC']=(rslt_df['TC']-rslt_df['BC']).round(2)
    rslt_df=rslt_df.drop(columns=['SERIES','PREVCLOSE','LAST','ISIN'])
    rslt_df=rslt_df[rslt_df['TC-BC'].between(-1,1)]
    rslt_df.sort_values('TOTALTRADES',inplace=True,ascending=False)
    return rslt_df

df=extractDFfromFile(str(folderName)+'/Combined.csv')
df.to_csv("PreviousDaysStockData.csv")
shutil.rmtree(str(folderName))
