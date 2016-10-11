import Nucleo
from random import randint

def julgarJogada(tabuleiroAtual, pecaDaIA, pecaDoJogador, espacoEmBranco, vez=0):
    jogadas = []
    vencedor = Nucleo.verificarVencedor(tabuleiroAtual, espacoEmBranco)

    if vencedor==pecaDaIA:
        return 0
    if vencedor:
        return 2

    for i in range(3):
        for j in range(3):
            if tabuleiroAtual[i][j]==espacoEmBranco:
                tabuleiro = Nucleo.copiarMatriz(tabuleiroAtual)

                if vez%2:
                    tabuleiro[i][j] = pecaDaIA
                else:
                    tabuleiro[i][j] = pecaDoJogador

                jogadas.append(julgarJogada(tabuleiro, pecaDaIA, pecaDoJogador, espacoEmBranco, vez+1))

    if jogadas:
        if vez%2:
            jogadas = sorted(jogadas)
        else:
            jogadas = sorted(jogadas, reverse=True)
        return jogadas[0]

    return 1

def pegarJogadaDaIa(tabuleiroAtual, espacoEmBranco, pecaDaIA, pecaDoJogador):
    #0:Ganha, 1:Empata, 2:Perde
    jogadas = [[],[],[]]

    for i in range(3):
        for j in range(3):
            if tabuleiroAtual[i][j]==espacoEmBranco:
                tabuleiro = Nucleo.copiarMatriz(tabuleiroAtual)

                tabuleiro[i][j] = pecaDaIA
                jogada = julgarJogada(tabuleiro, pecaDaIA, pecaDoJogador, espacoEmBranco)
                
                jogadas[jogada].append((i, j))

    if len(jogadas[0]):
        return jogadas[0][randint(0, len(jogadas[0])-1)]
    if len(jogadas[1]):
        return jogadas[1][randint(0, len(jogadas[1])-1)]
    if len(jogadas[2]):
        return jogadas[2][randint(0, len(jogadas[2])-1)]

#Testes

tabuleiro = [[0,0,0],[0,0,0],[0,0,0]]

while True:
    aux = input().split()
    x = int(aux[0])
    y = int(aux[1])

    tabuleiro[x][y] = 1

    for i in tabuleiro:
        print(i)

    print("\n\n")

    x, y = pegarJogadaDaIa(tabuleiro, 0, 2, 1)

    tabuleiro[x][y] = 2

    for i in tabuleiro:
        print(i)

    print("\n\n")