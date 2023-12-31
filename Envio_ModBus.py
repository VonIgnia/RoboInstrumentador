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
dicionario_gaveta = {'tesoura':1, 'bisturi':2, 'seringa':3, 'agulha':4, 'gaze':5, 'pinça':6}
dicionario_numero = {'tesoura':0, 'bisturi':0, 'seringa':0, 'agulha':0, 'gaze':0, 'pinça':0}

lista_ferramentas_nome = [0]
inicio_nome = 1
while inicio_nome:
    primeira_fer = input('Qual ferramenta voce deseja? Digite em letra minuscula:')
    if primeira_fer in dicionario_gaveta:
        lista_ferramentas_nome[0] = primeira_fer
        inicio_nome = 0
    else:
        print('Desculpe, essa ferramenta nao esta disponivel')

inicio_quant = 1
while inicio_quant:
    primeira_quant = input('Quantas ferramenta voce deseja?: Digite numeros, (nao usar virgula):')
    if float(primeira_quant).is_integer():

        dicionario_numero[primeira_fer] = primeira_quant
        inicio_quant = 0
    else:
        print('Desculpe, esse numero nao e aceitavel')

continua_pergunta = 1
continua_quant = 1
while continua_pergunta:
    resposta =input('Deseja algo mais? (s/n):')
    if resposta == 'n':
        continua_pergunta = 0
    else:
        ferramenta = input('O que voce deseja?:')
        if ferramenta in dicionario_gaveta:
            lista_ferramentas_nome.append(ferramenta)
            while continua_quant:
                quant = input('Quantas ferramenta voce deseja?: Digite numeros, (nao usar virgula):')
                if float(quant).is_integer():
                    #indice = list(dicionario_gaveta.keys()).index(ferramenta)
                    dicionario_numero[ferramenta] = quant 
                    continua_quant = 0
                else:
                    print('Desculpe, esse numero nao e aceitavel')

        else:
            print('Desculpe, esa ferramenta nao esta disponivel')


print(dicionario_numero)
lista_ferramentas = [dicionario_gaveta[ferramenta] for ferramenta in lista_ferramentas_nome]
#lista_ferramentas = sorted([dicionario[nome] for nome in lista_ferramentas_nome])
lista_ferramentas


n_posicoes = 6
lista_final = [0]*n_posicoes
for n in range(len(lista_ferramentas)):
    lista_final[n] = lista_ferramentas[n]

################################################################################################



#Create an instance of ModbusServer
HOST_ADDRESS = '10.103.16.11' #'localhost' 
HOST_PORT = 502
server = ModbusServer(HOST_ADDRESS, HOST_PORT, no_block = True)

try:
    print('Starting server...')
    server.start()
    print('Server is online')

    while True:
        #print("Its True")
        #Envia lista de zeros para os 6 registradores
        DATA_SENT = [lista_final[0]]
        server.data_bank.set_input_registers(128, DATA_SENT)
        DATA_SENT = [lista_final[1]]
        server.data_bank.set_input_registers(129, DATA_SENT)
        DATA_SENT = [lista_final[2]]
        server.data_bank.set_input_registers(130, DATA_SENT)
        DATA_SENT = [lista_final[3]]
        server.data_bank.set_input_registers(131, DATA_SENT)
        DATA_SENT = [lista_final[4]]
        server.data_bank.set_input_registers(132, DATA_SENT)
        DATA_SENT = [lista_final[5]]
        server.data_bank.set_input_registers(133, DATA_SENT)
    
        #DATA_RECEIVED = server.data_bank.get_holding_registers(0)
        #server.data_bank.set_input_registers(0, DATA_SENT)
        print('Data sent:', DATA_SENT)
        #print('Data received:', DATA_RECEIVED)
        sleep(0.5)

except Exception as e:
    print(e)
    print('Shutting down server...')
    server.stop()
    print('Server is offline')