import requests
import json

import asyncio
from websockets import connect

from server_config import config as config


def login(config, machine):
    headers = {'Content-type': 'application/json'}
    data = '{"login": "test", "password": "111111"}'
    url = f"{config['machine_ips'][machine]}/user/login"

    response = requests.post(url, data=data, headers=headers)
    print(response.text)
    resp = json.loads(response.text)
    return resp["token"]


def availableEngines(token, config, machine):
    headers = {'Authorization': f'Bearer {token}'}
    url = f"{config['machine_ips'][machine]}/engine/available"

    response = requests.get(url, headers=headers)
    print(response.text)


def startEngine(token, config, machine):
    headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
    data = '{"engine" : "Stockfish"}'
    url = f"{config['machine_ips'][machine]}/engine/start"

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
    tkn = login(config, 0)
    availableEngines(tkn, config, 0)
    startEngine(tkn, config, 0)

    num_of_moves = 4
    asyncio.run(hello(f"{config['socket_ips'][0]}/ws_engine", num_of_moves, moves, tkn))

login_and_run(config['start_pos'][0])
