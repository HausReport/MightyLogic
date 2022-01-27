from pathlib import Path
import PySide2.QtCore as QtCore
import appdirs

from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QWidget, QFileDialog


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


def get_data_directory():
    appname = "Mighty Useful"
    appauthor = "Nightmare"
    data_dir = appdirs.user_data_dir(appname, appauthor)
    print(data_dir)

    dir_path = Path(data_dir)
    tdir_path = dir_path.parent
    if not tdir_path.exists():
        tdir_path.mkdir(exist_ok=True)

    if not dir_path.exists():
        dir_path.mkdir(exist_ok=True)
    return dir_path


def get_data_file():
    dir_path = get_data_directory()
    file_name = "all.csv"
    file_path = dir_path / file_name

    if file_path.exists():
        print("File Exists")
        return file_path
    else:
        print("File Nexists")
        return dir_path


def get_strategies_file():
    dir_path = get_data_directory()
    file_name = "strategies.csv"
    file_path = dir_path / file_name

    if file_path.exists():
        print("Config File Exists")
        return file_path
    else:
        print("Config File Nexists")
        return None