"""
    the interactive_sys
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui_logit import GUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = GUI(MainWindow)
    MainWindow.show()
    ui.play_action()

    sys.exit(app.exec_())

