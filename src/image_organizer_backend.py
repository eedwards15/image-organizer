from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame, QFileDialog, QGraphicsPixmapItem, QGraphicsScene,\
    QGraphicsView, QGridLayout,QLineEdit, QLabel, QMessageBox, QSizePolicy, QSplitter, QWidget
from PyQt6.QtGui import QImage, QPixmap
import sys, os, platform, shutil

from click_frame import ClickFrame


def on_browse_click(self, widget):
    ''' Opens a file dialog to select a folder '''
    #widget.selection_input.clear()
    chosen_directory = QFileDialog.getExistingDirectory(widget)
    widget.selection_input.insert(chosen_directory)
    widget.input_text = widget.selection_input.text()
    widget.import_button.setDisabled(False)

def on_selected_input_change(self, widget):
    ''' Enables the import button when the input field is not empty '''
    selected_folder_empty = widget.selection_input.text() == ""
    print(selected_folder_empty)
    widget.selection_input.setDisabled(selected_folder_empty)

def on_import_click(self, widget):
    ''' Assigns the input path to the current working directory '''
    if os.path.exists(widget.selection_input.text()) and widget.selection_input.text() != "":
        widget.loading_msg_label.setText("Loading Images . . .")
        widget.input_text = widget.selection_input.text() #rename this to something more descriptive
        widget.working_directory = widget.input_text
        os.chdir(widget.working_directory)
        clear_categories_tree(self, widget)
        clear_category_selector(self, widget)
        clear_thumbnails(self, widget)
        clear_img_display(self,widget)
        build_dict(self,widget)  #refactor this method.       
    else:
        widget.invalid_path = QMessageBox(self)
        widget.invalid_path.warning(self, "Attention", "Invalid file path!")



def loading_msg_check(self, widget):
    ''' Clears all images and executes the build dictionary function when the status bar reads "Importing Images... '''
    if "Importing Images . . ." in widget.loading_msg_label.text():
        QApplication.processEvents()
        if widget.bottom_layout.count() != 0:
            clear_thumbnails(self, widget)
            clear_img_display(self,widget)
        build_dict(self,widget)


    if "Refreshing . . ." in widget.loading_msg_label.text():
        QApplication.processEvents()
        if widget.bottom_layout.count() != 0:
            clear_thumbnails(self, widget)
            clear_img_display(self,widget)
        build_dict(self,widget)

def add_wd_to_tree(self, widget):
    ''' Adds the working directory as the root item in the category view '''
    widget.current_os = platform.system()

    if "/" in widget.working_directory:
        clear_categories_tree(self, widget)
        widget.image_folder = widget.working_directory.split("/")[-1]
        widget.WD_item = QtWidgets.QTreeWidgetItem(widget.category_view, [widget.image_folder])
        widget.WD_item.setExpanded(True)
        widget.category_view.addTopLevelItem(self.WD_item)
        widget.new_category_input.setDisabled(False)
    elif "\\" in widget.working_directory:
        clear_categories_tree(self, widget)
        widget.image_folder = widget.working_directory.split("\\")[-1]
        widget.WD_item = QtWidgets.QTreeWidgetItem(widget.category_view, [widget.image_folder])
        widget.category_view.addTopLevelItem(widget.WD_item)

def on_create_category_click(self, widget):
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
    highlight_selected(self,widget)

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
    show_category_if_categorized(self, widget)
    #sets the style of the selected thumbnail
    widget.clicked.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")

## migt not be used not needed
def warning_button_clicked(self, widget):
    ''' If the user clicks the yes button, the file operations are executed '''
    if widget.warning_popup == QMessageBox.StandardButton.Yes:
        organize_images(self,widget)
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

