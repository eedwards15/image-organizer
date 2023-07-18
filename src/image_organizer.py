from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFrame, QFileDialog, QGraphicsPixmapItem, QGraphicsScene,\
    QGraphicsView, QGridLayout,QLineEdit, QLabel, QMessageBox, QSizePolicy, QSplitter, QWidget
from PyQt6.QtGui import QImage, QPixmap
import sys, os, platform, shutil

from click_frame import ClickFrame
from constants import *
from image_organizer_backend import *

# qtmodern.styles

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        '''MainWindow Constructor'''
        super().__init__(*args, **kwargs)
        self.title = Constants.TITLE
        self.width = Constants.WIDTH
        self.height = Constants.HEIGHT
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # Create Font Style Options
        self.itallic_font = QtGui.QFont()
        self.itallic_font.setItalic(True)
        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(16)
        self.big_font.setBold(True)

        # Browse Directory Button
        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.setMaximumWidth(75)
        #self.browse_button.clicked.connect(self.folder_select)
        self.browse_button.clicked.connect(lambda: folder_select(self, self))

        # Select Directory and input
        self.selection_input = QtWidgets.QLineEdit(self)
        self.selection_input.setPlaceholderText("Path to Folder")
        self.selection_input.setFont(self.itallic_font)
        self.selection_input.resize(350,33)
        self.selection_input.textChanged[str].connect(lambda: load_btn_status(self, self))

        # Select Button
        self.import_button =  QtWidgets.QPushButton('Import', self)
        self.import_button.clicked.connect(lambda: create_working_directory(self, self))
        self.import_button.setDisabled(True)

        # new category input
        self.new_category_input = QtWidgets.QLineEdit(self)
        self.new_category_input.setPlaceholderText("Create New Category...")
        self.new_category_input.setFont(self.itallic_font)
        self.new_category_input.resize(350,33)
        self.new_category_input.textChanged[str].connect(lambda : create_btn_status(self, self))
        self.new_category_input.setDisabled(True)

        # Create Button
        self.create_button =  QtWidgets.QPushButton('Create', self)
        self.create_button.setDisabled(True)
        self.create_button.clicked.connect(lambda: create_new_category(self, self))

        # Category Tree View
        self.category_view = QtWidgets.QTreeWidget(self)
        self.category_view.setHeaderLabel('Categories')
        self.category_view.setSortingEnabled(True)
        self.category_view.sortByColumn(0,QtCore.Qt.SortOrder.AscendingOrder)
        self.category_view.setAlternatingRowColors(True)
        self.category_view.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)

        # Organize button and label
        self.organization_label = QtWidgets.QLabel('This operation cannot be undone!')
        self.organization_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.organization_label.setFont(self.itallic_font)
        self.organization_label.setWordWrap(True)
        self.organization_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.organize_button = QtWidgets.QPushButton('Organize', self)
        self.organize_button.setFont(self.big_font)
        self.organize_button.setFixedWidth(125)
        self.organize_button.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Preferred)
        self.organize_button.clicked.connect(self.organize_warning_popup)
        self.organize_button.setDisabled(True)


        # Image Viewer Label and Scroll Area
        self.scrolling_display_area = QtWidgets.QScrollArea(self)
        self.scrolling_display_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_display_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_display_area.setWidgetResizable(True)

        self.image_display = QLabel(self)
        self.image_display.setScaledContents(False)
        self.image_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.scrolling_display_area.setWidget(self.image_display)

        # Image Navigation Buttons
        self.previous_button = QtWidgets.QPushButton("<", self)
        self.previous_button.setFont(self.big_font)
        self.previous_button.setMaximumWidth(25)
        self.previous_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.previous_button.clicked.connect(lambda : previous_image(self, self))
        self.previous_button.setDisabled(True)

        self.next_button = QtWidgets.QPushButton(">", self)
        self.next_button.setFont(self.big_font)
        self.next_button.setMaximumWidth(25)
        self.next_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.next_button.clicked.connect(lambda: next_image(self, self))
        self.next_button.setDisabled(True)

        # status bar
        self.loading_msg_label = QLineEdit(self)
        self.loading_msg_label.setStyleSheet( "border: 1px solid rgb(42,42,42); background-color:transparent; color: rgb(127,127,127);")
        self.loading_msg_label.setText("")
        self.loading_msg_label.setDisabled(True)
        self.loading_msg_label.setFont(self.itallic_font)
        self.loading_msg_label.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.loading_msg_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.loading_msg_label.textChanged[str].connect(lambda: loading_msg_check(self, self))   

        # version number
        self.version_label = QLineEdit(self)
        self.version_label.setStyleSheet( "border: 1px solid rgb(42,42,42); background-color:transparent; color: rgb(127,127,127);")
        self.version_label.setText('Created by: Daniel Lukas v0.3.2alpha')
        self.version_label.setDisabled(True)
        self.version_label.setFont(self.itallic_font)
        self.version_label.setFixedWidth(225)
        self.version_label.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

    #######################################################################
    ##############################  Layout  ###############################
    #######################################################################

        # creates the main layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # creates the right_layout and adds objects
        self.right_frame = QtWidgets.QFrame(self)
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.right_layout = QtWidgets.QVBoxLayout(self.right_frame)

        # selection Layout
        self.top_frame = QtWidgets.QFrame(self)
        self.top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.top_frame.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        self.path_selection_layout = QtWidgets.QHBoxLayout(self.top_frame)
        self.path_selection_layout.addWidget(self.browse_button)
        self.path_selection_layout.addWidget(self.selection_input)
        self.path_selection_layout.addWidget(self.import_button)

        # Create the main Display and Navigation Layout
        self.image_nav_layout = QtWidgets.QHBoxLayout()
        self.image_nav_layout.addWidget(self.previous_button, 0)
        self.image_nav_layout.addWidget(self.scrolling_display_area, 4)
        self.image_nav_layout.addWidget(self.next_button, 0)

        # add selection layout to right_layout
        self.right_layout.addLayout(self.image_nav_layout)

        # Category Layout
        self.left_frame = QtWidgets.QFrame(self)
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_layout = QtWidgets.QVBoxLayout(self.left_frame)

        # creates category_new layout
        self.category_create_new_layout = QtWidgets.QHBoxLayout()
        self.category_create_new_layout.addWidget(self.new_category_input)
        self.category_create_new_layout.addWidget(self.create_button)

        self.left_layout.addLayout(self.category_create_new_layout, 0)
        self.left_layout.addWidget(self.category_view, 1)
        self.left_layout.addWidget(self.organize_button,0, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Creates the horizontal splitter
        self.horizontal_splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.horizontal_splitter.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
        self.horizontal_splitter.addWidget(self.left_frame)
        self.horizontal_splitter.addWidget(self.right_frame)
        self.horizontal_splitter.setStretchFactor(1,5)
        self.horizontal_splitter.setSizes([300,960])
        self.horizontal_splitter.setCollapsible(0, False)
        self.horizontal_splitter.setCollapsible(1, False)

        # Grid View Scroll Area
        self.scrolling_grid_area = QtWidgets.QScrollArea(self)
        self.scrolling_grid_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_grid_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrolling_grid_area.setWidgetResizable(True)

        self.bottom_frame = QtWidgets.QFrame(self)
        self.bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.bottom_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.bottom_layout.setSpacing(10)
        self.scrolling_grid_area.setWidget(self.bottom_frame)

        # Creates the vertical splitter
        self.vertical_splitter = QSplitter(QtCore.Qt.Orientation.Vertical)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.scrolling_grid_area)
        self.vertical_splitter.setStretchFactor(10,1)
        self.vertical_splitter.setSizes([635,210])
        self.vertical_splitter.setCollapsible(0, False)
        self.vertical_splitter.setCollapsible(1, False)

        # status area
        self.status_layout = QtWidgets.QHBoxLayout()
        self.status_layout.addWidget(self.loading_msg_label,3)
        self.status_layout.addWidget(self.version_label,1)
        # add sub_layouts to main layout
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.vertical_splitter)
        self.main_layout.addLayout(self.status_layout)
        # sets the parent/main layout
        self.setLayout(self.main_layout)

        build_selector(self,self)

    def build_dict(self):
        ''' Creates all the dictionaries, lists, and sets to be used,
        then populates lists with names of supported image files in the working directory '''

        # creates a list that will get populated with filenames
        self.image_files = []
        self.sorted_image_files = []
        self.image_index_list = []
        self.thumb_list = []
        self.file_operation_dict = {}
        self.category_folder_set = set()

        self.reset_image_list()

        # populates lists with the names of all supported images files in the working directory
        for self.file_name in os.listdir():
            img_extention_check(self, self)
            if img_extention_check(self, self) == False: continue
            self.image_files.append(self.file_name)
            self.sorted_image_files = sorted(self.image_files, key=str.lower,)
        if self.sorted_image_files != []:
            populate_grid_view(self, self)
            display_images(self, self)
            add_wd_to_tree(self,self)
        elif self.sorted_image_files == []:
            self.loading_msg_label.setText("No valid image files found. Please choose a different folder.")

        cat_sel_func(self,self)



    def unhighlight_all(self):
        ''' sets style of unselected thumbnails '''
        for i in range(len(self.bottom_layout)):
            self.thumb = self.bottom_layout.itemAt(i).widget()
            self.thumb.setStyleSheet("border: none;")

    def highlight_selected(self):
        ''' sets the style of the selected thumbnail '''
        self.thumb_selected = self.findChild(ClickFrame, self.thumb_list[self.image_index])
        self.thumb_selected.setStyleSheet("border: 1px solid rgb(42, 130, 218); background-color: rgb(42, 130, 218); color: white;")
        print(self.thumb_list[self.image_index])


    def build_file_operation_dict(self):
        ''' Populates the dictionary that all file operations reference '''

        get_current_image(self, self)
        if self.file_operation_dict == {}:
            self.file_operation_dict = {self.current_image : self.category_name}
        else:
            self.file_operation_dict[self.current_image] = self.category_name
        self.loading_msg_label.setText(f"{self.current_image} added to {self.category_name}")
        print(self.file_operation_dict)
        self.organization_btn_status()

    def show_category_if_categorized(self):
        ''' If an image has been added to a category,
        that category becomes the current item in the selector when the image is selected '''

        get_current_image(self,self)
        if self.current_image in self.file_operation_dict.keys():
            self.category_index = self.category_selector.findText(self.file_operation_dict[self.current_image], QtCore.Qt.MatchFlag.MatchFixedString)
            self.category_selector.setCurrentIndex(self.category_index)
        else:
            self.category_selector.setCurrentIndex(0)

    def organization_btn_status(self):
        ''' Disables and enables the organize button when the conditions are met '''
        if len(self.file_operation_dict) != 0:
            self.organize_button.setDisabled(False)
        else:
            self.organize_button.setDisabled(True)

    def organize_warning_popup(self):
        ''' Displays a popup message to make sure user wants to execute file operations '''
        self.last_chance_message_box = QMessageBox(self)
        self.last_chance_message_box.setWindowTitle("WARNING!")
        self.last_chance_message_box.setIcon(QMessageBox.Icon.Warning)
        self.last_chance_message_box.setText("This operation cannot be undone! Do you wish to continue?")
        self.last_chance_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        self.yes_button = self.last_chance_message_box.button(QMessageBox.StandardButton.Yes)
        self.no_button = self.last_chance_message_box.button(QMessageBox.StandardButton.No)
        self.no_button.setText("Cancel")

        self.last_chance_message_box.exec()

        if self.last_chance_message_box.clickedButton() == self.yes_button:
            self.organize_images()



    def organize_images(self):
        ''' Creates a folder in the working directory for every category,
        and the moves all images to the folder of the category they're added to. '''
        rename = self.rename_popup()
        
        for self.current_image, self.category_name in self.file_operation_dict.items():
                self.category_folder_set.add(self.category_name)

        for self.category_name in self.category_folder_set:
            # creates a folder for every category
            # if the folder already exists, it skips the creation
            if os.path.exists(self.category_name) == False:
                os.mkdir(f"{self.category_name}")
        
        for self.current_image, self.category_name in self.file_operation_dict.items():
            if self.current_os == "Linux" or self.current_os == "Darwin":
                shutil.move(self.current_image, f"{self.working_directory}/{self.category_name}")
            else:
                shutil.move(self.current_image, f"{self.working_directory}\\{self.category_name}")
        
        if rename:
            for folder in self.category_folder_set:

                if self.current_os == "Linux" or self.current_os == "Darwin":
                    os.chdir(f"{self.working_directory}/{folder}")
                else:
                    os.chdir(f"{self.working_directory}\\{folder}")
      
                index = 0
                for f in os.listdir():
                    f_name, f_ext = os.path.splitext(f)
                    new_name = "{}{}{}{}".format(folder, "0", index, f_ext)
                    os.rename(f, new_name)
                    index += 1
            os.chdir(self.working_directory)

