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


def gest_multithread(self):
    worker = Worker(self.execute_this_fn)
    worker.signals.result.connect(self.print_output)
    worker.signals.finished.connect(self.thread_complete)
    worker.signals.progress.connect(self.progress_fn)
    self.threadpool.start(worker)