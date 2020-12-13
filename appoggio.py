import time

from PyQt5.QtCore import pyqtSlot, QRunnable, pyqtSignal, QObject

import traceback, sys

class WorkerSignals(QObject):

    ''' Defines the signals available from a running worker thread.
    PYTHON
    Supported signals are:

    finished
    No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)



class Worker(QRunnable):
    '''
    https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    Worker thread
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done