import gym
import chess
import random
import numpy as np

FILE = "data.dump"

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

    def close(self):
        pass
    
    def dump(self):
        with open(FILE, "w") as file:
            file.write(self.board.fen())


alpha = 0.1
gamma = 0.9
epsilon = 0.1
Q = {}

def choose_action(state, legal_moves, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        return legal_moves[np.random.randint(len(legal_moves))].uci()
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

    while True:
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
        print(env.render())

        # Check if the game is finished
        if done:
            break

# Close the environment
env.close()
