import streamlit as st
import chess
import chess.pgn
import chess.svg
import base64
import os

files = os.listdir('games')
file = st.selectbox('Select game',files)
pgn = open('games/'+file)

game = chess.pgn.read_game(pgn)
st.title(game.headers["White"]+" vs "+game.headers["Black"])
# st.write(game.headers["Link"])

board = game.board()
moves = [move for move in game.mainline_moves()]
mv = st.slider("Move",0,len(moves),len(moves))

for move in moves[0:mv]:
    board.push(move)

# for move in game.mainline_moves():
#     board.push(move)

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

render_svg(chess.svg.board(board))