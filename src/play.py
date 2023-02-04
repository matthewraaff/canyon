import os
import chess
import chess.pgn
import numpy as np
import pickle

# load the model from disk
def load_model():
    with open("model.pickle", "rb") as f:
        return pickle.load(f)

PLAYER = False

# convert board to feature vector
def board_to_input(board):
    input_vector = []
    for i in range(64):
        piece = board.piece_at(i)
        if piece is None:
            input_vector.append(0)
        else:
            input_vector.append(piece.piece_type + (piece.color * 6))
    return np.array(input_vector).reshape(1, -1)

# main function for playing against the AI
def play():
    model = load_model()
    board = chess.Board()
    while not board.is_game_over():
        print(board)
        
        
        if board.turn:
            legal = False
            while not legal:
                move = chess.Move.from_uci(input("Enter move (e.g. e2e4): "))
                if move not in board.legal_moves:
                    print("Invalid move. Try again.")
                else:
                    legal = True
            board.push(move)
        else:
            inputs = board_to_input(board)
            prediction = model.predict(inputs)[0]
            move = list(board.legal_moves)[prediction]
            print("AI move:", move)
            board.push(move)
    result = board.result()
    print("Result:", result)

if __name__ == "__main__":
    play()
