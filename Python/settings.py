import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Settings_Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI_Settings()
        

    def initUI_Settings(self):
        L1 = QLabel('Instellingen', self)
        LEmpty = QLabel('', self)

        #temperatuur
        LTemp = QLabel('Temperatuursensor', self)
        LETemp = QLineEdit(self)
        BTemp = QPushButton('Apply', self)
        
        #lichtintensiteit
        LLicht = QLabel('Lichtsensor', self)
        LELicht = QLineEdit(self)
        BLicht = QPushButton('Apply', self)

        #Layout
        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(L1, -1, 0)
        grid.addWidget(LETemp, 2, 0)
        grid.addWidget(LTemp, 2, 1)
        grid.addWidget(BTemp, 3, 0)
        grid.addWidget(LELicht, 4, 0)
        grid.addWidget(LLicht, 4, 1)
        grid.addWidget(BLicht, 5, 0)

        self.setLayout(grid)

        #font
        font = QFont()
        font.setPointSize(11)

        self.setFont(font)

        self.setFixedSize(540, 450)
        self.center
        self.setWindowTitle('Instellingen')
        self.setWindowIcon(QIcon('Gui_Icon.png'))
    
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    App = QApplication(sys.argv)
    Se_Window = Settings_Window()
    Se_Window.show()
    sys.exit(App.exec())
