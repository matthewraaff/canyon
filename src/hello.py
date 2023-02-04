import os
import chess
import chess.pgn
import numpy as np
from sklearn.neural_network import MLPClassifier
import io, pickle

# load PGN files in GAMES directory
def load_pgn_games():
    games = []
    cap = 10
    for filename in os.listdir("GAMES"):
        if cap == 0:
            break
        with open(f"GAMES/{filename}") as f:
            cap -= 1
            print(f"Loading {filename}...")
            pgn = f.read()
            end = pgn.rfind("1-0")
            if end == -1:
                end = pgn.rfind("0-1")
                if end == -1:
                    end = pgn.rfind("1/2-1/2")
                if end == -1:
                    continue
            pgn = pgn[:end+4]
            games.append(chess.pgn.read_game(io.StringIO(pgn)))
    return games

# convert board to feature vector
def board_to_input(board):
    input_vector = []
    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            input_vector.append(0)
        else:
            input_vector.append(piece.piece_type + (piece.color * 6))
    return np.array(input_vector)

# extract input/output data from games
def get_training_data(games):
    inputs = []
    outputs = []
    for game in games:
        node = game
        while node.variations:
            node = node.variation(0)
            inputs.append(board_to_input(node.board()))
            outputs.append(node.board().turn)
    return (inputs, outputs)

# train model on extracted data
def train_model(inputs, outputs):
    clf = MLPClassifier(hidden_layer_sizes=(64, 64), max_iter=10000)
    clf.fit(inputs, outputs)
    return clf

# main function
def main():
    games = load_pgn_games()
    inputs, outputs = get_training_data(games)
    model = train_model(inputs, outputs)
    return model

if __name__ == "__main__":
    model = main()
    with open("model.pickle", "wb") as f:
        pickle.dump(model, f)
