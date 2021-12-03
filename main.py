import requests
import json

import asyncio
from websockets import connect

from stockfish import Stockfish
stockfish = Stockfish("C:/Users/wafel/Downloads/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe",parameters={"MultiPV": 4})
# stockfish = Stockfish(parameters={"MultiPV": 4})
# stockfish.get_parameters()
stockfish.set_position(["e2e4"])
print(stockfish.get_top_moves(4))


# def login():
#     headers = {'Content-type': 'application/json'}
#     data = '{"login": "test", "password": "111111"}'
#     url = "http://192.168.56.108:8080/user/login"
#
#     response = requests.post(url, data=data, headers=headers)
#     print(response.text)
#     resp = json.loads(response.text)
#     return resp["token"]
#
#
# def availableEngines(token):
#     headers = {'Authorization': f'Bearer {token}'}
#     url = "http://192.168.56.108:8080/engine/available"
#
#     response = requests.get(url, headers=headers)
#     print(response.text)
#
#
# def startEngine(token):
#     headers = {'Authorization': f'Bearer {token}', 'Content-type': 'application/json'}
#     data = '{"engine" : "Stockfish"}'
#     url = "http://192.168.56.108:8080/engine/start"
#
#     response = requests.post(url, data=data, headers=headers)
#     print(response.text)
#     return response.text
#
# tkn = login()
# availableEngines(tkn)
# startEngine(tkn)
#
# moves = 4
#
# async def hello(uri):
#     async with connect(uri, extra_headers={"Authorization": f"Bearer {tkn}"}) as websocket:
#         await websocket.send("uci")
#         while True:
#             message = await websocket.recv()
#             print(message)
#             if message == 'uciok':
#                 break
#
#         await websocket.send(f"setoption name MultiPV value {moves}")
#         await websocket.send("isready")
#         while True:
#             print(message)
#             message = await websocket.recv()
#             if message == 'readyok':
#                 break
#
#         await websocket.send("ucinewgame")
#         await websocket.send("isready")
#         while True:
#             message = await websocket.recv()
#             print(message)
#             if message == 'readyok':
#                 break
#
#         await websocket.send("position startpos moves e2e4")
#         await websocket.send("go movetime 5000")
#
#         while True:
#             await websocket.recv()
#             async for message in websocket:
#                 print(message)
#
# asyncio.run(hello("ws://192.168.56.108:8080/ws_engine"))