def on_previous_image_click(self, widget):
    ''' Allows for backward navigation '''

    if widget.image_index != 0:
        widget.image_index = widget.image_index-1
        widget.image = QImage(widget.thumb_list[widget.image_index])
        widget.image_display.setPixmap(QPixmap(widget.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        unhighlight_all(self, widget)
        highlight_selected(self,widget)
    get_current_image(self, widget)
    show_category_if_categorized(self, widget)

def on_next_image_click(self, widget):
    ''' Allows for forward navigation '''

    if widget.image_index < len(widget.sorted_image_files)-1:
        widget.image_index = widget.image_index+1
        widget.image = QImage(widget.thumb_list[widget.image_index])
        widget.image_display.setPixmap(QPixmap(widget.image).scaled(
            700, 700, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        unhighlight_all(self, widget)
        highlight_selected(self,widget)
    get_current_image(self,widget)
    show_category_if_categorized(self, widget)

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
        widget.thumb_txt.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        widget.thumb_txt.setWordWrap(True)
        widget.thumb_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        widget.thumb_txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        widget.thumb_img.setPixmap(QPixmap(self.thumb_main_img).scaled(125, 125, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        widget.thumb_frame = ClickFrame(self)
        widget.thumb_frame.clicked.connect(lambda: thumbnail_click(self,self))
        widget.thumb_frame.setSizePolicy( QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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

def unhighlight_all(self, widget):
    ''' sets style of unselected thumbnails '''
    for i in range(len(widget.bottom_layout)):
        widget.thumb = widget.bottom_layout.itemAt(i).widget()
        widget.thumb.setStyleSheet("border: none;")

def on_organize_click(self, widget):
    ''' Displays a popup message to make sure user wants to execute file operations '''
    _organize_warning_popup(self, widget)

def _organize_warning_popup(self, wdiget):
    #TODO: 
    # move this to the GUI Helper. 
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
        organize_images(self,wdiget)

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

def organization_btn_status(self, widget):
    ''' Disables and enables the organize button when the conditions are met '''
    if len(widget.file_operation_dict) != 0:
        widget.organize_button.setDisabled(False)
    else:
        widget.organize_button.setDisabled(True)

def build_dict(self, widget):
    ''' Creates all the dictionaries, lists, and sets to be used,
    then populates lists with names of supported image files in the working directory '''

    if widget.image_files != []:
        widget.image_files = []
        widget.sorted_image_files = []
        widget.file_operation_dict = {}
        reset_image_list(self, widget)
        populate_grid_view(self, widget)
    else: 
        reset_image_list(self, widget)

    # populates lists with the names of all supported images files in the working directory
    for widget.file_name in os.listdir():
        img_extention_check(self, widget)
        if img_extention_check(self, widget) == False: continue
        widget.image_files.append(widget.file_name)
        widget.sorted_image_files = sorted(widget.image_files, key=str.lower,)
    
    if self.sorted_image_files != []:
        populate_grid_view(self, widget)
        display_images(self, widget)
        add_wd_to_tree(self,widget)
    elif widget.sorted_image_files == []:
        widget.loading_msg_label.setText("No valid image files found. Please choose a different folder.")

    cat_sel_func(self,widget)


################################  Rename Files  ###################################

def rename_popup(self,widget):
    ''' Displays a popup message to ask if files should be renamed by category '''
    widget.rename_message_box = QMessageBox(widget)
    widget.rename_message_box.setWindowTitle("WARNING!")
    widget.rename_message_box.setIcon(QMessageBox.Icon.Warning)
    widget.rename_message_box.setText("Would you like to rename files by category?")
    widget.rename_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
    widget.rename_yes_button = widget.rename_message_box.button(QMessageBox.StandardButton.Yes)
    widget.no_button = widget.rename_message_box.button(QMessageBox.StandardButton.No)
    widget.no_button.setText("No")

    widget.rename_message_box.exec()

    if widget.rename_message_box.clickedButton() == widget.rename_yes_button:
        return True
    else: 
        return False

def build_file_operation_dict(self, widget):
    ''' Populates the dictionary that all file operations reference '''
    get_current_image(self, widget)
    if widget.file_operation_dict == {}:
        widget.file_operation_dict = {widget.current_image : widget.category_name}
    else:
        widget.file_operation_dict[widget.current_image] = widget.category_name
    widget.loading_msg_label.setText(f"{widget.current_image} added to {widget.category_name}")
    print(widget.file_operation_dict)
    organization_btn_status(self, widget)

def organize_images(self, widget):
    ''' Creates a folder in the working directory for every category,
    and the moves all images to the folder of the category they're added to. '''
    rename = rename_popup(self,widget)
    
    for widget.current_image, widget.category_name in widget.file_operation_dict.items():
            widget.category_folder_set.add(widget.category_name)

    for widget.category_name in widget.category_folder_set:
        # creates a folder for every category
        # if the folder already exists, it skips the creation
        if os.path.exists(self.category_name) == False:
            os.mkdir(f"{self.category_name}")
    
    for widget.current_image, widget.category_name in widget.file_operation_dict.items():
        if widget.current_os == "Linux" or widget.current_os == "Darwin":
            shutil.move(widget.current_image, f"{widget.working_directory}/{widget.category_name}")
        else:
            shutil.move(widget.current_image, f"{widget.working_directory}\\{widget.category_name}")
    
    if rename:
        for folder in widget.category_folder_set:

            if widget.current_os == "Linux" or widget.current_os == "Darwin":
                os.chdir(f"{widget.working_directory}/{folder}")
            else:
                os.chdir(f"{widget.working_directory}\\{folder}")
    
            index = 0
            for f in os.listdir():
                f_name, f_ext = os.path.splitext(f)
                new_name = "{}{}{}{}".format(folder, "0", index, f_ext)
                os.rename(f, new_name)
                index += 1
        os.chdir(widget.working_directory)

    widget.loading_msg_label.setText("Importing Images . . ." )
    QApplication.processEvents()

def reset_image_list(self, widget):
    ''' Clears the list of image file names '''
    if widget.image_files != []:
        widget.selection_input.setText("")
        widget.image_files.clear()

def clear_thumbnails(self, widget):
    ''' Removes all thumbnails that have previously been created. '''
    for i in reversed(range(widget.bottom_layout.count())):
        widget.bottom_layout.itemAt(i).widget().deleteLater()
        QApplication.processEvents()

def clear_img_display(self,widget):
    ''' Removes the image in the main display '''
    widget.image_display.clear()

def clear_categories_tree(self,widget):
    ''' Removes all items from the category view widget '''
    widget.category_view.clear()

def clear_category_selector(self,widget):
    ''' Removes all items from the selection menu '''
    widget.category_selector.clear()
    QApplication.processEvents()
    widget.category_selector.addItem("--Select Category--")
    set_category_index(self,widget)
