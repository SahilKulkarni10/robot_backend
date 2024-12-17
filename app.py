from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from datetime import datetime
import asyncio
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000", 
        "https://neon-beignet-8da367.netlify.app",
        "http://localhost:5173"
    ],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Robot Backend API!"}


try:
    with open("fake_robot_data.json", "r") as f:
        robot_data = json.load(f)
except FileNotFoundError:
    robot_data = []  


@app.get("/robots")
def get_robots():
    return robot_data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            for robot in robot_data:
             
                if robot.get("Battery Percentage", 100) == 0:
                    robot["Battery Percentage"] = 100  
                else:
                    
                    robot["Battery Percentage"] = max(
                        0, robot["Battery Percentage"] - random.randint(0, 5)
                    )

              
                robot["CPU Usage"] = random.randint(0, 100)
                robot["RAM Consumption"] = random.randint(500, 8000)
                robot["Location Coordinates"] = [
                    max(-90, min(90, robot["Location Coordinates"][0] + random.uniform(-0.01, 0.01))),
                    max(-180, min(180, robot["Location Coordinates"][1] + random.uniform(-0.01, 0.01))),
                ]
                robot["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      
            await websocket.send_json(robot_data)
            await asyncio.sleep(5)  
    except WebSocketDisconnect:
        print("WebSocket client disconnected.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
