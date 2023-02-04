import chess
import random
import requests
import os

if not os.path.exists("temp_images"):
    os.makedirs("temp_images")

def FETCH_IMAGE_FOR_MOVE(string, i):
    r = requests.get(f"https://fen2image.chessvision.ai/{string}")
    with open(f"temp_images/{i}.png", "wb") as f:
        f.write(r.content)

def select_move(board):
    moves = list(board.legal_moves)
    best_move = moves[0]
    best_value = -9999
    
    for move in moves:
        board.push(move)
        value = -minimax(board, 3, -10000, 10000, True)
        board.pop()
        
        if value > best_value:
            best_value = value
            best_move = move
    
    return best_move

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizingPlayer:
        maxEval = -9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def evaluate_board(board):
    piece_map = board.piece_map()
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    return sum(piece_values.get(type(piece), 0) for piece in piece_map.values())

board = chess.Board()
i = 0
while not board.is_game_over():
    move = select_move(board)
    board.push(move)
    print(board.fen())
    FETCH_IMAGE_FOR_MOVE(board.fen(), i)
    i += 1
    print("=" * 15)

print(board.result())

# os.system("ffmpeg -framerate 1 -i temp_images/%d.png -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")