# import RPi.GPIO as GPIO
# import os
# import ds18sensor
# togliere i commenti qua sopra per raspberry


from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool
import time
from interfaccia import Ui_MainWindow
from appoggio import Worker
import multithread


# qua importo il builder che esce da qtdesigner
# esempio


class finestra(QtWidgets.QMainWindow):  # se la finestra è main.py allora non va widget
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # il codice va qua sotto
        # lancio la finestra che ho datto in qt designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # variabili per riassumere lo stato della finestra
        self.uscite = {'acqua': 0, 'aria': 0, 'ventola': 0, 'pompaxy': 0, 'pompaphpiu': 0, 'pompaphmeno': 0, 'luci': 0}
        self.ingressi = {'increpusc': 0, 'inlvlminacqua': 0}
        self.bandierine = {'autotimer': True, 'okacqua': True, 'okaria': True, 'crepuscolare': True, 'livacqua': True}
        self.valori = {'acc': 40, 'delta': 5, 'oraon': 9, 'minon': 0, 'oraoff': 21, 'minoff': 0, 'vbatt': 13.8,
                       'tacqua': 22.4, 'ph': 7, 'EC': 2600, 'isteresi_luce': 10, 'freqchk': 15, 'phcorrettore': 5,
                       'fertxy': 5}
        self.sts_isteresi = [0, 0]
        self.master_counter = 1

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
        # BOTTONI PER ACCENSIONE LUCI MANUALE E ISTERESI ACCENSIONE
        self.ui.btnlucion.clicked.connect(lambda: self.gestione_manuale('luci', 'on'))
        self.ui.btnlucioff.clicked.connect(lambda: self.gestione_manuale('luci', 'off'))
        self.ui.btncrppiu.clicked.connect(lambda: self.gest_temp_fan('isteresi_luce', 'piu'))
        self.ui.btncrpmeno.clicked.connect(lambda: self.gest_temp_fan('isteresi_luce', 'meno'))
        # BOTTONI PER LA GESTIONE DI PH ETC
        self.ui.btnfchkpiu.clicked.connect(lambda: self.gest_temp_fan('freqchk', 'piu'))
        self.ui.btnfchkmeno.clicked.connect(lambda: self.gest_temp_fan('freqchk', 'meno'))
        self.ui.btnphpiu.clicked.connect(lambda: self.gest_temp_fan('phcorrettore', 'piu'))
        self.ui.btnphmeno.clicked.connect(lambda: self.gest_temp_fan('phcorrettore', 'meno'))
        self.ui.btnxypiu.clicked.connect(lambda: self.gest_temp_fan('fertxy', 'piu'))
        self.ui.btnxymeno.clicked.connect(lambda: self.gest_temp_fan('fertxy', 'meno'))
        # metto il timer per azioni una volta al secondo
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
        # abilitazione tasti manuale
        self.ui.btnpompaon.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnpompaoff.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnariaon.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnariaoff.setEnabled(not self.ui.ckbclockok.isChecked())
        self.ui.btnlucion.setEnabled(not self.ui.chkcrepuscolare.isChecked())
        self.ui.btnlucioff.setEnabled(not self.ui.chkcrepuscolare.isChecked())

    def gest_orario_on_off(self, tipo, tasto, valore):
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
            if accensione <= time <= spegnimento:  # confronta l'ora
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
            self.valori[tasto] = self.valori[tasto] + 1
        else:
            self.valori[tasto] = self.valori[tasto] - 1
        if tasto == 'acc':
            self.ui.tmponfan.setProperty("value", self.valori[tasto])
        if tasto == 'delta':
            self.ui.tmpdeltafan.setProperty("value", self.valori[tasto])
        if tasto == 'isteresi_luce':
            self.ui.tmpcrp.setProperty("value", self.valori[tasto])
        if tasto == 'freqchk':
            self.ui.tmpfchk.setProperty("value", self.valori[tasto])
        if tasto == 'phcorrettore':
            self.ui.tmpph.setProperty("value", self.valori[tasto])
        if tasto == 'fertxy':
            self.ui.tmpxy.setProperty("value", self.valori[tasto])

    def gestione_manuale(self, cosa, stato):
        if stato == 'on':
            self.uscite[cosa] = 1
            # print('pompa ' + cosa + ' accesa')
            print(self.uscite[cosa])
        else:
            self.uscite[cosa] = 0
            # print('pompa ' + cosa + ' spenta')
            # print(self.uscite[cosa])

    def measure_temp(self):  # della CPU
        # dat ogliere la stringa  e lasciare il comando che inizia con os per raspberry
        temp = "temp= 47.5 'C"  # os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace('temp=', '')
        temp = temp.replace("'C", '')
        self.ui.tmpcpu.setProperty("value", temp)
        return (float(temp))

    def gestventolacpu(self):
        cpuact = self.measure_temp()
        if cpuact >= self.valori['acc']:
            self.ui.lblstatoventola.setText('Ventola accesa')
            self.uscite['ventola'] = 1

        if cpuact <= (self.valori['acc'] - self.valori['delta']):
            self.ui.lblstatoventola.setText('Ventola spenta')
            self.uscite['ventola'] = 0

    def gest_vbatt(self):
        # print(self.valori['vbatt'])
        self.ui.tmpvbatt.setProperty("value", self.valori['vbatt'])
        # print('vbatt')

    def gest_tacqua(self):
        # DA TOGLIERE COMMENTO CON RASPBERRY
        # self.valori['tacqua'] = self.dstemp.read_Ctemp()
        self.ui.tmpacqua.setProperty("value", self.valori['tacqua'])

    def gest_lvlacqua(self):
        if self.ingressi['inlvlminacqua']:
            self.ui.lbllvl.setText('LIVELLO MINIMO')
            print('ATTENZIONE LIVELLO MINIMO ACQUA ')
        else:
            self.ui.lbllvl.setText('Livello OK')

    def gest_luce(self):
        if self.ingressi['increpusc'] != self.sts_isteresi[0]:
            if self.sts_isteresi[1] >= self.ui.tmpcrp.value():
                self.sts_isteresi[0] = self.ingressi['increpusc']
                self.sts_isteresi[1] = 0
            else:
                self.sts_isteresi[1] = self.sts_isteresi[1] + 1
                print(self.sts_isteresi[1])
        else:
            self.sts_isteresi[1] = 0
        if self.bandierine['crepuscolare']:
            self.uscite['luci'] = self.sts_isteresi[0]

    # GESTONE DEL MULTITHEREAD ESTERNO --- INIZIO
    def progress_fn(self, n):
        multithread.avanzamento_funz(n)
        # print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        messaggio = multithread.da_eseguire(self.uscite, progress_callback)
        self.ingressi['increpusc'] = messaggio[0]
        self.ingressi['inlvlminacqua'] = messaggio[1]
        self.valori['tacqua'] = messaggio[2]
        return messaggio

    def print_output(self, s):
        multithread.stampa_uscita_funz(s)

    def thread_complete(self):
        multithread.sottoprog_completato()

    def gest_multithread(self):
        worker = Worker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    # GESTONE DEL MULTITHEREAD ESTERNO --- FINE

    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        if time.second() % 2 == 0:
            text = text[:2] + ' ' + text[3:]
        self.ui.lcdclock.display(text)
        # Da eseguire una volta al secondo
        self.chk_handler()
        self.gest_luce()
        self.gest_lvlacqua()
        self.temporizzatore()
        self.gest_timer_orario()
        self.gestventolacpu()

    def temporizzatore(self):
        print(self.master_counter)
        if self.master_counter == 1:
            print('primo giro')
            self.gest_tacqua()
            self.gest_vbatt()
        if self.master_counter % 10 == 0:  # una volta ogni 10 sec
            self.gest_multithread()
            print('uno ogni 10')
        if self.master_counter % 60 == 0:  # una volta al minuto
            print('una volta al minuto ')
        if self.master_counter % 900 == 0:  # una volta ogni 15min
            self.gest_tacqua()
            self.gest_vbatt()
        if self.master_counter % 3600 == 0:  # una volta ogni 15min
            self.master_counter = 0
        self.master_counter += 1

    # il codice va qua sopra
