from socket import timeout
import serial
import time

ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)
ser.flushInput()
data = []
while True:
    try:
        ser_bytes = ser.readline()
        if ser_bytes:
            string = ser_bytes.decode()  # convert the byte string to a unicode string
            num = int(string) # convert the unicode string to an int
            print(num)
            data.append(num)
    except KeyboardInterrupt:
        with open('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\acc_cough.txt', 'w') as f:
            for item in data:
                f.write("%s\n" % item)
