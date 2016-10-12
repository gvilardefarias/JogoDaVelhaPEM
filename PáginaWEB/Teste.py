from flask_socketio import send, SocketIO, emit
from flask import Flask, request

app = Flask(__name__)
socketio = SocketIO(app)

tabuleiro = [[0,0,0],
             [0,0,0],
             [0,0,0]]
@app.route('/jogar')
def recebeJogada():
    x = request.args.get('x')
    y = request.args.get('y')
    jogada = int(request.args.get('jogada'))
    print(x)
    print(y)
    print(jogada)

    tabuleiro[int(x)][int(y)] = jogada
    socketio.emit('NovaJogada',str(tabuleiro))
    return str(tabuleiro)

socketio.run(app, port=5005, debug=True)