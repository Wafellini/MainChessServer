from stockfish import Stockfish
import node_communication
import asyncio
from server_config import config as config


def best_moves_depth(moves, depth, start_pos):
    engine = Stockfish(config["engine_location"], parameters={"MultiPV": config['machines']})
    engine.set_depth(depth)
    engine.set_position(start_pos)
    return engine.get_top_moves(moves)


def best_moves_time(moves, time, start_pos):
    engine = Stockfish(config["engine_location"], parameters={"MultiPV": config['machines']})
    engine.set_position(start_pos)
    return engine.get_top_moves_time(moves, time=time)


best_moves = best_moves_depth(4, config['depth'], config['start_pos'])
best_moves1 = best_moves_depth(3, config['depth'], config['start_pos'])
best_moves2 = best_moves_depth(2, config['depth'], config['start_pos'])
# best_moves = best_moves_time(2, 3000)
print(best_moves)
print(best_moves1)
print(best_moves2)

# from multiprocessing import Process
# if __name__ == '__main__':
#     p1 = Process(target=node_communication.login_and_run2())
#     p1.start()
#     p2 = Process(target=node_communication.login_and_run3())
#     p2.start()
#     p1.join()
#     p2.join()
