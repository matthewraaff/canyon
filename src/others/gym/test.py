import gymnasium as gym
import chess
import random
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt

try:
    with open("q_table.pickle", "rb") as f:
        Q = pickle.load(f)
except:
    Q = {}

class ChessEnv(gym.Env):
    def __init__(self):
        self.board = chess.Board()

    def step(self, action):
        if action is None:
            return self.board.fen(), -10, True, {}
        move = chess.Move.from_uci(action)
        self.board.push(move)

        reward = 0
        done = False
        if self.board.is_checkmate():
            reward = -10
            done = True

        # if taken piece, reward
        if self.board.is_capture(move):
            # if queen, reward
            if self.board.piece_type_at(move.to_square) == 5:
                reward = 10
            # if rook, reward
            elif self.board.piece_type_at(move.to_square) == 4:
                reward = 5
            # if bishop, reward
            elif self.board.piece_type_at(move.to_square) == 3:
                reward = 3
            # if knight, reward
            elif self.board.piece_type_at(move.to_square) == 2:
                reward = 2
            # if pawn, reward
            elif self.board.piece_type_at(move.to_square) == 1:
                reward = 1


        return self.board.fen(), reward, done, {}

    def reset(self):
        self.board.reset()
        return self.board.fen()

    def render(self, mode='human'):
        if mode == 'human':
            print(self.board.unicode())
        elif mode == 'dog':
            print(self.board.unicode())
            time.sleep(2)
        else:
            pass

    def close(self):
        pass
    
    def dump(self):
        print(self.board.fen())


VISUALIT = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.1
Q = {}

def choose_action(state, legal_moves, epsilon):
    if len(list(legal_moves)) == 0:
        return None
    if np.random.uniform(0, 1) < epsilon:
        return list(legal_moves)[np.random.randint(len(list(legal_moves)))].uci()
    else:
        return max(legal_moves, key=lambda move: Q.get((state, move.uci()), 0)).uci()



# Create the environment
env = ChessEnv()

for episode in range(1000):
    # Reset the environment to start a new game
    obs = env.reset()

    # Choose the initial action
    legal_moves = env.board.legal_moves
    action = choose_action(obs, legal_moves, epsilon)

    steps = 0
    while True:
        steps += 1
        # Step the environment
        next_obs, reward, done, info = env.step(action)

        # Choose the next action
        next_legal_moves = env.board.legal_moves
        next_action = choose_action(next_obs, next_legal_moves, epsilon)

        # Update the Q-table
        Q[(obs, action)] = (1 - alpha) * Q.get((obs, action), 0) + alpha * (reward + gamma * Q.get((next_obs, next_action), 0))

        obs = next_obs
        action = next_action

        # Render the environment
        # print(env.render(mode='dogx'))

        # IF steps > 1000: make a piece do a random move
        if steps > 1000:
            print("Debug B", steps)
            # env.board.push(random.choice(list(env.board.legal_moves)))
            VISUALIT.update({env.board.fen(): Q.get((env.board.fen(), None), 0)})
            break

        # Check if the game is finished
        if done:
            print("Debug A", steps)
            break
    with open("q_table.pickle", "wb") as f:
        pickle.dump(Q, f)

# Close the environment
env.close()
