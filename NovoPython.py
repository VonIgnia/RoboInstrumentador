#sudo path/to/venv/bin/pip ...
#sudo path/to/venv/bin/python -m pip ...

'''
>> Modbus TCP:
- Utilizar a biblioteca pyModbusTCP (instalar via pip install)
- O código de exemplo trabalha com os registradores de entrada e saída 0
- Em python, os objetos "server" e "server.data_bank" possuem os métodos para escrever e ler os registradores/bobinas (utilizar print(dir(server)) e print(dir(server.data_bank)) para visualizar os comandos)
'''

from pyModbusTCP.server import ModbusServer
from pyModbusTCP.client import ModbusClient
from time import sleep
from random import uniform

#############################################################################################
dicionario_gaveta = {'tesoura':1, 'bisturi':2, 'seringa':3, 'agulha':4, 'gaze':5, 'pinca':6}
lista_ferramentas = []

inicio_nome = 1
while inicio_nome:
    primeira_fer = input('Qual ferramenta voce deseja? Digite em letra minuscula:')
    if primeira_fer in dicionario_gaveta:
        lista_ferramentas.append(primeira_fer)
        inicio_nome = 0
    else:
        print('Desculpe, essa ferramenta nao esta disponivel')

continua_pergunta = 1
while continua_pergunta:
    resposta =input('Deseja algo mais? (s/n):')
    if resposta == 'n':
        continua_pergunta = 0
    else:
        ferramenta = input('O que voce deseja?:')
        if ferramenta in dicionario_gaveta:
            lista_ferramentas.append(ferramenta) 
        else:
            print('Desculpe, esa ferramenta nao esta disponivel')

def chave_personalizada(item):
    return dicionario_gaveta[item]

lista_organizada = sorted(lista_ferramentas, key=chave_personalizada)
lista_envio = [dicionario_gaveta[chave] for chave in lista_organizada]

print(lista_envio)

################################################################################################

class ListaModbus:
    def __init__(self,lista):
        self.lista = lista
        self.posição = 0

    def obter_proximo_valor(self, sinal_modbus):
        if sinal_modbus == 1:
            if self.posicao_atual < len(self.lista):
                valor_atual = self.lista[self.posicao_atual]
                self.posicao_atual +=1
                return valor_atual
            else:
                return 7
        else:
            return None

modbus_handler = ListaModbus(lista_envio)
#
#Create an instance of ModbusServer
HOST_ADDRESS = '10.103.16.12' #'localhost' 
HOST_PORT = 502
server = ModbusServer(HOST_ADDRESS, HOST_PORT, no_block = True)

try:
    print('Starting server...')
    server.start()
    print('Server is online')

    while True:
        DATA_RECEIVED = server.data_bank.get_holding_registers(0)
        DATA_SENT = modbus_handler.obter_proximo_valor(DATA_RECEIVED)

        #Envia lista de zeros para os 6 registradores
        #DATA_SENT = [dicionario_numero['tesoura']]
        #server.data_bank.set_input_registers(128, DATA_SENT)
        #DATA_SENT = [dicionario_numero['bisturi']]
        #server.data_bank.set_input_registers(129, DATA_SENT)
        #DATA_SENT = [dicionario_numero['seringa']]
        #server.data_bank.set_input_registers(130, DATA_SENT)
        #DATA_SENT = [dicionario_numero['agulha']]
        #server.data_bank.set_input_registers(131, DATA_SENT)
        #DATA_SENT = [dicionario_numero['gaze']]
        #server.data_bank.set_input_registers(132, DATA_SENT)
        #DATA_SENT = [dicionario_numero['pinca']]
        #server.data_bank.set_input_registers(133, DATA_SENT)
    
        #DATA_RECEIVED = server.data_bank.get_holding_registers(0)
        #server.data_bank.set_input_registers(0, DATA_SENT)
        print('Data sent:', DATA_SENT)
        print('Data received:', DATA_RECEIVED)
        sleep(0.5)

except Exception as e:
    print(e)
    print('Shutting down server...')
    server.stop()
    print('Server is offline')
#
