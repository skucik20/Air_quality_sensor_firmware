import serial

class Settings:
	"""W tej klasie będą ustawienia"""
	
	def __init__(self):
		
		# dane serial portu
		self.ser = serial.Serial(
				port='/dev/ttyUSB0',
				baudrate=115200,
				parity=serial.PARITY_EVEN,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS,
				timeout=0.1)
		# ramka bitowa
		
		self.czas_jednego_pomiaru_gazu = 0.5 # sekundy
		self.krok_czasowy = 0.01 #sekundy
