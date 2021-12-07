from stockfish import Stockfish
import node_communication
import asyncio


def best_moves_depth(moves, depth):
    engine = Stockfish("C:/Users/wafel/Downloads/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe",
                       parameters={"MultiPV": moves})
    engine.set_depth(depth)
    return engine.get_top_moves(moves)


def best_moves_time(moves, time):
    engine = Stockfish("C:/Users/wafel/Downloads/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe",
                       parameters={"MultiPV": moves})
    return engine.get_top_moves_time(4, time=time)

best_moves = best_moves_time(2, 1000)
print(best_moves)

node_communication.login_and_run()
# node_communication.login_and_run2()