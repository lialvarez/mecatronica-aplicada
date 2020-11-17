from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import GUI_design
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from DataList import DataList
from reader_thread import ReaderThread
import numpy as np


class Application(QMainWindow, GUI_design.Ui_MainWindow):
    max_len = 100
    update_enabled = False
    update_period_ms = 1/25.0 * 1000

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

        self.t = DataList(self.max_len)

        self.ax_t = DataList(self.max_len)
        self.ay_t = DataList(self.max_len)
        self.az_t = DataList(self.max_len)

        self.gx_t = DataList(self.max_len)
        self.gy_t = DataList(self.max_len)
        self.gz_t = DataList(self.max_len)

        self.q1 = DataList(self.max_len)
        self.q2 = DataList(self.max_len)
        self.q3 = DataList(self.max_len)
        self.q4 = DataList(self.max_len)

        self.pitch = DataList(self.max_len)
        self.yaw = DataList(self.max_len)
        self.roll = DataList(self.max_len)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.acc_t_axes = self.figure.add_subplot(321)
        self.acc_t_axes.set_xticks([])
        self.acc_f_axes = self.figure.add_subplot(322)
        self.acc_f_axes.set_xticks([])
        self.gyro_t_axes = self.figure.add_subplot(323)
        self.gyro_t_axes.set_xticks([])
        self.gyro_f_axes = self.figure.add_subplot(324)
        self.gyro_f_axes.set_xticks([])
        self.angles_t_axes = self.figure.add_subplot(325)
        self.angles_t_axes.set_xticks([])
        self.angles_f_axes = self.figure.add_subplot(326)
        self.angles_f_axes.set_xticks([])
        self.figure.tight_layout()
        self.gridLayout.addWidget(self.canvas)

        self.update_plot()


        self.btn_start_stop.clicked.connect(self.toggle_update_data)




    def toggle_update_data(self):
        if not self.update_enabled:
            # TODO: move serial settings to json file
            serial_settings = dict()
            serial_settings["baudrate"] = 115000
            serial_settings["port"] = "COM6"
            self.reader_thread = ReaderThread(serial_settings)
            self.reader_thread.update_signal.connect(self.update_data)
            self.reader_thread.start()
            self.timer.start(int(self.update_period_ms))
            self.update_enabled = True
        elif self.update_enabled:
            self.reader_thread.terminate()
            self.update_plot()
            self.update_enabled = False

    def update_plot(self):
        self.acc_t_axes.cla()
        self.acc_t_axes.plot(self.ax_t, label='Ax')
        self.acc_t_axes.plot(self.ay_t, label='Ay')
        self.acc_t_axes.plot(self.az_t, label='Az')
        self.acc_t_axes.set_xticks([])
        self.acc_t_axes.set_ylim(-1.5, 2)

        self.acc_f_axes.cla()

        self.gyro_t_axes.cla()
        self.gyro_t_axes.plot(self.gx_t, label='Ax')
        self.gyro_t_axes.plot(self.gy_t, label='Ay')
        self.gyro_t_axes.plot(self.gz_t, label='Az')
        self.gyro_t_axes.set_xticks([])
        self.gyro_t_axes.set_ylim(-4.1, 4.1)

        self.gyro_f_axes.cla()

        self.angles_t_axes.cla()

        self.canvas.draw()


    def update_data(self, data_f):
        self.reader_thread.Paused = True
        self.ax_t.append(data_f[1])
        self.ay_t.append(data_f[2])
        self.az_t.append(data_f[3])
        self.gx_t.append(data_f[4])
        self.gy_t.append(data_f[5])
        self.gz_t.append(data_f[6])

        x, y, z = self.quaternion_to_euler_angle_vectorized2(data_f[7], data_f[8], data_f[9], data_f[10])
        self.pitch.append(x)
        self.yaw.append(y)
        self.roll.append(z)

        self.reader_thread.Paused = False

    def quaternion_to_euler_angle_vectorized2(self, w, x, y, z):
        ysqr = y * y

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + ysqr)
        X = np.degrees(np.arctan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)

        t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
        Y = np.degrees(np.arcsin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        Z = np.degrees(np.arctan2(t3, t4))

        return X, Y, Z