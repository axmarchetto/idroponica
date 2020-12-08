import sys

# import RPi.GPIO as GPIO

from principale import finestra
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = finestra()
    w.show()
    sys.exit(app.exec_())

# setto le gariabili del raspberry, attebzioen quando lo fai su PC
# self.cpuout = 12  # PWM pin connected to LED
# self.uscitaacua=5
# self.uscitaaria=6
# GPIO.setwarnings(False)  # disable warnings
# GPIO.setmode(GPIO.BOARD)  # set pin numbering system
# GPIO.setup(self.cpuout, GPIO.OUT)
# GPIO.setup(self.uscitaacua, GPIO.OUT)
# GPIO.setup(self.uscitaaria, GPIO.OUT)
# GPIO.output(self.cpuout, False)
# GPIO.output(self.uscitaacua, False)
# GPIO.output(self.uscitaaria, False)