# Robo Instrumentador
Robô Instrumentador para a disciplina Robótica Industrial do 7ºSemestre do Insper, com integração com eletiva de IOT.

## Introdução
A preparação de kits para cirurgias atualmente é feita manualmente. O objetivo do projeto é automatizar esse processo utilizando robótica e banco de dados.

<div align="center">
<img src ="https://github.com/VonIgnia/RoboInstrumentador/assets/72100554/a01eb235-bc5f-4beb-80f7-b016292764c1" width="400px"/>
</div>

## Fluxograma do robô
O robô colaborativo UR5 foi programado no teachpendant do controlador para gerar um arquivo ```.urp``` que recebe informações nos registradores via ModBus e executa a ação de pegar determinada caixa e deixar em uma posição determinada. 

### Sub-rotina de pegar a gaveta
### Sub-rotina de entregar a gaveta

## FLuxograma da solução IoT


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
