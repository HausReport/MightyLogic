import PySide2
from PySide2.QtWidgets import QTableView


class MyTableView(QTableView):

    def verticalHeader(self) -> PySide2.QtWidgets.QHeaderView:
        pass
