$(document).ready(function(){
    $('.modal-trigger').leanModal();
});

var pecas = 'X', vez = 0, placar = [0, 0], tabuleiro = new Array(3), ganhador='False';
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

    var x=1;

    for(var i=0;i<3;i++){
        for(var j=0;j<3;j++){
            if(tabuleiro[i][j]=="O"){
                $('#' + x).attr("src",".config/Imgs/Henrique.png");
            }
            else{
                if(tabuleiro[i][j]=="X"){
                    $('#' + x).attr("src",".config/Imgs/O.png");
                }
                else{
                    $('#' + x).attr("src",".config/Imgs/Transparente.png");
                }
            }

            x++;
        }
    }

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

    tabuleiro[x][y] = pecas;
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

    if(ganhador!='False')
        return

    $.ajax({
        type : "POST",
        url : "http://localhost:" + myPort + "/pegarJogadaDaIA",
        data: JSON.stringify(tabuleiro, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);

            result = JSON.parse(result);

            tabuleiro[result[0]][result[1]] = "O";
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
    });

    console.log(tabuleiro);
    vez++;
}

function mouseEmCima(x){
    if(ganhador!='False' || vez%2)
        return;

    if(tabuleiro[dicionario[x][0]][dicionario[x][1]]!='')
        return;

    $('.' + x).addClass("z-depth-3");
    $('#' + x).attr("src",".config/Imgs/O.png");
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
