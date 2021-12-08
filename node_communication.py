import requests
import json

import asyncio
from websockets import connect


def login():
    headers = {'Content-type': 'application/json'}
    data = '{"login": "test", "password": "111111"}'
    url = "http://192.168.56.108:8080/user/login"

    response = requests.post(url, data=data, headers=headers)
    print(response.text)
    resp = json.loads(response.text)
    return resp["token"]


def availableEngines(token):
    headers = {'Authorization': f'Bearer {token}'}
    url = "http://192.168.56.108:8080/engine/available"

    response = requests.get(url, headers=headers)
    print(response.text)


def startEngine(token):
    headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
    data = '{"engine" : "Stockfish"}'
    url = "http://192.168.56.108:8080/engine/start"

    response = requests.post(url, data=data, headers=headers)
    print(response.text)
    return response.text


async def hello(uri, number_moves, moves, tkn):
    async with connect(uri, extra_headers={"Authorization": f"Bearer {tkn}"}) as websocket:
        await websocket.send("uci")
        while True:
            message = await websocket.recv()
            print(message)
            if message == 'uciok':
                break

        await websocket.send(f"setoption name MultiPV value {number_moves}")
        await websocket.send("isready")
        while True:
            print(message)
            message = await websocket.recv()
            if message == 'readyok':
                break

        await websocket.send("ucinewgame")
        await websocket.send("isready")
        while True:
            message = await websocket.recv()
            print(message)
            if message == 'readyok':
                break

        await websocket.send(f"position startpos moves {moves}")
        await websocket.send("go movetime 5000")

        while True:
            await websocket.recv()
            async for message in websocket:
                print(message)


def login_and_run(moves):
    tkn = login()
    availableEngines(tkn)
    startEngine(tkn)

    num_of_moves = 4
    asyncio.run(hello("ws://192.168.56.108:8080/ws_engine", num_of_moves, moves, tkn))

def login_and_run2():
    tkn = login()
    availableEngines(tkn)
    startEngine(tkn)

    moves = 4
    asyncio.run(hello("ws://192.168.56.108:8081/ws_engine", moves, tkn))