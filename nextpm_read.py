import serial
from time import sleep


def get_data(ser, read_data_frame, output_length):
    ser.write(read_data_frame)
    #print(read_data_frame)
    data = []
    for i in range(output_length):
        output = ser.read()
        data.append(int.from_bytes(output, "big"))
    #print(data)
    return data


def get_pm(pm_bytes):
    return (pm_bytes[0] * 256 + pm_bytes[1]) / 10


def get_pm_data(ser):
    frame = [0x81, 0x11, 0x6E]

    output = get_data(ser, frame, 16)
    #print(output)
    pm1 = output[9:11]
    pm25 = output[11:13]
    pm10 = output[13:15]
    checksum = output[15]
    checksum2 = sum(output) % 0x100

    #print(pm1)
	
    pm1 = get_pm(pm1)
    pm25 = get_pm(pm25)
    pm10 = get_pm(pm10)
    return {"pm1": pm1, "pm25": pm25, "pm10": pm10}


if __name__ == '__main__':
    # port='/dev/ttyS0',
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)

    #while True:
     #   sleep(1)
      #  data = get_pm_data(ser)
      #  print(data)

