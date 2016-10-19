from flask_socketio import send, SocketIO, emit
from flask import Flask, request
from flask_cors import CORS, cross_origin
from random import randint
import requests
import Nucleo

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

tabuleiro = [['','',''],
             ['','',''],
             ['','','']]

ipAdversario = False
minhaJogada = 0
jogadaAdversario = 0
myPort = 5005

@app.route("/temVencedor", methods = ['POST'])
def temVencedor():
    tabuleiro = request.json
    return str(Nucleo.verificarVencedor(tabuleiro, ''))

@app.route("/setIPByServer/<port>")
def setIPByServer(port):
    global ipAdversario, minhaJogada, jogadaAdversario

    if not ipAdversario:
        jogadaAdversario = request.args.get("jogada")

        if jogadaAdversario=="X":
            minhaJogada = "O"
        else:
            minhaJogada = "X"

        socketio.emit("defineJogada", minhaJogada)
        ipAdversario = request.remote_addr + ":" + str(port)

        return minhaJogada

    return "N"

@app.route("/setIPByWEB/<ip>")
def setIPByWEB(ip):
    global ipAdversario, minhaJogada, jogadaAdversario

    minhaJogada = randint(1, 2)
    if minhaJogada==1:
        minhaJogada = "X"
    else:
        minhaJogada = "O"

    if not ipAdversario:
        ipAdversario = ip

        r = requests.get("http://" + ip + "/setIPByServer/" + str(myPort), params={"jogada": minhaJogada})

        return minhaJogada

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