import time
from PyQt5.QtCore import *
import serial.tools.list_ports

# Main initializer
class Main(QThread):

    adddevice = pyqtSignal(int, str, str)
    deldevice = pyqtSignal(int, str)

    def __init__(self):
        self.devices = {}
        self.com = {}
        QThread.__init__(self)

    def run(self):
        ports = serial.tools.list_ports.comports();
        serial_number = []
        port_com = []
        for port in ports:
            i = 0
            while i < 257:
                temp = str(i)
                if port.description == 'Serieel USB-apparaat (COM' + temp + ')':
                    print("Arduino: " + port.serial_number[-4:])
                    serial_number.append(port.serial_number)
                    port_com.append(port.device)
                    if port.serial_number not in self.devices:
                        name = "Serial number " + port.serial_number[-4:]
                        temp = "Comport " + port.device
                        self.adddevice.emit(port.serial_number, name, port.device)
                        self.devices[port.serial_number] = {name}
                        self.com[port.device] = {temp}
                i += 1
        for key in list(self.devices.keys()):
            if key not in serial_number:
                for com in list(self.com.keys()):
                    if com not in port_com:
                        self.deldevice.emit(key, com)
                        del self.devices[key]
                        del self.com[com]
