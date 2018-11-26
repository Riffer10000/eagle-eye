import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Traffic import Arduino

class Status_Window(QWidget):

    serial = None
    result = []
    T1 = None
    T2 = None
    T3 = None
    
    def __init__(self, port):
        super().__init__()
        self.serial = Arduino(port)
        self.result = self.serial.executor()
        self.initUI_Status()

    def initUI_Status(self):
        #labels
        L1 = QLabel('  Status:', self)
        L2 = QLabel('De huidige temperatuur is:', self)
        L3 = QLabel('De huidige lichtintensiteit is:', self)
        L4 = QLabel('De huidige afstand is:', self)

        R1 = QLabel(str(self.result[0]), self)
        R2 = QLabel(str(self.result[1]), self)
        R3 = QLabel(str(self.result[2]), self)

        self.T1 = R1
        self.T2 = R2
        self.T3 = R3

        BRefresh = QPushButton("Refresh", self)
        BRefresh.clicked.connect(self.refresh)

        #layout
        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(L1, -1, 0)
        grid.addWidget(L2, 2, 0)
        grid.addWidget(R1, 2, 1)
        grid.addWidget(L3, 3, 0)
        grid.addWidget(R2, 3, 1)
        grid.addWidget(L4, 4, 0)
        grid.addWidget(R3, 4, 1)

        self.setLayout(grid)

        #font
        font = QFont()
        font.setPointSize(11)

        self.setFont(font)

        self.setFixedSize(540, 450)
        self.center
        self.setWindowTitle('Status')
        self.setWindowIcon(QIcon('Gui_Icon.png'))
    
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def refresh(self):
        self.result = self.serial.executor()
        self.T1.setText(str(self.result[0]))
        self.T2.setText(str(self.result[1]))
        self.T3.setText(str(self.result[2]))

    def rollDown(self):
        self.serial.send_rollout()

    def rollIn(self):
        self.serial.send_rollin()

if __name__ == '__main__':

    App = QApplication(sys.argv)
    St_Window = Status_Window()
    St_Window.show()
    sys.exit(App.exec())
