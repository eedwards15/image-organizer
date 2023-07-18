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

def create_btn_status(self, widget):
    ''' Disables and enables the create button when the conditions are met '''

    if widget.new_category_input.text() != "":
        widget.create_button.setDisabled(False)
    elif widget.new_category_input.text() == "":
        widget.create_button.setDisabled(True)


def add_btn_status(self, widget):
    ''' Disables and enables the add button when the conditions are met '''
    if widget.category_index != 0:
        widget.add_button.setDisabled(False)
    elif widget.category_index == 0:
        widget.add_button.setDisabled(True)

def set_category_index(self, widget):
    ''' finds the index of the selected category item '''
    widget.category_name = widget.category_selector.currentText()
    widget.category_index = widget.category_selector.findText(widget.category_name, QtCore.Qt.MatchFlag.MatchFixedString)
    widget.category_selector.setCurrentIndex(widget.category_index)

def display_images(self, widget):
    ''' Displays the first image in the directory '''
    widget.import_button.setDisabled(True)
    widget.interactive_widgets_status()
    widget.image_index = 0
    widget.image = QImage(widget.thumb_list[widget.image_index])
    widget.image_display.setPixmap(QPixmap(widget.image).scaled(700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
    widget.get_current_image()
    widget.highlight_selected()


def img_extention_check(self, widget):
    ''' Checks all files in the working directory for supported image formats '''
    widget.img_extentions = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'tif', 'xbm', 'xpm', 'webp']
    widget.three_char_extention = widget.file_name[-3:]
    widget.four_char_extention = widget.file_name[-4:]
    if widget.three_char_extention in widget.img_extentions or widget.four_char_extention in widget.img_extentions:
        return True
    elif widget.three_char_extention not in widget.img_extentions or widget.four_char_extention not in widget.img_extentions:
        return False
    

def thumbnail_click(self, widget):
    ''' Get thumbnail that was clicked '''

    widget.clicked = widget.sender()
    widget.image_index = widget.thumb_dict[widget.clicked.objectName()]
    widget.image = QImage(widget.thumb_list[widget.image_index])
    widget.image_display.setPixmap(QPixmap(widget.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
    print(widget.clicked.objectName())
    widget.unhighlight_all()
    widget.show_category_if_categorized()
    #sets the style of the selected thumbnail
    widget.clicked.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")



## migt not be used not needed
def warning_button_clicked(self, widget):
    ''' If the user clicks the yes button, the file operations are executed '''
    if widget.warning_popup == QMessageBox.StandardButton.Yes:
        widget.organize_images()
    elif widget.warning_popup == QMessageBox.Cancel:
        widget.last_chance_message_box.Ignore()