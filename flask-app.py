from flask import Flask,request,jsonify
import stockfish
import chess
import json
app = Flask(__name__)

# fen = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'

@app.route('/score',methods=['POST'])
def score():
    data = request.data
    jsonData = json.loads(data)
    fen = jsonData['data']
    # print(fen)
    board = stockfish.fen2board(fen)
    score = stockfish.evaluation(board)
    return jsonify(isError= False,
                    message= "Success",
                    data=score,
                    statusCode= 200), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)