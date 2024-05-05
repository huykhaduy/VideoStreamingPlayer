import asyncio
import time

import websockets
import multiprocessing


async def send_data_id(video_id):
    uri = "ws://localhost:8000/ws"  # replace with your server's URL
    async with websockets.connect(uri) as websocket:
        await websocket.send(video_id)
        while True:
            await asyncio.sleep(1)  # keep the client live


def run_client(video_id):
    asyncio.run(send_data_id(video_id))


client_thread = None


def start_socket():
    video_id = "your_video_id_993"  # replace with your video id
    global client_thread
    client_thread = multiprocessing.Process(target=run_client, args=(video_id,))
    client_thread.start()


def stop_socket():
    if client_thread is not None:
        client_thread.terminate()


start_socket()
time.sleep(2)
stop_socket()
