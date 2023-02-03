import gym
import chess

class ChessEnv(gym.Env):
    def __init__(self):
        self.board = chess.Board()

    def step(self, action):
        move = chess.Move.from_uci(action)
        self.board.push(move)

        reward = 0
        done = False
        if self.board.is_checkmate():
            reward = -1
            done = True

        return self.board.fen(), reward, done, {}

    def reset(self):
        self.board.reset()
        return self.board.fen()

    def render(self, mode='human'):
        return self.board.unicode()

env = ChessEnv()
