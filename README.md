# Chess [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/slevin48/chess/main/chess-app.py)

Analyzing chess games and rendering as a [web app](https://share.streamlit.io/slevin48/chess/main/chess-app.py)

![game1](images/game1.svg)

Match plot:

![matchplot](images/matchplot.png)

## Stockfish

[Stockfish](https://stockfishchess.org/) is an open source chess engine

```python
import chess
import chess.pgn
import chess.engine

def stockfish_evaluation(board, color='white', time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    if color == 'white':
        score = info['score'].white().score()
    else:
        score = info['score'].black().score()
    engine.quit()
    return score

pgn = open('games/slevin48_vs_GraciasSenior_2020.11.22.pgn')
first_game = chess.pgn.read_game(pgn)

# Move 48
board = first_game.board()
moves = [move for move in first_game.mainline_moves()]

# Iterate through all moves and play them on a board
for move in moves[0:48]:
    board.push(move)
result = stockfish_evaluation(board)
print(result)
```

[Analysing and evaluating a position](https://python-chess.readthedocs.io/en/latest/engine.html#analysing-and-evaluating-a-position):

```python
import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
info = engine.analyse(board, chess.engine.Limit(depth=20))
print("Score:", info["score"])
# Score: PovScore(Mate(+1), WHITE)

engine.quit()
```

It enables to perform analysis plots of the match

![matchplot](images/matplot.png)


## Stockfish on demand

🐋[Dockerfile](Dockerfile) installing Stockfish + Python Chess library, exposing analysis as a REST API:

```
docker build -t chess-engine .
docker run -p 5000:5000 chess-engine
```
(run command can also be detached: `--detach` , `-d`)

```
curl http://localhost:5000/score -d '{"data":"rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"}' -X POST -v -H "Content-Type: application/json"
```
(unnecessary use of `-X POST` and of optional use of `-v` for verbose output)

🚀*Deploy to Heroku* 
[Dockerize Your Python Flask application and deploy it onto Heroku](https://medium.com/analytics-vidhya/dockerize-your-python-flask-application-and-deploy-it-onto-heroku-650b7a605cc9)
```
$ curl https://stockfish48.herokuapp.com/score -d '{"data":"rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"}' -H "Content-Type: application/json"
{
  "data": 40, 
  "isError": false, 
  "message": "Success", 
  "statusCode": 200
}
```
## AlphaZero

Mentally play through possible future scenarios, giving priority to promising paths, whilst also considering how others are most likely to react to your actions and continuing to explore the unknown.

After reaching a state that is unfamiliar, evaluate how favourable you believe the position to be and cascade the score back through previous positions in the mental pathway that led to this point.

After you’ve finished thinking about future possibilities, take the action that you’ve explored the most.

At the end of the game, go back and evaluate where you misjudged the value of the future positions and update your understanding accordingly.

[How to build your own AlphaZero AI using Python and Keras
](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188)

## AlphaZero vs Stockfish

![AlphaZeroVsStockfish](images/AlphaZeroVsStockfish.jpeg)

![AlphaZeroVsStockfishGame](images/AlphaZeroVsStockfishGame.png)

## Resources

Code:
* [Python-chess](https://github.com/niklasf/python-chess) + ([Doc](https://python-chess.readthedocs.io/en/latest/))
* [Programming a Chess Player](https://jupyter.brynmawr.edu/services/public/dblank/CS371%20Cognitive%20Science/2016-Fall/Programming%20a%20Chess%20Player.ipynb)
* [Deep Pink](https://github.com/erikbern/deep-pink)
* [Chess annotator](https://pypi.org/project/chess-annotator/)
* [python-chess-analysis](https://github.com/mptedesco/python-chess-analysis)
* [Chess-Graphical-Evaluation](https://github.com/rafaelmcam/Chess-Graphical-Evaluation)
* [Python-Easy-Chess-GUI](https://github.com/fsmosca/Python-Easy-Chess-GUI)
* [Chess analysis D3js](https://github.com/m-hou/Chess-Analysis)
* [Python chess graph](https://github.com/Destaq/chess_graph)
* [Chess web app](https://github.com/SayonB/Predicting-Pro-Chess-Moves)

Articles:
* [Using Deep Learning to train a Deep Search Chess Algorithm](https://towardsdatascience.com/creating-a-chess-engine-with-deep-learning-b9477ff3ee3d)
* [How to build your own AlphaZero AI using Python and Keras
](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188)
* [Analyzing Chess with Pandas to Learn from the Best and Raise My Rating](https://medium.com/@crawftv/analyzing-chess-with-pandas-to-learn-from-the-best-raise-my-rating-1bf22f28b83)
* [Modeling a ChessBoard And Mechanics Of Its Pieces In Python](https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/amp/)
* [A Visual Look at 2 Million Chess Games](https://blog.ebemunk.com/a-visual-look-at-2-million-chess-games/)
* [Chessviz](https://andreasstckl.medium.com/chessviz-graphs-of-chess-games-7ebd4f85a9b9)
* [Machine Learning for Chess — AlphaZero vs Stockfish](https://mmsubra1.medium.com/machine-learning-for-chess-alphazero-vs-stockfish-b58638e73fee)
* [AlphaZero Crushes Stockfish In New 1,000-Game Match](https://www.chess.com/news/view/updated-alphazero-crushes-stockfish-in-new-1-000-game-match)
* [Predicting Professional Players’ Chess Moves with Deep Learning](https://towardsdatascience.com/predicting-professional-players-chess-moves-with-deep-learning-9de6e305109e)
