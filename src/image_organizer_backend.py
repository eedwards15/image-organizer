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

def create_working_directory(self, widget):
    ''' Assigns the input path to the current working directory '''
    if os.path.exists(widget.selection_input.text()) and widget.selection_input.text() != "":
        widget.input_text = widget.selection_input.text()
        widget.working_directory = widget.input_text
        os.chdir(widget.working_directory)
        widget.clear_categories_tree()
        widget.clear_cat_selector()
        widget.loading_msg_label.setText("Importing Images . . .")
    else:
        widget.invalid_path = QMessageBox(self)
        widget.invalid_path.warning(self, "Attention", "Invalid file path!")

def add_wd_to_tree(self, widget):
    ''' Adds the working directory as the root item in the category view '''
    widget.current_os = platform.system()

    if "/" in widget.working_directory:
        widget.clear_categories_tree()
        widget.image_folder = widget.working_directory.split("/")[-1]
        widget.WD_item = QtWidgets.QTreeWidgetItem(widget.category_view, [widget.image_folder])
        widget.WD_item.setExpanded(True)
        widget.category_view.addTopLevelItem(self.WD_item)
        widget.new_category_input.setDisabled(False)
    elif "\\" in widget.working_directory:
        widget.clear_categories_tree()
        widget.image_folder = widget.working_directory.split("\\")[-1]
        widget.WD_item = QtWidgets.QTreeWidgetItem(widget.category_view, [widget.image_folder])
        widget.category_view.addTopLevelItem(widget.WD_item)

def create_new_category(self, widget):
    ''' Adds a new category to the category_view and category_selector widgets '''

    if widget.new_category_input.text() != "":
        widget.category = QtWidgets.QTreeWidgetItem(widget.WD_item,[widget.new_category_input.text()])
        widget.category_view.addTopLevelItem(widget.category)
        widget.category_selector.addItem(widget.new_category_input.text())
        widget.category_selector.model().sort(0, QtCore.Qt.SortOrder.AscendingOrder)
        widget.new_category_input.clear()
        QApplication.processEvents()
        widget.interactive_widgets_status()