from stockfish import Stockfish
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

#todo moze wszystkie dostepne ruchy i multipv na dostepnych kompach?
if __name__ == "__main__":
    best_moves = best_moves_depth(config['machines'] * 2, config['depth'], config['start_pos'])

    print(best_moves)
