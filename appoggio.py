import time

from PyQt5.QtCore import pyqtSlot, QRunnable


class Worker(QRunnable):
    '''
    https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    Worker thread
    '''

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        time.sleep(5)
        print("Thread complete")