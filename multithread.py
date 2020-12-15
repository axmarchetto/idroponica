# import RPi.GPIO as GPIO
#
# USCITE

# cpuout = 11
# uscitaacqua = 40
# uscitaaria = 38
# uscitaluci = 36
#
# GPIO.setwarnings(False)  # disable warnings
# GPIO.setmode(GPIO.BOARD)  # set pin numbering system
#
# GPIO.setup(cpuout, GPIO.OUT)
# GPIO.setup(uscitaacqua, GPIO.OUT)
# GPIO.setup(uscitaaria, GPIO.OUT)
# GPIO.setup(uscitaluci, GPIO.OUT)
#
# GPIO.output(cpuout, False)
# GPIO.output(uscitaacqua, False)
# GPIO.output(uscitaaria, False)
# GPIO.output(uscitaluci, False)

# INGRESSI


def avanzamento_funz(n):
    print("%d%% done" % n)


def da_eseguire(pass_valori, progress_callback):
    ingressi = [0, 0]
    print(pass_valori)
    if pass_valori['ventola']:
        # GPIO.output(cpuout, True)
        mess = 'ventola accesa, '
    else:
        # GPIO.output(cpuout, False)
        mess = 'ventola spenta, '

    if pass_valori['acqua']:
        # GPIO.output(uscitaacqua, True)
        mess = mess + 'pompa acqua accesa, '
    else:
        # GPIO.output(uscitaacqua, False)
        mess = mess + 'pompa acqua spenta, '

    if pass_valori['aria']:
        # GPIO.output(uscitaaria, True)
        mess = mess + 'pompa aria accesa, '
    else:
        # GPIO.output(uscitaaria, False)
        mess = mess + 'pompa aria spenta, '

    if pass_valori['luci']:
        # GPIO.output(uscitaluci, True)
        mess = mess + 'luci accese'
    else:
        # GPIO.output(uscitaluci, False)
        mess = mess + 'luci spente'

    return ingressi


def stampa_uscita_funz(s):
    print(s)


def sottoprog_completato():
    print("THREAD COMPLETE!")
