import ssl
from pyModbusTCP.server import ModbusServer
from paho.mqtt.client import Client
from time import sleep


#-----------------------------------------------------------------------------------------------------------------
#                                            MQTT Configuration
#-----------------------------------------------------------------------------------------------------------------
broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443
topic = "gi/mandando/dados"
client_id = "gigio"
ca = "certs/AmazonRootCA1.pem"
cert = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-certificate.pem.crt"
private = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-private.pem.key"
import time

#dicionario que relaciona as ferramentas com suas posições (gavetas)
dicionario_gaveta = {'tesoura':1, 'bisturi':2, 'seringa':3, 'agulha':4, 'gaze':5, 'pinca':6}
#estoque que define quantas ferramentas ainda tem em cada gaveta (2:1 significa que tem 1 ferramenta na gaveta 2)
estoque = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1}

# Modbus Configuration
HOST_ADDRESS = '10.103.16.12'  # 'localhost'
HOST_PORT = 502
server = ModbusServer(HOST_ADDRESS, HOST_PORT, no_block=True)

#-----------------------------------------------------------------------------------------------------------------
                                            #MQTT Listener
#-----------------------------------------------------------------------------------------------------------------

def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = Client(client_id)
    ssl_context = ssl_alpn()
    client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def update_payload_value(value):
    #define variavel global payload_value, que é atualizada quando a função for chamada
    global payload_value
    payload_value = value

    #define variavel global INICIALIZAR, que é atualizada quando a função for chamada
    global INICIALIZAR
    INICIALIZAR = 1
    #print(payload_value)

def subscribe(client, callback):
    def on_message(client, userdata, msg):
        payload_value = int(msg.payload.decode())
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        callback(payload_value)
        

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect()
    subscribe(client, update_payload_value)
    client.loop_start()


#-----------------------------------------------------------------------------------------------------------------
                #Funções, Classes e Dicionarios utilizadoas para definir sinais enviados para o robo
#-----------------------------------------------------------------------------------------------------------------

# dicionario utilizado para verificar que ferramentas fazem parte de que kit e em que gavetas elas se encontram 
def get_lista_mqtt(payload):
    print('---------------------------------------------------------------------')
    switch_dict = {
        1: ['tesoura'],
        2: ['bisturi'],
        3: ['seringa'],
        4: ['agulha'],
        5: ['gaze'],
        6: ['pinca'],
        7: ['tesoura', 'bisturi'],
        8: ['tesoura', 'seringa'],
        9: ['tesoura', 'agulha'],
        10: ['tesoura', 'gaze'],
        11: ['tesoura', 'pinca'],
        12: ['bisturi', 'seringa'],
        13: ['bisturi', 'agulha'],
        14: ['bisturi', 'gaze'],
        15: ['bisturi', 'pinca'],
        16: ['seringa', 'agulha'],
        17: ['seringa', 'gaze'],
        18: ['seringa', 'pinca'],
        19: ['agulha', 'gaze'],
        20: ['agulha', 'pinca'],
        21: ['gaze', 'pinca'],
        22: ['tesoura', 'bisturi', 'seringa'],
        23: ['tesoura', 'bisturi', 'agulha'],
        24: ['tesoura', 'bisturi', 'gaze'],
        25: ['tesoura', 'bisturi', 'pinca'],
        26: ['tesoura', 'seringa', 'agulha'],
        27: ['tesoura', 'seringa', 'gaze'],
        28: ['tesoura', 'seringa', 'pinca'],
        29: ['tesoura', 'agulha', 'gaze'],
        30: ['tesoura', 'agulha', 'pinca'],
        31: ['tesoura', 'gaze', 'pinca'],
        32: ['bisturi', 'seringa', 'agulha'],
        33: ['bisturi', 'seringa', 'gaze'],
        34: ['bisturi', 'seringa', 'pinca'],
        35: ['bisturi', 'agulha', 'gaze'],
        36: ['bisturi', 'agulha', 'pinca'],
        37: ['bisturi', 'gaze', 'pinca'],
        38: ['seringa', 'agulha', 'gaze'],
        39: ['seringa', 'agulha', 'pinca'],
        40: ['seringa', 'gaze', 'pinca'],
        41: ['agulha', 'gaze', 'pinca'],
        None: []
    }
    #verifica se o kit não é um valor vazio
    if payload is not None:
        payload = int(payload)
    #substitui o kit pelas ferramentas e as organiza de acordo com a ordem definida na chave_personalizada
    lista_organizada = sorted(switch_dict.get(payload, []), key=chave_personalizada)
    
    #substitui as ferramentas pelas gavetas em que elas estão armazenadas
    lista_envio = [dicionario_gaveta[chave] for chave in lista_organizada]
    return lista_envio



