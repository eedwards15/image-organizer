from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame, QFileDialog, QGraphicsPixmapItem, QGraphicsScene,\
    QGraphicsView, QGridLayout,QLineEdit, QLabel, QMessageBox, QSizePolicy, QSplitter, QWidget
from PyQt6.QtGui import QImage, QPixmap
import sys, os, platform, shutil

 



def folder_select(self, widget):
    ''' Assignes the selected path to the input box '''
    chosen_directory = QFileDialog.getExistingDirectory(widget)
    if chosen_directory != "":
        widget.selection_input.clear()
    widget.selection_input.insert(chosen_directory)
    widget.input_text = widget.selection_input.text()

def load_btn_status(self, widget):
    ''' Disables and enables the load button when the conditions are met '''
    if widget.selection_input.text() != "":
        widget.import_button.setDisabled(False)
    elif widget.selection_input.text() == "":
        widget.import_button.setDisabled(True)

def loading_msg_check(self, widget):
    ''' Clears all images and executes the build dictionary function when the status bar reads "Importing Images... '''
    if "Importing Images . . ." in widget.loading_msg_label.text():
        QApplication.processEvents()
        if widget.bottom_layout.count() != 0:
            widget.clear_thumbnails()
            widget.clear_img_display()
        widget.build_dict()