from PyQt6 import QtCore, QtWidgets

class ClickFrame(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QFrame.mousePressEvent(self, event)