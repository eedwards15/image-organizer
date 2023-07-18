from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame, QFileDialog, QGraphicsPixmapItem, QGraphicsScene,\
    QGraphicsView, QGridLayout,QLineEdit, QLabel, QMessageBox, QSizePolicy, QSplitter, QWidget
from PyQt6.QtGui import QImage, QPixmap
import sys, os, platform, shutil

from click_frame import ClickFrame



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
        interactive_widgets_status(self, widget)

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
    interactive_widgets_status(self, widget)
    widget.image_index = 0
    widget.image = QImage(widget.thumb_list[widget.image_index])
    widget.image_display.setPixmap(QPixmap(widget.image).scaled(700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
    get_current_image(self, widget)
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
    unhighlight_all(self, widget)
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

def cat_sel_func(self, widget):
    ''' runs the funtion when the category selection changes '''
    widget.category_selector.currentIndexChanged.connect(lambda: interactive_widgets_status(self,widget))

def interactive_widgets_status(self, widget):
    ''' Enables or disables all widgets with conditional dependencies '''

    set_category_index(self, self)
    add_btn_status(self, self)
    if widget.sorted_image_files != []:
        widget.previous_button.setDisabled(False)
        widget.next_button.setDisabled(False)
        widget.category_selector.setDisabled(False)
    else:
        widget.previous_button.setDisabled(True)
        widget.next_button.setDisabled(True)
        widget.add_button.setDisabled(True)
        widget.category_selector.setDisabled(True)

def previous_image(self, widget):
    ''' Allows for backward navigation '''

    if widget.image_index != 0:
        widget.image_index = widget.image_index-1
        widget.image = QImage(widget.thumb_list[widget.image_index])
        widget.image_display.setPixmap(QPixmap(widget.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        unhighlight_all(self, widget)
        widget.highlight_selected()
    get_current_image(self, widget)
    widget.show_category_if_categorized()

def next_image(self, widget):
    ''' Allows for forward navigation '''

    if widget.image_index < len(widget.sorted_image_files)-1:
        widget.image_index = widget.image_index+1
        widget.image = QImage(widget.thumb_list[widget.image_index])
        widget.image_display.setPixmap(QPixmap(widget.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        unhighlight_all(self, widget)
        widget.highlight_selected()
    get_current_image(self,widget)
    widget.show_category_if_categorized()

def get_current_image(self, widget):
    ''' Adds the current image file to a variable'''
    widget.current_image = widget.sorted_image_files[widget.image_index]



def populate_grid_view(self, widget):
    ''' creates the thumbnails of every supported image in the working directory '''

    for widget.image_index, widget.file_name in enumerate(widget.sorted_image_files):
        widget.thumb_main_img = QImage(widget.sorted_image_files[widget.image_index])
        widget.thumb_img = QLabel(self)
        widget.thumb_txt = QLabel(self.file_name, self)
        widget.image_index_list.append(self.image_index)
        widget.thumb_txt.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding)
        widget.thumb_txt.setWordWrap(True)
        widget.thumb_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        widget.thumb_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        widget.thumb_img.setPixmap(QPixmap(self.thumb_main_img).scaled(
            125, 125, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        widget.thumb_frame = ClickFrame(self)
        widget.thumb_frame.clicked.connect(lambda: thumbnail_click(self,self))
        widget.thumb_frame.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed)
        # assigns a name to every frame created so that they are directly accessible
        widget.thumb_frame.setObjectName(widget.file_name)
        widget.thumb_list.append(widget.thumb_frame.objectName())
        widget.thumb_layout = QtWidgets.QVBoxLayout(widget.thumb_frame)
        widget.thumb_layout.addWidget(widget.thumb_img)
        widget.thumb_layout.addWidget(widget.thumb_txt)
        widget.bottom_layout.addWidget(widget.thumb_frame)
        widget.thumb_dict = dict(zip(widget.thumb_list, widget.image_index_list))
        QApplication.processEvents()
    self.loading_msg_label.setText("Import complete")

def build_selector(self ,widget):
    ''' Creates the selection menu for the categories '''

    # Category Selector
    widget.category_selector = QtWidgets.QComboBox(widget)
    widget.category_selector.setDisabled(True)
    widget.category_selector.setSizePolicy(
        QSizePolicy.Policy.Preferred,
        QSizePolicy.Policy.Fixed)
    # Add Button
    widget.add_button =  QtWidgets.QPushButton('Add', widget)
    widget.add_button.setSizePolicy( QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    widget.add_button.clicked.connect(widget.build_file_operation_dict)
    widget.add_button.setDisabled(True)
    # Creates the category selector layout
    widget.cat_frame = QtWidgets.QFrame(widget)
    widget.cat_frame.setFrameShape(QFrame.Shape.StyledPanel)
    widget.cat_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    widget.cat_sel_layout = QtWidgets.QHBoxLayout(widget.cat_frame)
    widget.cat_sel_layout.addWidget(widget.category_selector)
    widget.cat_sel_layout.addWidget(widget.add_button)
    # Adds the selector to right layout
    widget.right_layout.addWidget(widget.cat_frame)

def unhighlight_all(self, widget):
    ''' sets style of unselected thumbnails '''
    for i in range(len(widget.bottom_layout)):
        widget.thumb = widget.bottom_layout.itemAt(i).widget()
        widget.thumb.setStyleSheet("border: none;")

def organize_warning_popup(self, wdiget):
    ''' Displays a popup message to make sure user wants to execute file operations '''
    wdiget.last_chance_message_box = QMessageBox(wdiget)
    wdiget.last_chance_message_box.setWindowTitle("WARNING!")
    wdiget.last_chance_message_box.setIcon(QMessageBox.Icon.Warning)
    wdiget.last_chance_message_box.setText("This operation cannot be undone! Do you wish to continue?")
    wdiget.last_chance_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
    wdiget.yes_button = self.last_chance_message_box.button(QMessageBox.StandardButton.Yes)
    wdiget.no_button = self.last_chance_message_box.button(QMessageBox.StandardButton.No)
    wdiget.no_button.setText("Cancel")

    wdiget.last_chance_message_box.exec()

    if wdiget.last_chance_message_box.clickedButton() == wdiget.yes_button:
        wdiget.organize_images()

def highlight_selected(self, widget):
    ''' sets the style of the selected thumbnail '''
    widget.thumb_selected = widget.findChild(ClickFrame, widget.thumb_list[widget.image_index])
    widget.thumb_selected.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")
    print(widget.thumb_list[widget.image_index])


def show_category_if_categorized(self, widget):
    ''' If an image has been added to a category,
    that category becomes the current item in the selector when the image is selected '''

    get_current_image(self,widget)
    if widget.current_image in widget.file_operation_dict.keys():
        widget.category_index = widget.category_selector.findText(widget.file_operation_dict[widget.current_image], QtCore.Qt.MatchFlag.MatchFixedString)
        widget.category_selector.setCurrentIndex(self.category_index)
    else:
        widget.category_selector.setCurrentIndex(0)