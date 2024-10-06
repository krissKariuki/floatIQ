from flask import Flask,jsonify
from flask_cors import CORS
from datetime import datetime,timedelta
import time
import json
import threading

app=Flask(__name__)
CORS(app)

#________________utility functions_________________

#running tasks concurrently
def thread(func,*args):
    threading.Thread(target=func,args=(args)).start()
    
#run task endlessly at specified time intervals
def exeiter(func,sleep=1,interval=1):
    
    timeBasis=lambda T:T.minute
    
    def timeToUpdate(t):
       return timeBasis(t)%interval==0
    
    while True:
        timeNow=datetime.now()
        
        if timeToUpdate(timeNow):func()
            
        time.sleep(sleep)

#source of data stream
sourceData='../db/mozzart.json'

with open(sourceData,'r') as rawData:
    rawData=json.load(rawData)

#fundamental variables
i=0
OPEN=0
HIGH=float('-inf')
LOW=float('inf')
CLOSE=0
DTTM=datetime.now().timestamp()

FORMAT={}
datapoint={}
datapoints=[]

#produce processed data in the background endlessly 
def source(token=65):
    global i,HIGH,LOW,CLOSE,DTTM,datapoint
    
    M=rawData[i][0]
    
    if M>token:CLOSE+=token-1
    else:CLOSE-=1
    
    HIGH=max(OPEN,HIGH,CLOSE)
    LOW=min(OPEN,LOW,CLOSE)
    
    datapoint={'time':DTTM,'open':OPEN,'high':HIGH,'low':LOW,'close':CLOSE}

    if i>=len(rawData):i=0
    i+=1

#update data after specified time interval
def feed():
    global OPEN,HIGH,LOW,CLOSE,DTTM,datapoint,datapoints
    
    DTTM=datetime.now().timestamp()

    datapoints.append(datapoint)
    
    OPEN=CLOSE
    HIGH=float('-inf')
    LOW=float('inf')
    

#tokens data extraction
fmt='../db/format_1.1.json'
with open(fmt,'r') as FMT:
    FORMAT=json.load(FMT)['tokens']


#tokens
@app.route('/floatIQ/tokens')
def tokens():
    return jsonify(FORMAT)
    
#single data points
@app.route('/floatIQ/live-data/datapoint')
def liveDatapoint():
    return jsonify(datapoint)

#entire array of datapoints
@app.route('/floatIQ/live-data/datapoints')
def liveDatapoints():
    return jsonify(datapoints)


#__________inititalize background processes________
thread(exeiter,source)
thread(exeiter,feed,60,15)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)