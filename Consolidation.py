import numpy as np   
import pandas as pd
def trendline(data, order=1):
    coeffs = np.polyfit(data.index.values, list(data), order)
    slope = coeffs[-2]
    return float(slope)

StockDF = pd.read_csv("PreviousDaysStockData.csv")
StockDF.sort_values(['SYMBOL','TIMESTAMP'],inplace=True,ascending=[True, False])


uniqueValues = StockDF['SYMBOL'].unique()
#print(uniqueValues)

bearishstocks='BearishStocks.csv'
bullishstocks='BullishStocks.csv'

bullDF = pd.DataFrame()
bearDF=pd.DataFrame()
FirstBull=0
FirstBear=0
for eachSymbol in uniqueValues:
    
    #Df for a specific Symbol.
    curSymbolDF=StockDF[(StockDF.SYMBOL==eachSymbol)].sort_values('TIMESTAMP',inplace=False,ascending=True)
    if (curSymbolDF.count==5):
        print(curSymbolDF)
    else:
        print(curSymbolDF.count)
    '''
    slope = trendline(curSymbolDF['PIVOT'])
    if (abs(round(slope,1))<.1):
        continue
    else:
        if (slope>0):
            
            
            if (FirstBull==0):
                bullDF=curSymbolDF
                
                FirstBull+=1
                
            else:
                bullDF+=curSymbolDF
                
            
        else:
            if (FirstBear==0):
                bearDF=curSymbolDF
                
                FirstBear+=1
                
            else:
                bearDF+=curSymbolDF
        #print(curSymbolDF.head(10))
       # print(eachSymbol +' Trend is ')
        print(str(eachSymbol)+' '+str(slope))
        #counting+=1
        #if (counting>10): break
        '''
bearDF.to_csv(bearishstocks)
bullDF.to_csv(bullishstocks)




noofvalues=0
bullDF = pd.DataFrame()
bearDF=pd.DataFrame()

for eachSymbol in uniqueValues:
    
    #Df for a specific Symbol.
    curSymbolDF=StockDF[(StockDF.SYMBOL==eachSymbol)].sort_values('TIMESTAMP',inplace=False,ascending=True)
    #print(curSymbolDF)
    #if (noofvalues>5):
        #break
    if (curSymbolDF.shape[0]>=5):
        #print(curSymbolDF.shape[0])
        firstitemIndex=0
        firstitem=0
        lastitem=firstitem
        lastitemIndex=curSymbolDF.shape[0]-1
        #print(lastitemIndex)
        slope=0
        for eachitem in curSymbolDF['PIVOT']:
            #print(eachitem)
            if(firstitemIndex==0):  
                firstitem=eachitem
            if (firstitemIndex==lastitemIndex):
                lastitem=eachitem
            firstitemIndex=firstitemIndex+1
        slope=lastitem-firstitem
        if (slope>0):
            bullDF+=curSymbolDF
        else:
            bearDF+=curSymbolDF

        noofvalues+=1
bearDF.to_csv(bearishstocks)
bullDF.to_csv(bullishstocks)
