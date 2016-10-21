from flask_socketio import send, SocketIO, emit
from flask import Flask, request
from flask_cors import CORS, cross_origin
from random import randint
import socket
import fcntl
import struct
import requests
import Nucleo
import IA

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

tabuleiro = [['','',''],
             ['','',''],
             ['','','']]

ipAdversario = False
minhaJogada = ''
jogadaAdversario = 0
myPort = 5005
minhaVez = ""

def limpaTudo():
    global tabuleiro, ipAdversario, minhaJogada, jogadaAdversario, minhaVez
    tabuleiro = [['','',''],
                 ['','',''],
                 ['','','']]

    ipAdversario = False
    minhaJogada = ''
    jogadaAdversario = 0
    minhaVez = ""

def setJogada():
    global minhaVez, jogadaAdversario, minhaJogada

    minhaJogada = randint(1, 2)

    if minhaJogada==1:
        minhaJogada = "X"
        jogadaAdversario = "O"
        minhaVez = "true"
    else:
        minhaJogada = "O"
        jogadaAdversario = "X"
        minhaVez = "false"

    requests.get("http://" + ipAdversario + "/setJogada/" + str(minhaJogada))

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

@app.route("/setJogada/<jogada>")
def setJogadaW(jogada):
    global minhaVez, jogadaAdversario, minhaJogada

    jogadaAdversario = str(jogada)

    if jogadaAdversario=="X":
        minhaJogada = "O"
        minhaVez = "false"
    else:
        minhaJogada = "X"
        minhaVez = "true"

    socketio.emit("defineJogada", minhaJogada)
    socketio.emit("defineVez", minhaVez)

    return ""

@app.route("/setIPByServer/<ip>")
def setIPByServer(ip):
    global ipAdversario, minhaJogada, jogadaAdversario, minhaVez

    limpaTudo()

    ipAdversario = str(ip)

    print(ipAdversario)

    return minhaJogada

@app.route("/setIPByWEB/<ip>")
def setIPByWEB(ip):
    global ipAdversario, minhaJogada, jogadaAdversario, minhaVez

    limpaTudo()

    ipAdversario = ip

    r = requests.get("http://" + ip + "/setIPByServer/" + get_ip_address() + ":" + str(myPort))

    setJogada()

    socketio.emit("defineJogada", minhaJogada)
    socketio.emit("defineVez", minhaVez)

    return minhaJogada

@app.route("/jogar")
def recebeJogada():
    global minhaVez, tabuleiro

    x = request.args.get('x')
    y = request.args.get('y')

    minhaVez = "true"
    tabuleiro[int(x)][int(y)] = str(jogadaAdversario)
    socketio.emit("NovaJogada", str(tabuleiro).replace("'","\""))

    return str(tabuleiro).replace("'","\"")

@app.route("/jogarNoAdversario")
def recebeJogadaWEB():
    global minhaVez, tabuleiro

    x = request.args.get('x')
    y = request.args.get('y')

    minhaVez = "false"
    tabuleiro[int(x)][int(y)] = str(minhaJogada)

    r = requests.get("http://" + ipAdversario + "/jogar", params={"x": x, "y": y})

    return "S"

@app.route("/pegarMinhaVez")
def pegarMinhaVez():
    return minhaVez

@app.route("/passarPartidaServidor")
def passarPartidaServidor():
    global tabuleiro

    tabuleiro = [['','',''],
                ['','',''],
                ['','','']]

    socketio.emit("passarPartida", "ok")
    socketio.emit("defineJogada", minhaJogada)
    socketio.emit("defineVez", minhaVez)

    return ""

@app.route("/passarPartida")
def passarPartida():
    global tabuleiro

    tabuleiro = [['','',''],
                ['','',''],
                ['','','']]

    r = requests.get("http://" + ipAdversario + "/passarPartidaServidor")

    socketio.emit("passarPartida", "ok")
    setJogada()
    
    return ""

@app.route("/pegarJogadaDaIA", methods = ['POST'])
def pegarJogadaDaIA():
    tabuleiro = request.json

    x, y = IA.pegarJogadaDaIa(tabuleiro, '', 'O', 'X')

    return str([x, y])

socketio.run(app, debug=True, port=myPort, host='0.0.0.0')