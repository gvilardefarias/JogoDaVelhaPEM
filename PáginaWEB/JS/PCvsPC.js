$(document).ready(function(){
  $('.modal-trigger').leanModal();
  $("#escolherIP").openModal();
});

var pecas = ['X', 'O'], minhaPeca, minhaVez = false, placar = [0, 0], tabuleiro = new Array(3), ganhador='False', passar=false;
var dicionario = {1 : [0, 0], 2 : [0, 1], 3 : [0, 2], 4 : [1, 0], 5 : [1, 1], 6 : [1, 2], 7 : [2, 0], 8 : [2, 1], 9 : [2, 2]};

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

function atualizaDados(){
  $.get("http://localhost:" + myPort + "/pegarPeca").done(function minhaJogada(result){
    minhaPeca = result;
  });

  $.get("http://localhost:" + myPort + "/pegarMinhaVez").done(function minhaJogada(result){
    if(result=='')
      return;

    minhaVez = JSON.parse(result);
  });

  $.get("http://localhost:" + myPort + "/pegarTabuleiro").done(function minhaJogada(result){
    tabuleiro = JSON.parse(result.toString());

    atualizarTabuleiro();
  });
}

atualizaDados();

function temVencedor(){
  $.ajax({
    type : "POST",
    url : "http://localhost:" + myPort + "/temVencedor",
    data: JSON.stringify(tabuleiro, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      if(result!='False'){
        passar = true;

        $('.again').removeClass("disabled");

        ganhador = result;

        if(ganhador=='X')
          placar[0]++;
        else
          placar[1]++;

        $(".placar1").text(placar[0]);
        $(".placar2").text(placar[1]);
        $('#Placar').openModal();
      }
    }
  });
}

function passarPartida(){
  if(!passar)
    return;

  $.get("http://localhost:" + myPort + "/passarPartida").done(function minhaJogada(result){
  });

  passar = false;

  $('.again').addClass("disabled");
}


function novaJogada(tabuleiroE){
  tabuleiro = JSON.parse(tabuleiroE.toString());

  minhaVez = true;

  atualizarTabuleiro();
  temVencedor();
}

function addPeca(x, y){
  if(ganhador!='False' || !minhaVez)
    return;

  if(tabuleiro[x][y]!='')
    return;

  $.get("http://localhost:" + myPort + "/jogarNoAdversario?x=" + x.toString() + "&y=" + y.toString())
  .done(function( data ) {});

  tabuleiro[x][y] = minhaPeca;

  temVencedor();

  minhaVez = false;
}

function setandoAdversario(){
  $.ajax({
    type : "GET",
    url : "http://localhost:" + myPort + "/setIPByWEB/" + $('#ip').val() + ":" + $('#porta').val(),
    success: function(result) {
      minhaPeca = result;
      console.log(result);
    }
  });
}

function mouseEmCima(x){
  if(ganhador!='False' || !minhaVez)
    return;

  if(tabuleiro[dicionario[x][0]][dicionario[x][1]]!='')
    return;

  $('.' + x).addClass("z-depth-3");

  $('#' + x).html(minhaPeca);
}

var socket = io.connect("http://localhost:" + myPort);

socket.on('NovaJogada', function(result) {
  novaJogada(result);
});

socket.on('defineJogada', function(result) {
  minhaPeca = result;
});

socket.on('defineVez', function(result) {
  console.log(result);

  minhaVez = JSON.parse(result);
});

socket.on('habilitarPassar', function(result) {
  passar = true;
  atualizarTabuleiro();
});

socket.on('passarPartida', function(result) {
  $('.again').addClass("disabled");
  minhaVez = false;
  tabuleiro = new Array(3);
  ganhador='False';
  eu=0;
  passar=false;

  for(var i=0;i<3;i++)
    tabuleiro[i] = new Array('','','');

  atualizaDados();
});
