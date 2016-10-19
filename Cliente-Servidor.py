from flask_socketio import send, SocketIO, emit
from flask import Flask, request
from flask_cors import CORS, cross_origin
from random import randint
import requests
import Nucleo

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

tabuleiro = [[0,0,0],
             [0,0,0],
             [0,0,0]]

ipAdversario = False
minhaJogada = 0
jogadaAdversario = 0
myPort = 5000

@app.route("/temVencedor", methods = ['POST'])
def temVencedor():
    tabuleiro = request.json
    return str(Nucleo.verificarVencedor(tabuleiro, ''))

@app.route("/setIPByServer/<port>")
def setIPByServer(port):
    global ipAdversario, minhaJogada, jogadaAdversario

    if not ipAdversario:
        jogadaAdversario = request.args.get("jogada")
        minhaJogada = 3-jogadaAdversario

        ipAdversario = request.remote_addr + ":" + str(port)

        return "S"

    return "N"

@app.route("/setIPByWEB/<ip>")
def setIPByWEB(ip):
    global ipAdversario, minhaJogada, jogadaAdversario

    minhaJogada = randint(1, 2)
    jogadaAdversario = 3-minhaJogada

    if not ipAdversario:
        ipAdversario = ip

        r = requests.get("http://" + ip + "/setIPByServer/" + str(myPort), params={"jogada": minhaJogada})

        return "S"

    return "N"

@app.route("/jogar")
def recebeJogada():
    x = request.args.get('x')
    y = request.args.get('y')

    if ipAdversario.split(":")[0]!=request.remote_addr:
        return "N"

    tabuleiro[int(x)][int(y)] = jogadaAdversario
    socketio.emit("NovaJogada", str(tabuleiro))

    return str(tabuleiro)

socketio.run(app, debug=True, port=myPort)