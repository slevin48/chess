import chess
import chess.pgn
import chess.engine

def fen2board(fen):
    board = chess.Board(fen)
    return board

def analysis(board, time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    engine.quit()
    return info

def evaluation(board, color='white', time_limit = 0.01):
    info = analysis(board, time_limit)
    if color == 'white':
        score = info['score'].white().score()
    else:
        score = info['score'].black().score()
    return score