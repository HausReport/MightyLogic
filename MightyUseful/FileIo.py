from PySide2.QtWidgets import QWidget, QFileDialog

from MightyUseful.Datafile import get_data_file


def getArmy(parent: QWidget, army):
    data_file = get_data_file()
    if data_file.is_dir():
        data_file = QFileDialog.getOpenFileName(parent, "Open Collection File", str(data_file.absolute()), "CSV Files (*.csv)")
    army.fromFile(data_file)