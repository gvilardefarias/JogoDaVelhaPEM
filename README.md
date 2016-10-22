#Começando

Para usar o jogo, primeiro você deve instalar as dependencias usando [esse guia](https://github.com/gvilardefarias/JogoDaVelhaPEM/blob/master/Instala%C3%A7%C3%A3o/Guia)

Após todas as dependencias instaladas, você deve rodar o servidor na pasta raiz do projeto com o comando 
>python Cliente-Servidor.py

Com o servidor rodando, você já pode abrir o index que se encontra na pasta
>PáginaWEB

#Ajustes
##Troca de porta
Para trocar a porta do servidor você deve alterar a variavel myPort nos arquivos 
>Cliente-Servidor.py
>PáginaWEB/JS/porta.js

##Jogar com outro servidor no mesmo PC
Para jogar com outro servidor no mesmo PC você pode ultilizar a interface web que se encontra na pasta
>PáginaWEB/Teste

E o servidor
>Cliente-ServidorTeste.py

Ambos estão pré-configurados para a porta **5005**, lmebrando também que o servidor principal está pré-configurado para porta **5000**

#Jogar no multiplayer em rede
Para jogar no multiplayer em rede, ambos devem abrir a página de multiplayer online, e **em apenas uma máquina deve ser colocada o IP e a porta da outra máquina**, *para fechar a tela de IP na outra máquina basta aperta em algum lugar fora do bloco* 

##Erros de comunicação
Eventualmente alguns erros podem acontecer na comunicação, caso ocorra algum desses erros você deve:
- Atualizar a página
- Recolocar o IP do oponente
- Atualizar a página do oponente
- Em ultimo caso, reiniciar o servidor