from flask import Flask,jsonify,Response
from flask_cors import CORS
from datetime import datetime,timedelta
import time
import json
import random
import threading

app=Flask(__name__)
CORS(app)

#________________utility functions_________________

#running tasks concurrently
def THREAD(func,*args):
    thread=threading.Thread(target=func,args=(args))
    thread.daemon=True
    thread.start()
    
#run task endlessly at specified time intervals
def exeiter(func,interval=1):
    
    timeBasis=lambda T:T.second
    
    def timeToUpdate(t):
       return timeBasis(t)%interval==0
    
    while True:
        timeNow=datetime.now()
        
        if timeToUpdate(timeNow):func()
            
        time.sleep(1)

#source of data stream
sourceData='../db/mozzart.json'

with open(sourceData,'r') as rawData:
    rawData=json.load(rawData)[::-1]

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
def bgProcess(func):
    while True:
        yield f'{json.dumps(func())}\n\n'
        time.sleep(1)
        
def source(token=3):
    global i,HIGH,LOW,CLOSE,DTTM,datapoint
    
    M=rawData[i][0]
    token=round(random.expovariate(1/M),2)
    if M>token:CLOSE+=token-1
    else:CLOSE-=1
    
    HIGH=max(OPEN,HIGH,CLOSE)
    LOW=min(OPEN,LOW,CLOSE)
    
    datapoint={'time':DTTM,'open':round(OPEN,2),'high':round(HIGH,2),'low':round(LOW,2),'close':round(CLOSE,2)}
    
    return datapoint
    

#update data after specified time interval
def feed():
    global OPEN,HIGH,LOW,CLOSE,DTTM,datapoint,datapoints
    
    DTTM=datetime.now().timestamp()

    datapoints.append(datapoint)
    
    OPEN=CLOSE
    HIGH=float('-inf')
    LOW=float('inf')
    
    return datapoints
    

#tokens data extraction
fmt='../db/format_1.1.json'
with open(fmt,'r') as FMT:
    FORMAT=json.load(FMT)['tokens']


#tokens
@app.route('/floatIQ/tokens')
def tokens():
    return jsonify(FORMAT)
    
#single data points
@app.route('/floatIQ/stream/datapoint')
def liveDatapoint():
    return Response(bgProcess(source),content_type='text/event-stream')

#entire array of datapoints
@app.route('/floatIQ/stream/datapoints')
def liveDatapoints():
    return Response(bgProcess(feed),content_type='text/event-stream')


#__________inititalize background processes________
THREAD(exeiter,source)
THREAD(exeiter,feed,5)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)