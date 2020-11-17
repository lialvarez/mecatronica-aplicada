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
import pyqtgraph as pg


class Application(QMainWindow, GUI_design.Ui_MainWindow):
    max_len = 100
    update_enabled = False
    update_period_ms = 1/20.0 * 1000

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

        self.acc_t_plot = pg.PlotWidget()
        self.acc_t_plot.setYRange(-1.5, 1.5)
        self.acc_t_layout.addWidget(self.acc_t_plot)

        self.gyro_t_plot = pg.PlotWidget()
        self.gyro_t_plot.setYRange(-70, 70)
        self.gyro_t_layout.addWidget(self.gyro_t_plot)

        self.angles_t_plot = pg.PlotWidget()
        self.angles_t_plot.setYRange(-1, 1)
        self.angles_t_layout.addWidget(self.angles_t_plot)


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
        self.acc_t_plot.plotItem.clear()
        self.acc_t_plot.plotItem.addLegend()
        self.acc_t_plot.plot(self.ax_t, pen='r', name='Ax')
        self.acc_t_plot.plot(self.ay_t, pen='g', name='Ay')
        self.acc_t_plot.plot(self.az_t, pen='b', name='Az')

        self.gyro_t_plot.plotItem.clear()
        self.gyro_t_plot.plotItem.addLegend()
        self.gyro_t_plot.plot(self.gx_t, pen='r', name='Gx')
        self.gyro_t_plot.plot(self.gy_t, pen='g', name='Gy')
        self.gyro_t_plot.plot(self.gz_t, pen='b', name='Gz')

        self.angles_t_plot.plotItem.clear()
        self.angles_t_plot.plotItem.addLegend()
        self.angles_t_plot.plot(self.q1)
        self.angles_t_plot.plot(self.q2)
        self.angles_t_plot.plot(self.q3)
        self.angles_t_plot.plot(self.q4)

    def update_data(self, data_f):
        self.reader_thread.Paused = True
        self.ax_t.append(data_f[1])
        self.ay_t.append(data_f[2])
        self.az_t.append(data_f[3])
        self.gx_t.append(data_f[4])
        self.gy_t.append(data_f[5])
        self.gz_t.append(data_f[6])
        self.q1.append(data_f[7])
        self.q2.append(data_f[8])
        self.q3.append(data_f[9])
        self.q4.append(data_f[10])

        x, y, z = self.quaternion_to_euler_angle_vectorized2(data_f[7], data_f[8], data_f[9], data_f[10])
        self.pitch.append(x)
        self.yaw.append(y)
        self.roll.append(z)

        self.reader_thread.Paused = False

    @staticmethod
    def quaternion_to_euler_angle_vectorized2(w, x, y, z):
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