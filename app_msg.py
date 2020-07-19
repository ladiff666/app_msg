from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import sys
from app_msg_d import Ui_MainWindow
from socket import AF_INET, socket, SOCK_STREAM,gethostname
from threading import Thread
import time
header = 10 
s = socket(AF_INET, SOCK_STREAM)
s.connect((gethostname(), 1235))

class thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    msg_rcv = pyqtSignal(str)
        
    def __del__(self):
        self.wait()
        
    def receive(self):
        while True :
            full_msg = ''
            new_msg = True
            while True:
                msg = s.recv(16)
                if len(msg.decode('utf-8')) > 0:
                    if new_msg:
                        print(msg)
                        msg_l = int(msg[:header])
                        new_msg = False
                    full_msg += msg.decode('utf-8')
                    if len(full_msg) - header == msg_l:
                        self.msg = full_msg[header:]
                        self.msg_rcv.emit(self.msg)
                        new_msg = True
                        full_msg = ''
    def run(self):
        self.receive()


class MainApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        self.thread = thread()
        self.thread.start()
        self.thread.msg_rcv.connect(self.update_msg)

    def send(self):
        msg = self.plainTextEdit.toPlainText()
        msg_send = f"{len(msg):<{header}}" + msg
        print(msg)
        self.plainTextEdit.setPlainText("")
        s.send(bytes(msg_send,'utf-8'))
        
        if msg == 'quit':
            print('ok')
            sys.exit()
            s.close()

    def update_msg(self,msg):
        print(msg)
        self.textBrowser.append(msg)
        
def main():
    app = QApplication(sys.argv)
    windows = MainApp()
    windows.show()
    app.exec_()


if __name__ == '__main__':
    main()
