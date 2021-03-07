
import serial
import time
import sys
import os
import re

e = 't0.txt=\"1234567890\"'
#e='123456789'
f=b'\xff\xff\xff' #questa cosi funziona come terminatore

e=e.encode("ascii", "replace")
print(e)
print(type(e))
print(f)
print(type(f))
#ser = serial.Serial('COM4', 9600)
ser=serial.Serial(
    port='COM4',
    baudrate =38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=3,
    writeTimeout=3)
#ser.write(str.encode('t0.txt=ÿÿÿ '))
ser.write(e+f)

print(e)
#'t0.txt=\"prova\"ÿÿÿ '

# if 'comok' in r:
#     print('Connected with baudrate: ' + str(baudrate) + '...')
#     noConnect = False
#     status, unknown1, model, fwversion, mcucode, serial, flashSize = r.strip("\xff\x00").split(',')
#     print('Status: ' + status.split(' ')[0])
#     if status.split(' ')[1] == "1":
#         print('Touchscreen: yes')
#     else:
#         print('Touchscreen: no')
#     print('Model: ' + model)
#     print('Firmware version: ' + fwversion)
#     print('MCU code: ' + mcucode)
#     print('Serial: ' + serial)
#     print('Flash size: ' + flashSize)
#     if fSize and fSize > flashSize:
#         print('File too big!')
#         return False
#     if checkModel and not checkModel in model:
#         print('Wrong Display!')
#         return False
#     return True

