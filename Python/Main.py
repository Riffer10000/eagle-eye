import sys
import time
from Connection import Main
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from settings import Settings_Window
from status import Status_Window
from Traffic import Arduino

class Main_Window(QWidget):
    
    serial = Main()
    grid = QGridLayout()
    connectedDevices = []
    connectedCOM = []
    connectedLabels = []
    unconnectedLabels = []
    b0 = False
    b1 = False
    b2 = False
    b3 = False
    b4 = False
    
    def __init__(self):
        super().__init__()
        self.devices = {}
        
        LArd1 = QLabel("disconnected", self)
        Label_1 = QLabel("Arduino 1: ", self)
        LArd2 = QLabel("disconnected", self)
        Label_2 = QLabel("Arduino 2: ", self)
        LArd3 = QLabel("disconnected", self)
        Label_3 = QLabel("Arduino 3: ", self)
        LArd4 = QLabel("disconnected", self)
        Label_4 = QLabel("Arduino 4: ", self)
        LArd5 = QLabel("disconnected", self)
        Label_5 = QLabel("Arduino 5: ", self)

        self.grid.addWidget(Label_1, 2, 0)
        self.grid.addWidget(LArd1, 2, 1)
        self.grid.addWidget(Label_2, 3, 0)
        self.grid.addWidget(LArd2, 3, 1)
        self.grid.addWidget(Label_3, 4, 0)
        self.grid.addWidget(LArd3, 4, 1)
        self.grid.addWidget(Label_4, 5, 0)
        self.grid.addWidget(LArd4, 5, 1)
        self.grid.addWidget(Label_5, 6, 0)
        self.grid.addWidget(LArd5, 6, 1)

        self.unconnectedLabels.append(LArd1)
        self.unconnectedLabels.append(LArd2)
        self.unconnectedLabels.append(LArd3)
        self.unconnectedLabels.append(LArd4)
        self.unconnectedLabels.append(LArd5)
        
        self.serial.adddevice.connect(self.addDevice)
        self.serial.deldevice.connect(self.deleteDevice)

        self.initUI()
        self.serial.run()
    
    def initUI(self):
        # Label variables
        l1 = QLabel("Zonneschermen:", self)

        # Button Variables
        BSettings = QPushButton("Settings", self)
        BSettings.clicked.connect(self.Open_Settings)
        BQuit = QPushButton("Exit", self)
        BQuit.clicked.connect(self.Close_Program)
        BStatus0 = QPushButton("Status", self)
        BStatus0.clicked.connect(self.Open_Status0)
        BStatus1 = QPushButton("Status", self)
        BStatus1.clicked.connect(self.Open_Status1)
        BStatus2 = QPushButton("Status", self)
        BStatus2.clicked.connect(self.Open_Status2)
        BStatus3 = QPushButton("Status", self)
        BStatus3.clicked.connect(self.Open_Status3)
        BStatus4 = QPushButton("Status", self)
        BStatus4.clicked.connect(self.Open_Status4)
        BRefresh = QPushButton("Refresh", self)
        BRefresh.clicked.connect(self.refresh)
        BRolldown0 = QPushButton("Rollout", self)
        BRolldown0.clicked.connect(self.roll_Down0)
        BRollin0 = QPushButton("Rollin", self)
        BRollin0.clicked.connect(self.roll_In0)
        BRolldown1 = QPushButton("Rollout", self)
        BRolldown1.clicked.connect(self.roll_Down1)
        BRollin1 = QPushButton("Rollin", self)
        BRollin1.clicked.connect(self.roll_In1)
        BRolldown2 = QPushButton("Rollout", self)
        BRolldown2.clicked.connect(self.roll_Down2)
        BRollin2 = QPushButton("Rollin", self)
        BRollin2.clicked.connect(self.roll_In2)
        BRolldown3 = QPushButton("Rollout", self)
        BRolldown3.clicked.connect(self.roll_Down3)
        BRollin3 = QPushButton("Rollin", self)
        BRollin3.clicked.connect(self.roll_In3)
        BRolldown4 = QPushButton("Rollout", self)
        BRolldown4.clicked.connect(self.roll_Down4)
        BRollin4 = QPushButton("Rollin", self)
        BRollin4.clicked.connect(self.roll_In4)

        # QGridLayout

        self.grid.setSpacing(50)

        self.grid.addWidget(l1, 1, 0)
        self.grid.addWidget(BRefresh, 1, 1)

        self.grid.addWidget(BStatus0, 2, 2)
        self.grid.addWidget(BRolldown0, 2, 3)
        self.grid.addWidget(BRollin0, 2, 4)
        
        self.grid.addWidget(BStatus1, 3, 2)
        self.grid.addWidget(BRolldown1, 3, 3)
        self.grid.addWidget(BRollin1, 3, 4)
        
        self.grid.addWidget(BStatus2, 4, 2)
        self.grid.addWidget(BRolldown2, 4, 3)
        self.grid.addWidget(BRollin2, 4, 4)
        
        self.grid.addWidget(BStatus3, 5, 2)
        self.grid.addWidget(BRolldown3, 5, 3)
        self.grid.addWidget(BRollin3, 5, 4)
        
        self.grid.addWidget(BStatus4, 6, 2)
        self.grid.addWidget(BRolldown4, 6, 3)
        self.grid.addWidget(BRollin4, 6, 4)
        
        h_box1 = QHBoxLayout()
        h_box1.addWidget(BSettings)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(BQuit)

        v_box = QVBoxLayout()
        v_box.addLayout(self.grid)
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)

        self.setLayout(v_box)

        #font
        font = QFont()
        font.setPointSize(11)

        self.setFont(font)

        self.resize(720, 600)
        self.center
        self.setWindowTitle('Zonnescherm UI')
        self.setWindowIcon(QIcon('Gui_Icon.png'))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def addDevice(self, serialn, name, port):
        self.connectedDevices.append(serialn)
        self.connectedCOM.append(port)
        i = 0
        index = len(self.connectedDevices)
        for device in self.connectedDevices:
            for label in self.unconnectedLabels:
                if i < 1:
                    doc = QTextDocument()
                    doc.setHtml(label.text())
                    qtext = doc.toPlainText()
                    if device == qtext:
                        print("success")
                    if device != qtext:
                        temp = str(serialn)
                        label.setText(temp)
                        self.connectedLabels.append(label)
                        self.unconnectedLabels.remove(label)
                i += 1

    def deleteDevice(self, serialn, port):
        for com in self.connectedCOM:
            if com == port:
                self.connectedCOM.remove(port)
                
        for label in self.connectedLabels:
            doc = QTextDocument()
            doc.setHtml(label.text())
            qtext = doc.toPlainText()
            if int(serialn) == int(qtext):
                i = 0
                while i < 6:
                    if label == self.connectedLabels[i]:
                        if i == 0:
                            self.b0 = bool(False)
                        label.setText("Disconnected")
                        self.unconnectedLabels.insert(i, label)
                        self.connectedLabels.remove(label)
                        self.connectedDevices.remove(serialn)
                        i = 0
                        return
                    i += 1

    def refresh(self):
        self.serial.run()

    def Open_Settings(self):
        self.SeW = Settings_Window()
        self.SeW.show()

    def Close_Program(self):
        sys.exit(1)

    def Open_Status0(self):
        if len(self.connectedCOM) >= 1:
            if self.b0 == False:
                self.StW0 = Status_Window(self.connectedCOM[0])
            else:
                self.StW0.refresh()
            self.StW0.show()
            self.b0 = bool(True)

    def Open_Status1(self):
        if len(self.connectedCOM) >= 2:
            if self.b1 == False:
                self.StW1 = Status_Window(self.connectedCOM[1])
            else:
                self.StW1.refresh()
            self.StW1.show()
            self.b1 = bool(True)
            
    def Open_Status2(self):
        if len(self.connectedCOM) >= 3:
            if self.b2 == False:
                self.StW2 = Status_Window(self.connectedCOM[2])
            else:
                self.StW2.refresh()
            self.StW2.show()
            self.b2 = bool(True)

    def Open_Status3(self):
        if len(self.connectedCOM) >= 4:
            if self.b3 == False:
                self.StW3 = Status_Window(self.connectedCOM[3])
            else:
                self.StW3.refresh()    
            self.StW3.show()
            self.b3 = bool(True)

    def Open_Status4(self):
        if len(self.connectedCOM) >= 5:
            if self.b4 == False:
                self.StW4 = Status_Window(self.connectedCOM[4])
            else:
                self.StW4.refresh()
            self.StW4.show()
            self.b4 = bool(True)

    def roll_Down0(self):
        if len(self.connectedCOM) >= 1:
            if self.b0 == False:
                self.StW0 = Status_Window(self.connectedCOM[0])
                self.StW0.rollDown()
            else:
                self.StW0.rollDown()
            self.b0 = bool(True)

    def roll_In0(self):
        if len(self.connectedCOM) >= 1:
            if self.b0 == False:
                self.StW0 = Status_Window(self.connectedCOM[0])
                self.StW0.rollIn()
            else:
                self.StW0.rollIn()
            self.b0 = bool(True)

    def roll_Down1(self):
        if len(self.connectedCOM) >= 2:
            if self.b1 == False:
                self.StW1 = Status_Window(self.connectedCOM[1])
                self.StW1.rollDown()
            else:
                self.StW1.rollDown()
            self.b1 = bool(True)

    def roll_In1(self):
        if len(self.connectedCOM) >= 2:
            if self.b1 == False:
                self.StW1 = Status_Window(self.connectedCOM[1])
                self.StW1.rollIn()
            else:
                self.StW1.rollIn()
            self.b1 = bool(True)

    def roll_Down2(self):
        if len(self.connectedCOM) >= 3:
            if self.b2 == False:
                self.StW2 = Status_Window(self.connectedCOM[2])
                self.StW2.rollDown()
            else:
                self.StW2.rollDown()
            self.b2 = bool(True)

    def roll_In2(self):
        if len(self.connectedCOM) >= 3:
            if self.b2 == False:
                self.StW2 = Status_Window(self.connectedCOM[2])
                self.StW2.rollIn()
            else:
                self.StW2.rollIn()
            self.b2 = bool(True)

    def roll_Down3(self):
        if len(self.connectedCOM) >= 4:
            if self.b3 == False:
                self.StW3 = Status_Window(self.connectedCOM[3])
                self.StW3.rollDown()
            else:
                self.StW3.rollDown()
            self.b3 = bool(True)

    def roll_In3(self):
        if len(self.connectedCOM) >= 4:
            if self.b3 == False:
                self.StW3 = Status_Window(self.connectedCOM[3])
                self.StW3.rollIn()
            else:
                self.StW3.rollIn()
            self.b3 = bool(True)

    def roll_Down4(self):
        if len(self.connectedCOM) >= 5:
            if self.b4 == False:
                self.StW4 = Status_Window(self.connectedCOM[4])
                self.StW4.rollDown()
            else:
                self.StW4.rollDown()
            self.b4 = bool(True)

    def roll_In4(self):
        if len(self.connectedCOM) >= 5:
            if self.b4 == False:
                self.StW4 = Status_Window(self.connectedCOM[4])
                self.StW4.rollIn()
            else:
                self.StW4.rollIn()
            self.b4 = bool(True)

if __name__ == '__main__':

    App = QApplication(sys.argv)
    M_Window = Main_Window()
    M_Window.show()
    sys.exit(App.exec())
