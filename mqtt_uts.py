import paho.mqtt.client as mqtt  # import the client1
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print('connessione ok')
    else:
        print('connessiona a puttane', rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


mqtt.Client.connected_flag=False # create a flag in the class
broker = "broker.hivemq.com"
# broker="192.168.1.184" #se ho un ip lo metto qua
client = mqtt.Client('python1')
client.on_connect = on_connect
#print('connecting to broker', broker)
client.connect(broker)
client.loop_start()
while not client.connected_flag:
    print('in wait loop')
    time.sleep(1)
print('in main loop')
client.publish("pippo/pluto/paperino", "Domani nevica")
time.sleep(4)
client.loop_stop()
client.disconnect()
