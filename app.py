# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# import json
# import random
# from datetime import datetime
# import asyncio
# import uvicorn

# app = FastAPI()

# # Middleware for CORS (allows the frontend to access the backend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (for testing, change for production)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load initial robot data from the JSON file
# with open("fake_robot_data.json", "r") as f:
#     robot_data = json.load(f)

# # Endpoint to get robots
# @app.get("/robots")
# def get_robots():
#     return robot_data

# # WebSocket for real-time updates
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Simulate changes in robot data
#             for robot in robot_data:
#                 # Ensure the 'Battery Percentage' key exists, and update it
#                 if "Battery Percentage" not in robot:
#                     robot["Battery Percentage"] = 100  # Set a default value if missing
                
#                 robot["Battery Percentage"] = max(0, robot["Battery Percentage"] - random.randint(0, 5))

#                 # Update other parameters
#                 robot["CPU Usage"] = random.randint(0, 100)
#                 robot["RAM Consumption"] = random.randint(500, 8000)
#                 robot["Location Coordinates"] = [
#                     max(-90, min(90, robot["Location Coordinates"][0] + random.uniform(-0.01, 0.01))),
#                     max(-180, min(180, robot["Location Coordinates"][1] + random.uniform(-0.01, 0.01))),
#                 ]
#                 robot["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Log robot data to check if the Battery Percentage is updated correctly
#             print(robot_data)  # This will log the data every 5 seconds to verify the update

#             # Send updated robot data to the WebSocket client
#             await websocket.send_json(robot_data)

#             # Delay to simulate periodic updates
#             await asyncio.sleep(5)

#     except WebSocketDisconnect:
#         print("Client disconnected")

# # Run the application with Uvicorn when executed directly
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from datetime import datetime
import asyncio
import uvicorn

app = FastAPI()

# Middleware for CORS (allows the frontend to access the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing, change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Robot Backend API!"}

# Load initial robot data from the JSON file
with open("fake_robot_data.json", "r") as f:
    robot_data = json.load(f)

# Endpoint to get robots
@app.get("/robots")
def get_robots():
    return robot_data

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate changes in robot data
            for robot in robot_data:
                # Ensure the 'Battery Percentage' key exists, and update it
                if "Battery Percentage" not in robot:
                    robot["Battery Percentage"] = 100  # Set a default value if missing
                
                robot["Battery Percentage"] = max(0, robot["Battery Percentage"] - random.randint(0, 5))

                # Update other parameters
                robot["CPU Usage"] = random.randint(0, 100)
                robot["RAM Consumption"] = random.randint(500, 8000)
                robot["Location Coordinates"] = [
                    max(-90, min(90, robot["Location Coordinates"][0] + random.uniform(-0.01, 0.01))),
                    max(-180, min(180, robot["Location Coordinates"][1] + random.uniform(-0.01, 0.01))),
                ]
                robot["Last Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log robot data to check if the Battery Percentage is updated correctly
            print(robot_data)  # This will log the data every 5 seconds to verify the update

            # Send updated robot data to the WebSocket client
            await websocket.send_json(robot_data)

            # Delay to simulate periodic updates
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("Client disconnected")

# Run the application with Uvicorn when executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
