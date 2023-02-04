import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# Load the game
import chess
import chess.pgn
import numpy as np
import pickle

# load the model from disk
def load_model():
    with open("model.pickle", "rb") as f:
        return pickle.load(f)

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
    
class ChessGame:
    def __init__(self, master):
        self.master = master
        master.title("Chess Game")

        self.board = chess.Board()
        self.model = load_model()

        r = requests.get("https://fen2image.chessvision.ai/" + self.board.fen())
        with open("TEMP/fen.png", "wb") as f:
            f.write(r.content)

        self.board_image = PhotoImage(file="TEMP/fen.png")
        self.board_image_label = Label(master, image=self.board_image)
        self.board_image_label.grid(row=0, column=0, columnspan=2)

        self.move_entry = Entry(master)
        self.move_entry.grid(row=1, column=0)

        self.move_button = Button(master, text="Make Move", command=self.make_move)
        self.move_button.grid(row=1, column=1)

        self.update_board()

    def make_move(self):
        move = self.move_entry.get()
        if move not in [str(m) for m in self.board.legal_moves]:
            messagebox.showerror("Invalid Move", "The move you entered is invalid. Please try again.")
        else:
            self.board.push(chess.Move.from_uci(move))
            self.update_board()
            if not self.board.is_game_over():
                inputs = board_to_input(self.board)
                prediction = self.model.predict(inputs)[0]
                move = list(self.board.legal_moves)[prediction]
                self.board.push(move)
                self.update_board()
                if self.board.is_game_over():
                    messagebox.showinfo("Game Over", self.board.result())

    def update_board(self):

        r = requests.get("https://fen2image.chessvision.ai/" + self.board.fen())
        with open("TEMP/fen.png", "wb") as f:
            f.write(r.content)

        self.board_image = PhotoImage(file="TEMP/fen.png")
        self.board_image_label.configure(image=self.board_image)
        self.board_image_label.image = self.board_image

root = Tk()
my_gui = ChessGame(root)
root.mainloop()