#classe que define que gaveta deve ser pegue
class Gaveta:
    def __init__(self, lista):
        self.lista = lista
        self.posicao_atual = 0

    def obter_proximo_valor(self, sinal_modbus):
        #codigo que verifica o sinal recebido do robo, que diz que a gaveta foi pega
        sinal = sinal_modbus
        if sinal == 1:
            #aumenta o valor que corresponde à posição na lista de gavetas
            self.posicao_atual += 1
        if self.posicao_atual < len(self.lista):
            #se o valor for menor que o tamanha maximo da lista (codigo ainda nao chegou na ultima posição de pega), define esse valor como a gaveta a ser pegue)
            valor_atual = self.lista[self.posicao_atual]
        
        else:
            #se o valor for maior ou igual ao tamanha maximo da lista (codigo já chegou na ultima posição de pega), define a ultima posição como a gaveta a ser pegue)
            valor_atual = self.lista[-1]
        return valor_atual

#classe que define em que posição a gaveta deve ser entregue
class Entrega:
    def __init__(self, lista):
        self.lista = lista
        self.posicao_atual = 1
        self.sinal = 0

    def obter_proximo_valor(self, sinal_modbus):
        #codigo que detecta borda de subida no sinal enviado pelo robo de que a gaveta foi entregue
        if sinal_modbus != self.sinal:
            self.sinal = sinal_modbus
            #se for borda de subida e a posição de entrega for menor que a posição maxima definida (3), avançar para a proxima posição de entrega
            if self.posicao_atual < len(self.lista) and self.posicao_atual < 3 and sinal_modbus == 1:
                self.posicao_atual += 1
            
        valor_atual = self.posicao_atual
        #print(valor_atual)
        return valor_atual

#classe que define se o robo ja entregou todas as ferramentas
class Terminou:
    def __init__(self, lista):
        self.lista = lista
        self.n_entregas = 0
        self.avancar = 0
        self.terminou = 0
        self.repeticoes = 0
        self.sinal  = 0

    def obter_proximo_valor(self, entregou):
        #nao utilizado na versão final
        if entregou == 1:
            self.avancar = 1
        else:
            self.avancar = 0

        #quando o sinal recebido do robo de que a gaveta foi entrtegue ter uma borda de subida, 
        if entregou != self.sinal:
            self.sinal = entregou
            #aumenta o numero de repetições (pegas e entregues) feitas caso o numero seja menor que o maximo (3 repeticoes para 3 ferramentas a serem entrehues). 
            if self.repeticoes < len(self.lista) and entregou == 1:
                self.repeticoes += 1
        #caso o numero de repetições seja igual ao tamanho da lista (3 ferramentas das 3 pedidas foram entregues)
        if self.repeticoes == len(self.lista):
            #define que o robo terminou seu trabalho
            self.terminou = 1

        return self.terminou, self.avancar

#classe que define se o robo deve pegar ou entregar, não utilizada na versão final
class QFazer:
    def __init__(self):
        self.valor = 1

    def obter_proximo_valor(self, PEGOU, ENTREGOU):
        #1 para pegar, 2 para entregar
        if PEGOU == 1 or ENTREGOU == 1:
            if (self.valor and not 1) or (not self.valor and 1):
                self.valor = 1
            else:
                self.valor = 0

        return self.valor

#função utilizada para servir como a ordem a ser utilizada na organização de listas acima
def chave_personalizada(item):
    return dicionario_gaveta[item]


#-----------------------------------------------------------------------------------------------------------------
                                                #Loop Principal
