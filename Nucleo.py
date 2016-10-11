def copiarMatriz(matrizOriginal):
    copia = []

    for i in matrizOriginal:
        copiaLinha = []

        for j in i:
            copiaLinha.append(j)

        copia.append(copiaLinha)

    return copia

def verificarVencedor(tabuleiro, espacoEmBranco):
    todosIguaisNaDiagonal1 = True
    todosIguaisNaDiagonal2 = True

    for i in range(2):
        if tabuleiro[i][i]!=tabuleiro[i+1][i+1] or tabuleiro[i][i]==espacoEmBranco or tabuleiro[i+1][i+1]==espacoEmBranco:
            todosIguaisNaDiagonal1 = False

        if tabuleiro[i][2-i]!=tabuleiro[i+1][1-i] or tabuleiro[i][2-i]==espacoEmBranco or tabuleiro[i+1][1-i]==espacoEmBranco:
            todosIguaisNaDiagonal2 = False

    if todosIguaisNaDiagonal1 or todosIguaisNaDiagonal2:
        return tabuleiro[1][1]

    for i in range(3):
        todosIguaisNaLinha = True
        todosIguaisNaColuna = True

        for j in range(2):
            if tabuleiro[i][j]!=tabuleiro[i][j+1] or tabuleiro[i][j]==espacoEmBranco or tabuleiro[i][j+1]==espacoEmBranco:
                todosIguaisNaLinha = False

            if tabuleiro[j][i]!=tabuleiro[j+1][i] or tabuleiro[j][i]==espacoEmBranco or tabuleiro[j+1][i]==espacoEmBranco:
                todosIguaisNaColuna = False

        if todosIguaisNaLinha or todosIguaisNaColuna:
            return tabuleiro[i][i]

    return False