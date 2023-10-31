from nextpm_read import *
from settings import Settings
from mqtt import *
from gas_read import *

import time
import os 
from datetime import datetime
settings = Settings()



def utworz_plik_txt(nazwa_pliku,sciezka):
	
    try:
        with open(nazwa_pliku, 'w') as plik:
            plik.write("XDDD")
    except IOError:
        print('Lipa')

# przygotowanie połączenia z MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Połączenie z brokerem MQTT
client.connect(broker_address, broker_port)

# Czekanie na połączenie z brokerem
client.loop_start()

sciezka = "/home/pi/Documents/"
nazwa = utworz_plik_txt(f'{sciezka}123.txt',sciezka)

try:
    while True:
		
        # Publikowanie wiadomości jako zmienna dict na temacie publikacyjnym
        #random_number = random.randint(100, 150)
        #random_number = str(random_number)
        #message = {"key1": random_number, "key2": "300.22"}
        
        data = get_pm_data(settings.ser)
        #print(data)

        pm1 = data["pm1"]
        pm25 = data['pm25']
        pm10 = data['pm10']
        
        gas_val = gas_values(settings.czas_jednego_pomiaru_gazu, ADC)
        #print(gas_val["no2"])
        #no2 = no2.round(2)
        
        message = {"pm10": pm10, "pm25": pm25, "no2": gas_val["no2"], "o3": gas_val["o3"], "co": gas_val["co"], "so2": gas_val["so2"], "temp": gas_val["temp"]}
        print(message)
        client.publish(topic1, json.dumps(message))

        #client.publish(topic1, json.dumps(message))

        time.sleep(5)  # Oczekiwanie przed następnym publikowaniem
        
        
        
except KeyboardInterrupt:
    print('BŁĄD wysłania')
    pass

# Wyłączenie klienta MQTT
client.loop_stop()
client.disconnect()