#-----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    payload_value = None  # Inicialize aqui
    try:
        #inicializa server
        print('Starting server...')
        server.start()
        print('Server is online')
        run()
        #define variavel que evita da mesma lista ficar sendo redefinida, pois quando isso acontece ela impede que o codigo avançe na gaveta a ser pegue
        INICIALIZAR = 0

        while True:
            #define que a lista a ser utilziada é a recebida do mqtt
            lista_envio = get_lista_mqtt(payload_value)
            #define que os valores enviados para o robo só serão redefinidos se a lista não for um valor vazio
            if payload_value is not None:
                #verifica se a lista (pedido do mqtt) ainda não foi utilizada pelo python, pois caso ela ja tenha sido utilizada as posicoes de pega e entrega ficariam sendo redefinidas, e a lista nunca avancaria
                if INICIALIZAR == 1:
                    lista_envio = get_lista_mqtt(payload_value)
                    tem_estoque = 1
                    #verifica se todas as ferramentas na lista estam disponiveis em estoque e armazena isso em uma variavel estoque
                    for ferramenta in lista_envio:
                        if estoque[ferramenta]> 0:
                           pass
                        else:
                            tem_estoque = 0
                            server.data_bank.set_input_registers(135, str(1))
                            time.sleep(1)
                            server.data_bank.set_input_registers(135, str(0)) 
                    #se a variavel estoque for 1, ou seja, todas as ferramentas estao em estoque, manda a lista para as classes para que essas possam definir os valores dos sinais mandados para o robo
                    if tem_estoque == 1:
                        for ferramenta in lista_envio:
                             estoque[ferramenta] = estoque[ferramenta] - 1
                        gaveta_handler = Gaveta(lista_envio)
                        entrega_handler = Entrega(lista_envio)
                        terminou_retorno = Terminou(lista_envio)
                        qfazer_handler = QFazer()
                        INICIALIZAR = 0
                        
                #leitura dos sinais vindos do robo
                pegou = server.data_bank.get_holding_registers(address=129)[0] #manda um sempre que o robo termina de pegar a gaveta
                entregou = server.data_bank.get_holding_registers(address=131)[0] #manda um sempre que o robo termina de entregar a gaveta
                PEGOU = pegou
                ENTREGOU = entregou

                #verifica (do python) a gaveta a ser pegue
                GAVETA = gaveta_handler.obter_proximo_valor(PEGOU)
                #manda o valor para o robo
                server.data_bank.set_input_registers(128, str(GAVETA))

                #verifica (do python) em que posicao a gaveta deve ser entregue
                POS_ENTREGA = entrega_handler.obter_proximo_valor(ENTREGOU)
                #manda o valor para o robo
                server.data_bank.set_input_registers(130, str(POS_ENTREGA))

                #verifica (do python) se todas as gavetas ja foram entregues
                RETORNO = terminou_retorno.obter_proximo_valor(ENTREGOU)
                TERMINAR = RETORNO[0]
                #manda o valor para o robo
                server.data_bank.set_input_registers(132, str(TERMINAR))

                #verifica (do python) se o robo deve entregar ou pegar a gaveta, nao esta sendo utilizado na versao final
                QFAZER = qfazer_handler.obter_proximo_valor(PEGOU, ENTREGOU)
                #manda o valor para o robo
                server.data_bank.set_input_registers(133, str(QFAZER))

                #verifica (do python) se o robo pode avancar para a proxima acao, nao esta sendo utilizado na versao final
                AVANCAR = RETORNO[1]
                #manda o valor para o robo
                server.data_bank.set_input_registers(134, str(AVANCAR))

                #prints para verificar condicoes de funcionamento
                print(estoque)
                print('Qual gaveta pegar:{};Qual posicao entregar:{};Terminou de pegar?:{};Terminou de entregar?:{};Acabar processo:{}; QFazer:{}, Avancar:{}'.format(GAVETA, POS_ENTREGA, PEGOU, ENTREGOU, TERMINAR, QFAZER, AVANCAR))
                sleep(0.5)

    #caso algo de errado, desliga o servidor
    except Exception as e:
        print(e)
        print('Shutting down server...')
        server.stop()
        print('Server is offline')