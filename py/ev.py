'''
import json
import datetime
import random

sourceFile='../db/mozzart.json'
with open(sourceFile,'r') as sourceData:
    data=json.load(sourceData)[::-1][:1000]


def processor(token=2):
    price=0
    stake=5
    MULT=0
    DTTM=datetime.datetime.now()
    
    #Expected Round Return
    returnPerRound=0
    wins=0
    prob=0
    rounds=len(data)
    
    for i in range(len(data)):
        MULT=data[i][0]
        DTTM=data[i][1]
        
        if MULT>token:
            price+=(stake*token)-stake
            wins+=1
        else:
            price-=stake
        
        prob=wins/rounds
        returnPerRound=(((token-1)*prob)-(1-prob))
        
    return {'price':round(price,2),'returnPerRound':round(returnPerRound,4),'wins':round(wins,2),'probability':round(prob,4)}
        
print(processor(1.01))
'''
import json
from flask import Flask,jsonify

app=Flask(__name__)

formatFile='../db/format.json'
with open(formatFile,'r') as formatData:
    FORMAT=json.load(formatData)
    

@app.route('/floatIQ/data/tokens')
def avaliableTokens():
    return jsonify(FORMAT['tokens'])
    
for unit in FORMAT['timeFrames']:
    timeUrl=f"/floatIQ/data/{unit}"
    for tokenName,tokenObject in FORMAT['tokens'].items():
        URL=f"{timeUrl}/{tokenObject['abbr']}"
        app.add_url_rule(URL,endpoint=URL,view_func=lambda res=URL:res)
if __name__=='__main__':
    app.run(debug=True,port=8080)