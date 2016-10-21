$(document).ready(function(){
    $('.modal-trigger').leanModal();
});

var pecas = ['X', 'O'], vez = 0, placar = [0, 0], tabuleiro = new Array(3), ganhador='False';
var dicionario = {1 : [0, 0],
  2 : [0, 1],
  3 : [0, 2],
  4 : [1, 0],
  5 : [1, 1],
  6 : [1, 2],
  7 : [2, 0],
  8 : [2, 1],
  9 : [2, 2]}

for(var i=0;i<3;i++)
    tabuleiro[i] = new Array('','','');

function atualizarTabuleiro(){
    if(ganhador!='False')
        return;

    $('#1').html(tabuleiro[0][0]);
    $('#2').html(tabuleiro[0][1]);
    $('#3').html(tabuleiro[0][2]);
    $('#4').html(tabuleiro[1][0]);
    $('#5').html(tabuleiro[1][1]);
    $('#6').html(tabuleiro[1][2]);
    $('#7').html(tabuleiro[2][0]);
    $('#8').html(tabuleiro[2][1]);
    $('#9').html(tabuleiro[2][2]);

    $(".1").removeClass("z-depth-3");
    $(".2").removeClass("z-depth-3");
    $(".3").removeClass("z-depth-3");
    $(".4").removeClass("z-depth-3");
    $(".5").removeClass("z-depth-3");
    $(".6").removeClass("z-depth-3");
    $(".7").removeClass("z-depth-3");
    $(".8").removeClass("z-depth-3");
    $(".9").removeClass("z-depth-3");
}

function addPeca(x, y){
    if(ganhador!='False')
        return;

    if(tabuleiro[x][y]!='')
        return;

    tabuleiro[x][y] = pecas[vez%2];
    atualizarTabuleiro();

    $.ajax({
        type : "POST",
        url : "http://localhost:" + myPort + "/temVencedor",
        data: JSON.stringify(tabuleiro, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            if(result!='False'){
                ganhador = result;
                placar[vez%2]++;
                $(".placar1").text(placar[0]);
                $(".placar2").text(placar[1]);
                $('#Placar').openModal();
            }
        }
    });

    vez++;
}

function mouseEmCima(x){
    if(ganhador!='False')
        return;

    if(tabuleiro[dicionario[x][0]][dicionario[x][1]]!='')
        return;

    $('.' + x).addClass("z-depth-3");

    $('#' + x).html(pecas[vez%2]);
}

function limpaTudo(){
    console.log("ok");
    vez = 0;
    ganhador='False';

    tabuleiro = new Array(3);
    for(var i=0;i<3;i++)
        tabuleiro[i] = new Array('','','');

    atualizarTabuleiro();
}
