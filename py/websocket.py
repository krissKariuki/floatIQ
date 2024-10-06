import asyncio
import websockets
import json
import random

async def send_data(websocket, path):
    while True:
        # Simulate data (you can replace this with your actual data)
        data = {
            "value": round(random.expovariate(2),2)
        }
        
        # Send data as JSON
        await websocket.send(json.dumps(data))
        
        # Wait for 1 second before sending the next data

        await asyncio.sleep(random.randint(1,5))

async def main():
    async with websockets.serve(send_data, "localhost", 6789):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())