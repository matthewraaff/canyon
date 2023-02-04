# Canyon Chess Engine - Training Module

import chess
import chess.pgn
import chess.engine

import os
import yaml
import time

SAVE_DATA_FILE = "data/read.yaml"
SAVE_DATA_FILE = os.path.join(os.path.dirname(__file__), SAVE_DATA_FILE)

def create_data():
    """Go through all moves that can be done within the first 2 moves."""
    all_openings = []
    start_time = time.time()
    board = chess.Board()
    for move in board.legal_moves:
        board.push(move)
        for move2 in board.legal_moves:
            board.push(move2)
            all_openings.append(board.fen())
            board.pop()
        board.pop()
    print(f"Time taken: {time.time() - start_time}")
    return all_openings

def visualize_data():
    """Visualize the data."""
    with open(SAVE_DATA_FILE, "r") as file:
        all_openings = yaml.load(file, Loader=yaml.FullLoader)

    print(f"Total number of openings: {len(all_openings)}")

    for i in range(10):
        board = chess.Board(all_openings[i])
        print(board)
        print("=" * 15)

if __name__ == "__main__":
    all_openings = create_data()
    with open(SAVE_DATA_FILE, "w") as file:
        yaml.dump(all_openings, file)

    visualize_data()