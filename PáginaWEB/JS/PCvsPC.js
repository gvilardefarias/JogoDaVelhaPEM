var socket = io.connect('http://localhost:5005');

socket.on('NovaJogada', function(tabuleiro) {
    console.log(JSON.parse(tabuleiro));
    var aux = JSON.parse(tabuleiro);

    console.log(aux[0][0]);
    $('#1').html(aux[0][0]);
    $('#2').html(aux[0][1]);
    $('#3').html(aux[0][2]);
    $('#4').html(aux[1][0]);
    $('#5').html(aux[1][1]);
    $('#6').html(aux[1][2]);
    $('#7').html(aux[2][0]);
    $('#8').html(aux[2][1]);
    $('#9').html(aux[2][2]);
});