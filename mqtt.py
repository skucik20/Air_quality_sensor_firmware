import time
import json
import paho.mqtt.client as mqtt
import random


# Dane do połączenia z brokerem MQTT
broker_address = "broker.mqttdashboard.com"
broker_port = 1883
client_id = "moj_klient"
 
# Tematy
topic1 = "NEXTPM"
topic2 = "temat/subskrybowany"


# Funkcja wywoływana po połączeniu z brokerem MQTT
def on_connect(client, userdata, flags, rc):
    print("Połączono z kodem: " + str(rc))
    #client.subscribe(topic1)

# Funkcja wywoływana po otrzymaniu wiadomości z subskrybowanego tematu
def on_message(client, userdata, msg):
    print("Odebrano wiadomość: " + msg.topic + " " + str(msg.payload))
    # received_message = json.loads(msg.payload)
    # print("Pierwsza pozycja (key1):", received_message["key1"])
    # print(type(received_message))

# Tworzenie klienta MQTT


#try:
    #while True:
		
        # Publikowanie wiadomości jako zmienna dict na temacie publikacyjnym
        #random_number = random.randint(100, 150)
        #random_number = str(random_number)
        #message = {"key1": random_number, "key2": "300.22"}
        #print('xd')
        #client.publish(topic1, json.dumps(message))

        #time.sleep(5)  # Oczekiwanie przed następnym publikowaniem

#except KeyboardInterrupt:
##    print('BŁĄD wysłania')
 #   pass

# Wyłączenie klienta MQTT
#client.loop_stop()
#client.disconnect()
