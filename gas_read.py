from settings import Settings
from Lib import ADS1263
import RPi.GPIO as GPIO

import time
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

settings = Settings()




ADC = ADS1263.ADS1263()
    
		# The faster the rate, the worse the stability
		# and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
   exit()
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel 

def gas_values(czas_do_odliczenia, ADC):
	
	#tu trzeba ogarnąć co on bierze
    REF = 4.332     # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V


#NO2 consts
    no2_board_offset = 287.0
    no2_working_volt = -3.0
    no2_ref_volt = -3.0
    no2_electronic_offset = 285.0
    no2_sensitivity = 0.2628

	#ozon consts
    o3_board_offset = 398.0
    o3_working_volt = -4.0
    o3_ref_volt = -2.0
    o3_electronic_offset = 402.0
    o3_sensitivity = 0.30076
    o3_sensitivity2 = 0.26426

	#co consts
    co_board_offset = 398.0
    co_working_volt = -4.0
    co_ref_volt = -2.0
    co_electronic_offset = 402.0
    co_sensitivity = 0.30076
    co_sensitivity2 = 0.26426

	#so2 const 
    so2_board_offset = 398.0
    so2_working_volt = -4.0
    so2_ref_volt = -2.0
    so2_electronic_offset = 402.0
    so2_sensitivity = 0.30076
    so2_sensitivity2 = 0.26426

    no2_working = []
    no2_refer = []

    o3_working = []
    o3_refer = []

    so2_refer = []
    so2_working = []
				
    co_refer = []
    co_working = []
	
    try:
        # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
        # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
        #ADC = ADS1263.ADS1263()
    
		# The faster the rate, the worse the stability
		# and the need to choose a suitable digital filter(REG_MODE1)
        #if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
        #    exit()
        #ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel 

        channelList = [0, 1, 2, 3, 4, 5, 6, 7]  # The channel must be less than 10
	
        data = bme280.sample(bus, address, calibration_params)
        temp = data.temperature
        #temp = -5       
    #Sprawdzenie współczynnika kt z temperaturą
        if temp > 0:
            a8 = 2.25694444444445e-12
            a7 = -2.19246031746032e-10
            a6 = 2.11805555555555e-09
            a5 = 3.23611111111112e-07
            a4 = -6.53298611111111e-06
            a3 = -0.000132430555555556
            a2 = 0.00312986111111111
            a1 = 0.0352261904761905
            a0 = 0.200000000000000
            no2_kt = (a8*temp**8)+(a7*temp**7)+(a6*temp**6)+(a5*temp**5)+(a4*temp**4)+(a3*temp**3)+(a2*temp**2)+(a1*temp)+a0
        else:
            no2_kt = 0.2
        
        if temp >= 0:
            a6 = 5.5556e-10
            a5 = 1.5e-07
            a4 = 1.0139e-05
            a3 = -2e-04
            a2 = 4.8056e-04
            a1 = 0.0465
            a0 = 0.300000000000000
            o3_kt = (a6*temp**6)+(a5*temp**5)+(a4*temp**4)+(a3*temp**3)+(a2*temp**2)+(a1*temp)+a0
        elif temp<0 and temp>-10:
            o3_kt = (0.01*temp) + 0.3
        else:
            o3_kt = 0.1
        
        if temp < 0:
            co_nT = 1
        elif temp>0 and temp<30:
            a3 = -6.6667e-05
            a2 = 0.0045
            a1 = -0.1583
            a0 = 1   
            co_nT = (a3*temp**3)+(a2*temp**2)+(a1*temp)+a0   
        else:
            co_nT = -1.5
            
        if temp < 20:
            so2_kt = 0
        elif temp >= 20 and temp < 30:
            so2_kt = (temp/2)-5
        else:
            so2_kt = (temp * 2) - 55
    #Odczyt napięcia z ADC
                
        # get ADC1 value
                
        #czas_do_odliczenia = settings.czas_jednego_pomiaru_gazu
        i = 0
        while czas_do_odliczenia > 0:

		

  
            ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value

            no2_working.append(ADC_Value[0] * REF / 0x7fffffff)
            no2_refer.append(ADC_Value[1] * REF / 0x7fffffff)
        
            o3_working.append(ADC_Value[2] * REF / 0x7fffffff)
            o3_refer.append(ADC_Value[3] * REF / 0x7fffffff)
            
            so2_refer.append(ADC_Value[4] * REF / 0x7fffffff)
            so2_working.append(ADC_Value[5] * REF / 0x7fffffff)
            
            co_refer.append(ADC_Value[6] * REF / 0x7fffffff)
            co_working.append(ADC_Value[7] * REF / 0x7fffffff)
            

            
            
            czas_do_odliczenia -= settings.krok_czasowy
        
            time.sleep(settings.krok_czasowy)
        #ADC.ADS1263_Exit()
        
    except IOError as e:
        print(e)
        
    # Obliczenie srednich
         
    no2_working_mean = sum(no2_working)/(len(no2_working))
    no2_refer_mean = sum(no2_refer)/(len(no2_refer))
	
    o3_working_mean = sum(o3_working)/(len(o3_working))
    o3_refer_mean = sum(o3_refer)/(len(o3_refer))
	
    co_working_mean = sum(o3_working)/(len(o3_working))
    co_refer_mean = sum(o3_refer)/(len(o3_refer))
	
    so2_working_mean = sum(o3_working)/(len(o3_working))
    so2_refer_mean = sum(o3_refer)/(len(o3_refer))
	
	
	# Zamiana warosci z mV na V
    no2_working_mean = no2_working_mean*1000
    no2_refer_mean = no2_refer_mean*1000
    
    o3_working_mean = o3_working_mean*1000
    o3_refer_mean = o3_refer_mean*1000
    
    co_working_mean = co_working_mean * 1000
    co_refer_mean = co_refer_mean * 1000
	
    so2_working_mean = so2_working_mean * 1000
    so2_refer_mean = so2_refer_mean * 1000
    
    # Obliczenie zgodnie z algorytmem        
    no2_WEc = (no2_working_mean - no2_board_offset) - (no2_working_volt - no2_ref_volt) - (no2_kt * (no2_refer_mean - no2_electronic_offset))
    
    o3_WEc = (o3_working_mean - o3_board_offset) - (o3_working_volt - o3_ref_volt) - (o3_kt * (o3_refer_mean - o3_electronic_offset))
    
    co_Wec = (co_working_mean - co_board_offset) - ( co_nT * (co_refer_mean - co_electronic_offset))
    
    so2_Wec = (so2_working_mean - so2_board_offset) - so2_working_volt - so2_kt
    
    #Wynik pomiaru
    o3_measure = (o3_WEc/o3_sensitivity)/1000          
    no2_measure = no2_WEc/no2_sensitivity
    co_measure = co_Wec/co_sensitivity
    so2_measure = so2_Wec/so2_sensitivity
    
    #zaokraglone
    no2_measure = round(no2_measure, 2)
    o3_measure = round(o3_measure, 2)     
    co_measure = round(co_measure, 2)
    so2_measure = round(so2_measure, 2)
    temp = round(temp, 2)
    #print(temp)
    gases = {"no2": no2_measure, "o3": o3_measure, "co": co_measure, "so2": so2_measure, "temp": temp}
    #print(gases)
    return(gases)




#a=gas_values(settings.czas_jednego_pomiaru_gazu, ADC)
#print(a)
#b=gas_values(settings.czas_jednego_pomiaru_gazu, ADC)
#print(b)


