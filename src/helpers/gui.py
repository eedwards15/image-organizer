from PyQt6 import QtGui

class GuiHelper:

    def createFont(self, italic=False, bold=False, size=12):
        """
        Creates a QFont object with the specified properties.

        Args:
            italic (bool): Whether the font should be italicized.
            bold (bool): Whether the font should be bolded.
            size (int): The point size of the font.

        Returns:
            QFont: The created QFont object.
        """
        font = QtGui.QFont()
        font.setItalic(italic)
        font.setBold(bold)
        font.setPointSize(size)
        return font