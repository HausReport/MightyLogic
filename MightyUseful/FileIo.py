from pathlib import Path
import PySide2.QtCore as QtCore

from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QWidget, QFileDialog

from MightyUseful.Datafile import get_data_file


def getArmy(parent: QWidget, army):
    data_file = get_data_file()
    if data_file.is_dir():
        data_file = QFileDialog.getOpenFileName(parent, "Open Collection File", str(data_file.absolute()), "CSV Files (*.csv)")
    army.fromFile(data_file)

def nameToPixmap(aName, width=100, height=100):
    aName = aName.replace(' ', '_')  # need to replace spaces with underline
    aName = aName.replace('"', '')  # need to replace spaces with underline
    if aName.endswith('rmun_Grand'):
        aName = "J%3Frmun_Grand"
    if aName.endswith('tunn'):
        aName = "J%3Ftunn"
    aName += '.png'
    path = Path.cwd() / ".." / "MightyLogic" / "image" / aName
    # print(path)
    # print(path.exists())
    # print("role = " + str(role))
    image = QImage(str(path.absolute()))
    pixmap = QPixmap.fromImage(image)
    return pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)