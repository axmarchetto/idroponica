import time

from PyQt5.QtCore import pyqtSlot, QRunnable


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


    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        self.fn(*self.args, **self.kwargs)
        #time.sleep(5)
        print("Thread complete")