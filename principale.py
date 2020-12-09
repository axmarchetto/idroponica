import sys
import os
# import RPi.GPIO as GPIO

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

# qua importo il builder che esce da qtdesigner
# esempio
from interfaccia import Ui_MainWindow


class finestra(QtWidgets.QMainWindow):  # se la finestra è main.py allora non va widget
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # il codice va qua sotto
        # lancio la finestra che ho datto in qt designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # se metto qua una variabile funzuiona
        # variabili per riassumere lo stato della finestra
        self.uscite = {'acqua': 0, 'aria': 0, 'ventola': 0, 'pompaxy': 0, 'pompaphpiu': 0, 'pompaphmeno': 0, 'luci': 0}
        self.bandierine = {'autotimer': True, 'okacqua': True, 'okaria': True, 'crepuscolare': True, 'livacqua': True}
        self.valori = {'acc': 40, 'delta': 5, 'oraon': 9, 'minon': 0, 'oraoff': 21, 'minoff': 0, 'vbatt': 13.8,
                       'tacqua': 22.4, 'ph': 7, 'EC': 2600, 'isteresiluce': 10}

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

        self.variabile = -1
        # BOTTONI PER LA VENTOLA DELLA CPU
        self.ui.btnonfanpiu.clicked.connect(lambda: self.gest_temp_fan('acc', 'piu'))
        self.ui.btnonfanmeno.clicked.connect(lambda: self.gest_temp_fan('acc', 'meno'))
        self.ui.btndeltafanpiu.clicked.connect(lambda: self.gest_temp_fan('delta', 'piu'))
        self.ui.btndeltafanmeno.clicked.connect(lambda: self.gest_temp_fan('delta', 'meno'))
        # BOTTONI PER LA POMA ACQUA E ARIA
        self.ui.btnariaon.clicked.connect(lambda: self.gestione_manuale('aria', 'on'))
        self.ui.btnariaoff.clicked.connect(lambda: self.gestione_manuale('aria', 'off'))
        self.ui.btnpompaon.clicked.connect(lambda: self.gestione_manuale('acqua', 'on'))
        self.ui.btnpompaoff.clicked.connect(lambda: self.gestione_manuale('acqua', 'off'))
        # BOTTONI PER IL TIMER ACCENSIONE
        self.ui.btnonpiu.clicked.connect(lambda: self.gest_orario_on_off('oraon', 'minon', 'piu'))
        self.ui.btnonmeno.clicked.connect(lambda: self.gest_orario_on_off('oraon', 'minon', 'meno'))
        self.ui.btnoffpiu.clicked.connect(lambda: self.gest_orario_on_off('oraoff', 'minoff', 'piu'))
        self.ui.btnoffmeno.clicked.connect(lambda: self.gest_orario_on_off('oraoff', 'minoff', 'meno'))

        # metto il timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)  # in millisecondi

    # fine di init

    # GESTIONE DEI FLAG
    def chk_handler(self):
        # aggiorno la variabile sopra
        self.bandierine['autotimer'] = self.ui.ckbclockok.isChecked()
        self.bandierine['okacqua'] = self.ui.chkacquaok.isChecked()
        self.bandierine['okaria'] = self.ui.chkariaok.isChecked()
        self.bandierine['crepuscolare'] = self.ui.chkcrepuscolare.isChecked()
        print(self.bandierine)
        # abilitazione tasti manuale
        self.ui.btnpompaon.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnpompaoff.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnariaon.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnariaoff.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnlucion.setEnabled(not self.ui.chkcrepuscolare.isChecked())
        self.ui.btnlucioff.setEnabled(not self.ui.chkcrepuscolare.isChecked())

    def gest_orario_on_off(self, tipo, tasto, valore):
        # print('premunto '+tasto+' '+valore)
        if valore == 'piu':
            self.valori[tasto] = self.valori[tasto] + 15
            if self.valori[tasto] >= 60:
                self.valori[tasto] = 0
                self.valori[tipo] = self.valori[tipo] + 1
        if valore == 'meno':
            self.valori[tasto] = self.valori[tasto] - 15
            if self.valori[tasto] < 0:
                self.valori[tasto] = 45
                self.valori[tipo] = self.valori[tipo] - 1
        if tipo == 'oraon':
            self.ui.tmponmin.setProperty("value", self.valori[tasto])
            self.ui.tmponh.setProperty("value", self.valori[tipo])
        if tipo == 'oraoff':
            self.ui.tmpoffmin.setProperty("value", self.valori[tasto])
            self.ui.tmpoffh.setProperty("value", self.valori[tipo])

    def gest_timer_orario(self):
        time = QtCore.QTime.currentTime()
        accensione = QtCore.QTime(self.valori['oraon'], self.valori['minon'], 0)
        spegnimento = QtCore.QTime(self.valori['oraoff'], self.valori['minoff'], 0)
        if self.bandierine['autotimer']:
            if accensione <= time <= spegnimento:
                if self.bandierine['okacqua']:
                    self.uscite['acqua'] = 1
                if self.bandierine['okaria']:
                    self.uscite['aria'] = 1
            else:
                if self.bandierine['okacqua']:
                    self.uscite['acqua'] = 0
                if self.bandierine['okaria']:
                    self.uscite['aria'] = 0

    def gest_temp_fan(self, tasto, valore):
        if valore == 'piu':
            # print('premuto tasto piu')
            self.valori[tasto] = self.valori[tasto] + 1
            # print(str(self.cpufan[tasto]))
        else:
            # print('premuto tasto meno')
            self.valori[tasto] = self.valori[tasto] - 1
        if tasto == 'acc':
            self.ui.tmponfan.setProperty("value", self.valori[tasto])
        if tasto == 'delta':
            self.ui.tmpdeltafan.setProperty("value", self.valori[tasto])

    def gestione_manuale(self, cosa, stato):
        if stato == 'on':
            self.uscite[cosa] = 1
            # print('pompa ' + cosa + ' accesa')
            # print(self.uscite[cosa])
        else:
            self.uscite[cosa] = 0
            # print('pompa ' + cosa + ' spenta')
            # print(self.uscite[cosa])

    def measure_temp(self):
        # dat ogliere la stringa  e lasciare il comando che inizia con os per raspberry
        temp = "temp= 47.5 'C"  # os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace('temp=', '')
        temp = temp.replace("'C", '')
        self.ui.tmpcpu.setProperty("value", temp)
        return (float(temp))

    def gestventolacpu(self):
        cpuact = self.measure_temp()
        if cpuact >= self.valori['acc']:
            # print ('accensione ventola')
            self.ui.lblstatoventola.setText('Ventola accesa')
            # GPIO.output(self.cpuout, True)
            self.uscite['ventola'] = 1

        if cpuact <= (self.valori['acc'] - self.valori['delta']):
            self.ui.lblstatoventola.setText('Ventola spenta')
            # print ('spegnimento ventola')
            # GPIO.output(self.cpuout, False)
            self.uscite['ventola'] = 0
        # print(self.uscite['ventola'])

    def gest_vbatt(self):
        # print(self.valori['vbatt'])
        self.ui.tmpvbatt.setProperty("value", self.valori['vbatt'])
        # print('vbatt')

    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        if time.second() % 2 == 0:
            text = text[:2] + ' ' + text[3:]
        self.ui.lcdclock.display(text)
        self.gestventolacpu()
        self.chk_handler()
        self.gest_timer_orario()
        self.gest_vbatt()

        print(self.uscite)
        # print(self.valori)
        # print(self.bandierine)

    # il codice va qua sopra

    # self.show()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = finestra()
#     w.show()
#     sys.exit(app.exec_())
