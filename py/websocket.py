from flask import Flask,Response
from flask_cors import CORS
from datetime import datetime,timedelta
import json
import time
import random

app=Flask(__name__)
CORS(app)


sourceDataFile='../db/mozzart.json'

with open(sourceDataFile,'r') as sdf:
    sourceData=json.load(sdf)[::-1]

i=0
OPEN=0
HIGH=float('-inf')
LOW=float('inf')
CLOSE=0
DTTM=datetime.now().timestamp()
    
datapoint={}

def source(token=2):
    global i,OPEN,HIGH,LOW,CLOSE,DTTM,datapoint
    while True:
        
        M=sourceData[i][0]
        
        if M>token:CLOSE+=token-1
        
        else:CLOSE-=1
        
        HIGH=max(OPEN,HIGH,CLOSE)
        LOW=min(OPEN,LOW,CLOSE)
        
        datapoint={'open':OPEN,'high':HIGH,'low':LOW,'close':CLOSE,'time':DTTM}
        
        yield f'data:{json.dumps(datapoint)}\n\n'
        
        OPEN=CLOSE
        HIGH=float('-inf')
        LOW=float('inf')
        
        time.sleep(1)
        
        
@app.route('/floatIQ/stream/datapoint')
def liveDatapoint():
    return Response(source(),content_type='text/event-stream')
    
if __name__=='__main__':
    app.run(debug=True,port=8000)