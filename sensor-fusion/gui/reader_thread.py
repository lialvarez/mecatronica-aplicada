import csv
import datetime
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
from struct import *


class ReaderThread(QThread):
    update_signal = pyqtSignal(tuple)
    ser = serial.Serial()
    Paused = False

    def __init__(self, serial_conf):
        QThread.__init__(self)

        self.serial_conf = serial_conf

        # configure and open serial port
        self.ser.baudrate = self.serial_conf["baudrate"]
        self.ser.port = self.serial_conf["port"]
        self.ser.open()

    def __del__(self):
        self.wait()

    def run(self):
        # create binary dest file
        timestr = time.strftime("%Y%m%d_%H%M")
        filename = "logs/log_" + timestr + ".csv"
        log_file = open(filename, mode='w+', newline='')
        log_writer = csv.writer(log_file, delimiter=';')
        filednames = ['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_x', 'q1', 'q2', 'q3', 'q4']
        log_writer.writerow(filednames)
        start_time = datetime.datetime.now()
        elapsed = 0.0
        while not self.isFinished():
            if not self.Paused:
                package = self.ser.readline()[:-1]
                if len(package) == 40:
                    data_f = unpack('ffffffffff', package)
                    log_writer.writerow((elapsed,) + data_f)
                    self.update_signal.emit((elapsed,) + data_f)

                end_time = datetime.datetime.now()
                time_diff = (end_time - start_time)
                elapsed = time_diff.total_seconds()



