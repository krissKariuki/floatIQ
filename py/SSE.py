from flask import Flask,jsonify,Response
from flask_cors import CORS
from datetime import datetime
import time
import json
import threading

app=Flask(__name__)
CORS(app)

#global variables for access in separate functions
i=0
OPEN=0
HIGH=float('-inf')
LOW=float('inf')
CLOSE=0
DTTM=datetime.now().timestamp()
datapoint={}
datapoints=[]

#obtain data for simulation
sourceFilePath='../db/mozzart.json'
with open(sourceFilePath,'r') as sourceFile:
    sourceData=json.load(sourceFile)[::-1]

#execute function in background via separate thread
def THREAD(func,*args):
    thread=threading.Thread(target=func,args=args)
    thread.daemon=True
    thread.start()
    
#execute function endlessly
def executeInfinitely(func,*args):
    while True:
        func(*args)
        time.sleep(1)
        
#stream newest data to endpoint via SSE
def eventStream():
    global datapoint
    while True:
        yield f"data:{json.dumps(datapoint)}\n\n"
        time.sleep(1)

#create & update global variables
def processor(token=2,timeframe='second',interval=5):
    global i,OPEN,HIGH,LOW,CLOSE,DTTM,datapoint,datapoints
    
    #dict to enable timeframe input from current function
    timeframeMap={
        'second':lambda T:datetime.now().second%T==0,
        
        'minute':lambda T:datetime.now().minute%T==0 and datetime.now().second==0,
        
        'hour':lambda T:datetime.now().hour%T==0 and datetime.now().second==0
    }
    
    #variable to check for a desired time to run an update
    timeCheck=timeframeMap[timeframe](interval)
    
    M=sourceData[i][0]
    
    if M>token:
        CLOSE+=token-1
    else :
        CLOSE-=1
    
    #set high and low
    HIGH=max(OPEN,HIGH,CLOSE)
    LOW=min(OPEN,LOW,CLOSE)
    
    #modify datapoint object with new data
    datapoint={'time':DTTM,'open':OPEN,'high':HIGH,'low':LOW,'close':CLOSE}
    i+=1
    
    #check whether it is time to update variables
    if timeCheck:
        DTTM=datetime.now().timestamp()
        OPEN=CLOSE
        HIGH=float('-inf')
        LOW=float('inf')
        
        datapoints.append(datapoint)
    
    return datapoint
    
#live data endpoint
@app.route('/floatIQ/stream/datapoint')
def liveDatapoint():
    return Response(eventStream(),content_type='text/event-stream')
    
#datapoints array endpoint
@app.route('/floatIQ/fetch/datapoints')
def fetchDatapoints():
    return jsonify(datapoints)

if __name__=='__main__':
    
    # run the processor function endlessly in the background in separate thread
    THREAD(executeInfinitely,processor,15,'minute',15)
    
    #run the application
    app.run(debug=True,host='localhost',port=8000)