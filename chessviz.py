import numpy as np

def fentotensor(inputstr):
    pieces_str = "PNBRQK"
    pieces_str += pieces_str.lower()
    pieces = set(pieces_str)
    valid_spaces = set(range(1,9))
    pieces_dict = {pieces_str[0]:1, pieces_str[1]:2, pieces_str[2]:3, pieces_str[3]:4 , 
                    pieces_str[4]:5, pieces_str[5]:6,
                    pieces_str[6]:-1, pieces_str[7]:-2, pieces_str[8]:-3, pieces_str[9]:-4, 
                    pieces_str[10]:-5, pieces_str[11]:-6}

    boardtensor = np.zeros((8,8,6))
    
    inputliste = inputstr.split()
    rownr = 0
    colnr = 0
    for i, c in enumerate(inputliste[0]):
        if c in pieces:
            boardtensor[rownr, colnr, np.abs(pieces_dict[c])-1] = np.sign(pieces_dict[c])
            colnr = colnr + 1
        elif c == '/':  # new row
            rownr = rownr + 1
            colnr = 0
        elif int(c) in valid_spaces:
            colnr = colnr + int(c)
        else:
            raise ValueError("invalid fenstr at index: {} char: {}".format(i, c))
  
    return boardtensor


def countpieces(fen):
    boardtensor = fentotensor(fen)
    count = np.sum(np.abs(boardtensor))
    return count  

def pawnending(fen):
    boardtensor = fentotensor(fen)
    counts = np.sum(np.abs(boardtensor), axis = (0,1))
    if counts[1]==0 and counts[2]==0 and counts[3]==0 and counts[4]==0:
        return True
    else:
        return False
        
def rookending(fen):
    boardtensor = fentotensor(fen)
    counts = np.sum(np.abs(boardtensor), axis = (0,1))
    if  counts[1]==0 and counts[2]==0 and counts[4]==0 and counts[3]>0:
        return True
    else:
        return False

import chess.uci

def count(act_game):
    
    engine = chess.uci.popen_engine("stockfish_20090216_x64.exe")
    engine.uci()
    # Register a standard info handler.
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)
    counts ={"movecount":[],"scores":[],"check":[],"bestdiff":[],"pawnending":[],"rookending":[]}
    
    # Iterate through all moves and play them on a board.
    board = act_game.board()
    for move in act_game.main_line():
        board.push(move)
        cnt = len([i for i in board.legal_moves])
        counts["movecount"].append(cnt)
        counts["check"].append(board.is_check())
        counts["pawnending"].append(pawnending(board.fen()))
        counts["rookending"].append(rookending(board.fen()))
        
        # Start a search.
        engine.position(board)
        engine.go(movetime=100)
        if board.turn == chess.WHITE:
            counts["scores"].append(info_handler.info["score"][1][0])
        else:
            counts["scores"].append(-info_handler.info["score"][1][0])
        nextmovescores = []
        
        for mov in board.legal_moves:
            board.push(mov)
            engine.position(board)
            engine.go(movetime=100)
            if board.turn == chess.WHITE:
                if info_handler.info["score"][1][0] != None:
                    nextmovescores.append(info_handler.info["score"][1][0])
            elif board.turn == chess.BLACK:
                if info_handler.info["score"][1][0] != None:
                    nextmovescores.append(-info_handler.info["score"][1][0]) 
            board.pop()

        if len(nextmovescores) > 1:
            nextmovescores.sort(reverse=True)
            counts["bestdiff"].append(nextmovescores[0]-nextmovescores[1])
        else:
            counts["bestdiff"].append(0) 
    
    return counts

import chart_studio.plotly as py
import plotly.graph_objs as go

def plot(count,game):
    checkcolor = ['red' if i else 'white' for i in counts["check"]]
    checknr = [i for (i,s) in enumerate(counts["check"]) if s]
    bubble = [s/2 for s in counts["movecount"]]
    best = [np.log(s+1) for s in counts["bestdiff"]]

    rookcolor = ['blue' if i else 'white' for i in counts["rookending"]]
    pawncolor = ['green' if i else 'white' for i in counts["pawnending"]]

    # We prepare lists of shapes to show the different phases of the game and if the king is in check.
    shapes= []
    lists =[checkcolor, rookcolor, pawncolor]
    for (i,list) in enumerate(lists):
        shapes = shapes + [
                dict(
                        type = 'rect',
                        # x-reference is assigned to the x-values
                        xref = 'x',
                        # y-reference is assigned to the plot paper [0,1]
                        yref = 'paper',
                        x0 = i,
                        y0 = 0,
                        x1 = i+1,
                        y1 = 1,
                        fillcolor = s,
                        opacity = 0.2,
                        line = dict(
                            width = 0,
                        )
                    )
                    for (i,s) in enumerate(list)]
    
    annotations = [ dict(
                    xref = 'x',
                    yref = 'paper',
                    x = s,
                    y = (0.05 + i*0.2) % 1,
                    text = 'Check!',
                    opacity = 0.8,
                    xanchor = 'left',
                    showarrow = False,
                    ax = 20,
                    ay = -30,
                    font = dict(
                        family = 'Courier New, monospace',
                        size = 16,
                        color = 'red'
                    ),
                )
                for (i,s) in enumerate(checknr)]
    
    trace1 = go.Scatter(
        mode = 'markers+lines',
        y = counts["scores"],
        name = 'Scores',
        
        line = dict(
            color = ('black'),
            width = 4,
        ),
        marker = dict(
            size = bubble,
            line = dict(color = 'rgb(231, 99, 250)',width = 1),
            cmax=max(best),
            cmin=min(best),
            color=best,
            colorbar=dict(title='Critical Move'),
            colorscale='Jet'
        )
    )


    data = [trace1]

    layout = dict(title = game.headers["Event"] + " / " + game.headers["White"] + " - " 
                + game.headers["Black"] + "  " + game.headers["Result"] + " / " 
                + game.headers["Date"],
                xaxis = dict(title = 'Move'),
                yaxis = dict(title = 'Score'),
                shapes = shapes,
                annotations = annotations
            )

    fig = {
        'data': data,
        'layout': layout,
    }

    return py.iplot(fig, filename = 'chessviz')