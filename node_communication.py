import requests
import json

import asyncio
from websockets import connect
from multiprocessing import Process

from server_config import config as config
from main_server import best_moves_depth, best_moves_time


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

        info = []
        while True:
            await websocket.recv()
            async for message in websocket:
                info.append(message)
                print(message)
                if 'bestmove' in message:
                    print(info[-3:-1])
                    return info[-3:-1]


def talk(uri, number_moves, moves, tkn):
    asyncio.run(hello(uri, number_moves, moves, tkn))


def parallel_run(*ins):
    proc = []
    for p in ins:
        for pp in p:
            # p = Process(target=inn)
            pp.start()
            proc.append(pp)
    for p in proc:
        p.join()


def get_tokens(config):
    tokens = []
    for i in range(len(config['machine_ips'])):
        tkn = login(config, i)
        availableEngines(tkn, config, i)
        startEngine(tkn, config, i)
        tokens.append(tkn)
    return tokens


def just_run(tokens, config, bestmoves):
    best_moves_time(config['machines'] * 2, config['main_time'], config['start_pos'])

    nodes = []
    for item, (token, bmovess) in enumerate(zip(tokens, bestmoves)):
        nodes.append(Process(target=talk, args=(f"{config['socket_ips'][0]}/ws_engine", 2, config['start_pos'][item] + ' ' + bmovess, token)))

    parallel_run(nodes)


if __name__ == "__main__":
    best_moves = best_moves_depth(config['machines'], config['depth'], config['start_pos'])
    best_moves1 = [m['Move'] for m in reversed(best_moves)]
    print(best_moves)

    tokens = get_tokens(config)

    just_run(tokens, config, best_moves1)
