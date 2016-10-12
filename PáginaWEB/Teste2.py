from flask_socketio import send, SocketIO, emit
from flask import Flask, request
import requests

app = Flask(__name__)
socketio = SocketIO(app)

tabuleiro = [[0,0,0],
             [0,0,0],
             [0,0,0]]
ipAdversario = False
myPort = 5005

@app.route("/setIPByServer/<port>")
def setIPByServer(port):
    global ipAdversario

    if not ipAdversario:
        ipAdversario = request.remote_addr + ":" + str(port)
        print(ipAdversario)

        return "S"

    return "N"

@app.route("/setIPByWEB/<ip>")
def setIPByWEB(ip):
    global ipAdversario

    if not ipAdversario:
        ipAdversario = ip

        print(ipAdversario)
        r = requests.get("http://" + ip + "/setIPByServer/" + str(myPort))
        return "S"

    return "N"

@app.route("/jogar")
def recebeJogada():
    x = request.args.get('x')
    y = request.args.get('y')
    jogada = int(request.args.get("jogada"))
    print(x)
    print(y)
    print(jogada)

    tabuleiro[int(x)][int(y)] = jogada
    socketio.emit("NovaJogada", str(tabuleiro))
    return str(tabuleiro)

socketio.run(app, debug=True, port=myPort)