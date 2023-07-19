import sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  QFrame,QLineEdit, QLabel,  QSizePolicy, QSplitter, QWidget
from constants import *
from image_organizer_backend import *
from helpers.gui import GuiHelper

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        '''MainWindow Constructor'''
        super().__init__(*args, **kwargs)
        self.gui_helper = GuiHelper()
        self.title = Constants.TITLE
        self.image_files = []
        self.sorted_image_files = []
        self.image_index_list = []
        self.thumb_list = []
        self.file_operation_dict = {}
        self.category_folder_set = set()

        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(Constants.WIDTH,  Constants.HEIGHT)

        self.itallic_font = self.gui_helper.createFont(italic=True, size=10)
        self.big_font = self.gui_helper.createFont(bold=True, size=12)

        # Browse Directory Button
        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.setMaximumWidth(75)
        self.browse_button.clicked.connect(lambda: on_browse_click(self, self))

        # Select Directory and input
        self.selection_input = QtWidgets.QLineEdit(self)
        self.selection_input.setPlaceholderText("Path to Folder")
        self.selection_input.setFont(self.itallic_font)
        self.selection_input.resize(350,33)
        self.selection_input.textChanged[str].connect(lambda: load_btn_status(self, self))

        # Select Button
        self.import_button =  QtWidgets.QPushButton('Import', self)
        self.import_button.clicked.connect(lambda: on_import_click(self, self))
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
        self.create_button.clicked.connect(lambda: on_create_category_click(self, self))

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
        
        #Oranize Button
        self.organize_button = QtWidgets.QPushButton('Organize', self)
        self.organize_button.setFont(self.big_font)
        self.organize_button.setFixedWidth(125)
        self.organize_button.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Preferred)
        self.organize_button.clicked.connect(lambda: on_organize_click(self, self))
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
        self.previous_button.clicked.connect(lambda : on_previous_image_click(self, self))
        self.previous_button.setDisabled(True)

        self.next_button = QtWidgets.QPushButton(">", self)
        self.next_button.setFont(self.big_font)
        self.next_button.setMaximumWidth(25)
        self.next_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.next_button.clicked.connect(lambda: on_next_image_click(self, self))
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
        self.version_label.setText('v0.4.0')
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

        # Category Selector
        self.category_selector = QtWidgets.QComboBox(self)
        self.category_selector.setDisabled(True)
        self.category_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        # Add Button
        self.add_button =  QtWidgets.QPushButton('Add', self)
        self.add_button.setSizePolicy( QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.add_button.clicked.connect(lambda:build_file_operation_dict(self, self))
        self.add_button.setDisabled(True)

        # Creates the category selector layout
        self.cat_frame = QtWidgets.QFrame(self)
        self.cat_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cat_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.cat_sel_layout = QtWidgets.QHBoxLayout(self.cat_frame)
        self.cat_sel_layout.addWidget(self.category_selector)
        self.cat_sel_layout.addWidget(self.add_button)

        # Adds the selector to right layout
        self.right_layout.addWidget(self.cat_frame)





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
