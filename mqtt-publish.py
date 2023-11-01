import ssl
import time
import psutil
import json
import math
import paho.mqtt.client as mqtt_client

broker = "aspvpxjmfalxx-ats.iot.us-east-1.amazonaws.com"
port = 443
topic = "sala/terreo/temperatura"
client_id = f'Leo-00010'

ca = "certs/AmazonRootCA1.pem" 
cert = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-certificate.pem.crt"
private = "certs/6f963f6ec45fbc59ebb98cf9df943424944b334aec0a18ce0f2e7f5d256530c9-private.pem.key"

def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

def connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    ssl_context = ssl_alpn()
    client.tls_set_context(context=ssl_context)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish_PCstatus(client):
    while True:
        topic = "iot/pc_monitor/macbook/system_info"
        battery = psutil.sensors_battery()
        memory = psutil.virtual_memory()

        message_json = json.dumps({
                "time": int(time.time()),
                "hostname": "notebook_leonardo",
                "cpu": psutil.cpu_percent(),
                "cpu_count": psutil.cpu_count(), 
                "battery": battery.percent,
                "power": battery.power_plugged,
                "memory": str( math.floor( memory.total / 1024 / 1000000 ) ) + "GB"
            })

        result = client.publish(topic, message_json,0)

        print(message_json)
        if result[0] == 0:
            print(f"Message Sent to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(1)
        
        
def publish(client):
    while True:
        topic = "iot/pc_monitor/macbook/system_info"
        battery = psutil.sensors_battery()
        memory = psutil.virtual_memory()

        message_json = json.dumps({
                "time": int(time.time()),
                "hostname": "notebook_leonardo",
                "cpu": psutil.cpu_percent(),
                "cpu_count": psutil.cpu_count(), 
                "battery": battery.percent,
                "power": battery.power_plugged,
                "memory": str( math.floor( memory.total / 1024 / 1000000 ) ) + "GB"
            })

        result = client.publish(topic, message_json,0)

        print(message_json)
        if result[0] == 0:
            print(f"Message Sent to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(1)

def run():
    client = connect()
    client.loop_start()
    publish_PCstatus(client)
    client.loop_forever()

run()
