def avanzamento_funz(n):
    print("%d%% done" % n)


def da_eseguire(pass_valori,progress_callback):

    if pass_valori['ventola']:
         # GPIO.output(self.cpuout, True)
         mess = 'ventola accesa'
    else:
         # GPIO.output(self.cpuout, False)
         mess = 'ventola spenta'
    return mess


def stampa_uscita_funz(s):
    print(s)

def sottoprog_completato():
    print("THREAD COMPLETE!")

