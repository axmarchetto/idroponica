import sys

import paho.mqtt.client as mqtt  # import the client1
import time


def on_disconnect(client, userdata, flags, rc=0):
    m = "DisConnected flags" + "result code " + str(rc) + "client_id  "
    print(m)
    client.connected_flag = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print('connessione ok')
    else:
        print('connessiona a puttane', rc)
        client.bad_connection_flag = True


def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_message(client, userdata, message):
    print("message received:  ", message.topic, str(message.payload.decode("utf-8")))


# # The callback for when a PUBLISH message is received from the server.
# def on_message2(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))


keep_alive = 60
QOS1 = 1
QOS2 = 0
CLEAN_SESSION = False
port = 1883

mqtt.Client.connected_flag = False  # create a flag in the class
mqtt.Client.bad_connection_flag = False  # create a flag in the class
mqtt.Client.retry_count = 0  #

broker = "broker.hivemq.com"
# broker="192.168.1.184" #se ho un ip lo metto qua
client = mqtt.Client('python1')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log=on_log

run_main = False
run_flag = True


def gest_connessione():
    flag_connessione = True
    while not client.is_connected() and flag_connessione:
        try:
            print("connecting ", broker)
            client.connect(broker, port, keep_alive)  # connect to broker
            flag_connessione = True
            break  # break from while loop
        except:
            print("connection attempt failed will retry")
            time.sleep(1)
            client.retry_count += 1
            if client.retry_count > 2:
                flag_connessione = False
                break
    # print ('alla fine di gestione connessione ')
    # print('flag connessione:', flag_connessione)
    return flag_connessione


def gest_loop():
    flag_main = False
    client.loop_start()
    count = 0
    while True:
        #print(count)
        time.sleep(1)
        if client.is_connected():  # wait for connack
            client.retry_count = 0  # reset counter
            flag_main = True
            break
        if count > 5 or client.bad_connection_flag:  # don't wait forever
            client.loop_stop()  # stop loop
            client.retry_count += 1
            if client.retry_count > 3:
                flag_main = False
            break  # break from while loop
        # time.sleep(1)
        count += 1
    return flag_main

def gest_disconnessione():
    print("quitting")
    client.disconnect()
    client.loop_stop()



while run_flag:
   # print('run flag:', run_flag)

    run_flag = gest_connessione()
    if not run_main and run_flag:
        run_main = gest_loop()
    if run_main:
        try:
            # Do main loop
            print("in main loop")  # publish and subscribe here
            client.publish("casadiandrea/idroponica/valori", "prova ultima di adesso ")
            time.sleep(3)
            run_flag=False

            ##Added try block to catch keyborad interrupt  to break loop so we
            ##don't leave loop thread running.

        except(KeyboardInterrupt):
            print("keyboard Interrupt so ending")
            run_flag = False

gest_disconnessione()