################################  Rename Files  ###################################

    def rename_popup(self):
        ''' Displays a popup message to ask if files should be renamed by category '''
        self.rename_message_box = QMessageBox(self)
        self.rename_message_box.setWindowTitle("WARNING!")
        self.rename_message_box.setIcon(QMessageBox.Icon.Warning)
        self.rename_message_box.setText("Would you like to rename files by category?")
        self.rename_message_box.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        self.rename_yes_button = self.rename_message_box.button(QMessageBox.StandardButton.Yes)
        self.no_button = self.rename_message_box.button(QMessageBox.StandardButton.No)
        self.no_button.setText("No")

        self.rename_message_box.exec()

        if self.rename_message_box.clickedButton() == self.rename_yes_button:
            return True
        else: return False



#######################################################################
#############  Functions that remove and delete things   ##############
#######################################################################

    def reset_image_list(self):
        ''' Clears the list of image file names '''
        if self.image_files != []:
            self.selection_input.setText("")
            self.image_files.clear()

    def clear_thumbnails(self):
        ''' Removes all thumbnails that have previously been created. '''
        for i in reversed(range(self.bottom_layout.count())):
            self.bottom_layout.itemAt(i).widget().deleteLater()
            QApplication.processEvents()

    def clear_img_display(self):
        ''' Removes the image in the main display '''
        self.image_display.clear()

    def clear_categories_tree(self):
        ''' Removes all items from the category view widget '''
        self.category_view.clear()

    def clear_cat_selector(self):
        ''' Removes all items from the selection menu '''
        self.category_selector.clear()
        QApplication.processEvents()
        self.category_selector.addItem("--Select Category--")
        set_category_index(self,self)

if __name__ == '__main__':
    # Translate asset paths to useable format for PyInstaller
    def resource_path(relative_path):
        ''' This is a workaround by Aaron Tan
        from his blog https://blog.aaronhktan.com/posts/2018/05/14/pyqt5-pyinstaller-executable '''
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path('image-organizer-icon.png')))
    win = MainWindow()
    # qtmodern.styles.dark(app)
    win.show()
    sys.exit(app.exec())
