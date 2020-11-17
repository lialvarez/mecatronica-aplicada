import sys
from PyQt5.QtWidgets import QApplication
from Application_pyqtgraph import Application


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    fusion_gui = Application()
    fusion_gui.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()