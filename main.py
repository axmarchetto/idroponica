import sys

from PyQt5 import QtWidgets

from principale import finestra

#da togliere i commenti su raspberry
# import RPi.GPIO as GPIO


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = finestra()
    w.show()
    sys.exit(app.exec_())

