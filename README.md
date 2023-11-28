# Robo Instrumentador
Robô Instrumentador para a disciplina Robótica Industrial do 7ºSemestre do Insper, com integração com a eletiva de IOT.

## Introdução
A preparação de kits para cirurgias atualmente é feita manualmente, sendo passível de erros. O objetivo do projeto é automatizar esse processo utilizando robótica e internet das coisas.

<div align="center">
<img src ="https://github.com/VonIgnia/RoboInstrumentador/assets/72100554/a01eb235-bc5f-4beb-80f7-b016292764c1" width="400px"/>
</div>

## Fluxograma do robô
O robô colaborativo UR5 foi programado no teachpendant do controlador para gerar um arquivo ```.urp``` que recebe informações nos registradores via ModBus e executa a ação de pegar determinada gaveta e deixar em uma posição determinada. Cada uma das gavetas da estante representa um item que estará presente no kit cirúrgico de determinado procedimento. A montagem desse kit se dá pela disposição das gavetas sobre a mesa. Essa disposição é feita com três gavetas que são postas sobre a mesa lado a lado.   

O código do robô foi pensado para realizar duas sub-rotinas maiores: a de pegar a gaveta e a de entregar a gaveta. Antes de iniciar esses procedimentos, o robô é orientado a ir para uma posição inicial para que, em seguida, leia aquilo que foi entregue via ModBus em seus registradores e realize as respectivas movimentações.  
<div align="center">
<img src ="https://github.com/VonIgnia/RoboInstrumentador/assets/72100554/3f325ff5-4a6e-4ef9-859f-31c2ed85e3a1" width="400px"/>
</div>

### Sub-rotina de pegar a gaveta
Na sub-rotina em que robô precisa ir até a gaveta par pegá-la, o robô parte de sua posição inicial e vai em direção a posição de aproximação da gaveta, em seguida, aproxima-se da gaveta, fecha a garra, segurando-a pela alça, e leva para a posição intermediária entre as caixas do gaveteiro. 

<div align="center">
<img src ="https://github.com/VonIgnia/RoboInstrumentador/assets/72100554/d7cad2ff-6648-415d-9450-6da64bcf8ba4" width="400px"/>
</div>

### Sub-rotina de entregar a gaveta
Na sub-rotina de entrega, a posição do Tool Center Point (TCP) do robô está perpendicular a posição necessária para a deposição da gaveta sobre a mesa, logo o robô rotacionará a base e iniciará o processo de entrega da gaveta. Para que as gavetas sejam deixadas lado a lado sobre a mesa, um contador monitora a quantidade de gavetas que foram entregues nesse pedido e, de acordo com seu valor, faz com que o robô leve a caixa para um das três posições possíveis, de modo a enfileirá-las, solte a garra, afaste-se da gaveta e retorne para a  posição inicial. 

<div align="center">
<img src ="https://github.com/VonIgnia/RoboInstrumentador/assets/72100554/3a2c24a4-e72c-4471-9430-b420a83c45a1" width="400px"/>
</div>

## Solução IoT
A solução de IoT traz ao usuário a possibilidade de enviar remotamente ao robô qual kit contido na base de dados deverá ser preparado por meio de uma aplicação web. Para isso, a aplicação web disponibiliza quais kits estão na base de dados e permite que o usuário envie o pedido de preparo por ela, com isso, esse pedido é publicado em um servidor HTTP MQTT para um broker da AWS. O robô, que está inscrito no mesmo tópico do broker, recebe a mensagem enviada ao broker pela aplicação e manda via ModBus ao robô.      

## Troubleshooting
Comandos no terminal:
Para detectar se há multiplas versões de python na Rasp: ls -ls /usr/bin/python*

erros envolvendo numpy: 
sudo apt update
sudo apt remove python3-numpy
sudo apt install libatlas3-base
sudo pip3 install numpy
fonte: https://raspberrypi.stackexchange.com/questions/91679/upgrading-to-latest-numpy-version-on-raspberry-pi-3

instalar bibliotecas: sudo pip3 install [biblioteca]

https://pypi.org/project/pygigev/
