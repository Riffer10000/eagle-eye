import serial
import threading
from PyQt5.QtCore import *
import time
import struct
import codecs

class Arduino(QObject):

    successmsg = pyqtSignal(str)
    failedsmsg = pyqtSignal(str)

    tempmsg = pyqtSignal(int)
    lightmsg = pyqtSignal(int)
    distmsg = pyqtSignal(int)

    result = None
    
    def __init__(self, port):
        self.ser = serial.Serial(port=port,
                                 baudrate=19200)
        self.cmd = []
        self.instr = None
        self.codes = {
            '69': self.return_failed,
            '8': self.return_current_temp,
            '9': self.return_current_distance,
            '7': self.return_current_light,
            '6': self.send_rollout,
            '5': self.send_rollin
        }
        QObject.__init__(self)
        time.sleep(2)
        QTimer.singleShot(0,self.executor)

    def get_result(self, resul):
        resul = int(resul)
        return resul
    
    def executor(self):
        self.get_current_temp()
        result1 = self.get_result(self.result)
        result1 = int(result1 / 2)
        self.get_current_light()
        result2 = self.get_result(self.result)
        self.get_current_distance()
        result3 = self.get_result(self.result)
        return result1, result2, result3
    
    # Send hex instruction to ard
    def send_instruction(self, instruction):
        try:
            time.sleep(0.1)
            self.instr = instruction
            cmd = self.instr
            cmd = str(cmd)
            print("Pyhton transmits:", cmd)
            self.ser.write(bytes(cmd.encode('ascii')))
            self.stop = False
            self.listen()
        except:
            pass

    # Listens to incoming serial connection
    def listen(self):
        while not self.stop:
            char = self.ser.read(1)
            char = ord(char)
            print("Arduino returns:" , char)
            self.cmd.append(char)
            self.result = char
            self.stop = True

    def return_success(self):
        self.successmsg.emit("Success")

    def return_failed(self):
        self.failedmsg.emit("Failed")

    def return_current_temp(self, temp):
        self.tempmsg.emit(temp)

    def return_current_light(self, light):
        self.lightmsg.emit(light)

    def return_current_distance(self, distance):
        self.distmsg.emit(distance)

    # Requests current temperature from Arduino
    def get_current_temp(self):
        self.send_instruction(8)

    # Requests current distance from Arduino
    def get_current_distance(self):
        self.send_instruction(9)

    # Requests currently measured light intensity
    def get_current_light(self):
        self.send_instruction(7)

    # Sends roll-down command to Arduino
    def send_rollout(self):
        self.send_instruction(6)

    # Sends roll-up command to Arduino
    def send_rollin(self):
        self.send_instruction(5)
