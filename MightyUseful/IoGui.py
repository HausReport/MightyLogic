from pathlib import Path

import PySide2.QtCore as QtCore
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QWidget, QFileDialog

from MightyLogic.HighGrowth.Erlaed.FileIo import FileIO


class IoGui:
    @staticmethod
    def getArmy(parent: QWidget, army):
        data_file = IoGui.get_data_file()
        if data_file.is_dir():
            data_file = QFileDialog.getOpenFileName(parent, "Open Collection File", str(data_file.absolute()),
                                                    "CSV Files (*.csv)")
        army.fromFile(data_file)

    @staticmethod
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

    @staticmethod
    def get_data_file():
        dir_path = FileIO.get_data_directory()
        file_name = "all.csv"
        file_path = dir_path / file_name

        if file_path.exists():
            print("File Exists")
            return file_path
        else:
            print("File Nexists")
            return dir_path

    @staticmethod
    def get_strategies_file():
        dir_path = FileIO.get_data_directory()
        file_name = "strategies.csv"
        file_path = dir_path / file_name

        if file_path.exists():
            print("Config File Exists")
            return file_path
        else:
            print("Config File Nexists")
            return None
