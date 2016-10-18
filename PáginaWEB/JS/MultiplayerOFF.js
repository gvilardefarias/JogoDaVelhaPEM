$(document).ready(function(){
    $('.modal-trigger').leanModal();
});

var pecas = ['X', 'O'], vez = 0, placar = [0, 0], tabuleiro = new Array(3);
var dicionario = {1 : [0, 0],
                  2 : [0, 1],
                  3 : [0, 2],
                  4 : [1, 0],
                  5 : [1, 1],
                  6 : [1, 2],
                  7 : [2, 0],
                  8 : [2, 1],
                  9 : [2, 2]}

for(var i=0;i<3;i++){
    tabuleiro[i] = new Array('','','');
}

function atualizarTabuleiro(){
    console.log(tabuleiro);
    $('#1').html(tabuleiro[0][0]);
    $('#2').html(tabuleiro[0][1]);
    $('#3').html(tabuleiro[0][2]);
    $('#4').html(tabuleiro[1][0]);
    $('#5').html(tabuleiro[1][1]);
    $('#6').html(tabuleiro[1][2]);
    $('#7').html(tabuleiro[2][0]);
    $('#8').html(tabuleiro[2][1]);
    $('#9').html(tabuleiro[2][2]);
}

function addPeca(x, y){
    if(tabuleiro[x][y]!='')
        return;

    tabuleiro[x][y] = pecas[vez%2];
    atualizarTabuleiro();
    vez++;
}

function mouseEmCima(x){
    if(tabuleiro[dicionario[x][0]][dicionario[x][1]]!='')
        return;

    $('#' + x).html(pecas[vez%2]);
}