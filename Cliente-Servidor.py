from flask_socketio import send, SocketIO, emit
from flask import Flask, request
from flask_cors import CORS, cross_origin
from random import randint
import socket
import fcntl
import struct
import requests
import Nucleo

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

tabuleiro = [['','',''],
             ['','',''],
             ['','','']]

ipAdversario = False
minhaJogada = ''
jogadaAdversario = 0
myPort = 5000
minhaVez = "true"

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', 'eth0'[:15])
    )[20:24])

@app.route("/temVencedor", methods = ['POST'])
def temVencedor():
    tabuleiro = request.json
    return str(Nucleo.verificarVencedor(tabuleiro, ''))

@app.route("/pegarPeca")
def pegarPeca():
    return minhaJogada

@app.route("/pegarTabuleiro")
def pegarTabuleiro():
    return str(tabuleiro).replace("'","\"")

@app.route("/setIPByServer/<ip>")
def setIPByServer(ip):
    global ipAdversario, minhaJogada, jogadaAdversario

    if not ipAdversario:
        jogadaAdversario = request.args.get("jogada")

        if jogadaAdversario=="X":
            minhaJogada = "O"
        else:
            minhaJogada = "X"

        socketio.emit("defineJogada", minhaJogada)

        ipAdversario = str(ip)

        print(ipAdversario)

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

        r = requests.get("http://" + ip + "/setIPByServer/" + get_ip_address() + ":" + str(myPort), params={"jogada": minhaJogada})

    return minhaJogada

@app.route("/jogar")
def recebeJogada():
    x = request.args.get('x')
    y = request.args.get('y')

    minhaVez = "true"
    tabuleiro[int(x)][int(y)] = str(jogadaAdversario)
    socketio.emit("NovaJogada", str(tabuleiro).replace("'","\""))

    return str(tabuleiro).replace("'","\"")

@app.route("/jogarNoAdversario")
def recebeJogadaWEB():
    x = request.args.get('x')
    y = request.args.get('y')

    minhaVez = "false"
    tabuleiro[int(x)][int(y)] = str(minhaJogada)

    r = requests.get("http://" + ipAdversario + "/jogar", params={"x": x, "y": y})

    return "S"

@app.route("/pegarMinhaVez")
def pegarMinhaVez():
    return minhaVez

socketio.run(app, debug=True, port=myPort, host='0.0.0.0')