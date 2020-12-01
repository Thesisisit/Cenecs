import RPi.GPIO as GPIO
import serial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
print("Press the button")
arduinoData = serial.Serial('/dev/ttyUSB1', 19200, timeout=2)
while 1:
   GPIO.output(7,GPIO.HIGH)
   
GPIO.cleanup()