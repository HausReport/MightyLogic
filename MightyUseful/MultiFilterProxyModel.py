import re

from PySide2.QtCore import Qt, QSortFilterProxyModel, QModelIndex

from MightyUseful.AbstractFilter import AbstractFilter


class MultiFilterMode:
    AND = 0
    OR = 1


class MultiFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}
        self.multi_filter_mode = MultiFilterMode.AND

    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        col = source_left.column()
        if col in [2, 3, 4, 9, 10]:
            leftInt = int(str(source_left.data()).replace(',', ''))
            rightInt = int(str(source_right.data()).replace(',', ''))
            return leftInt < rightInt
        elif col == 0:
            return False
        else:
            return source_left.data() < source_right.data()

    def setFilterByColumn(self, column, regex):
        if isinstance(regex, str):
            regex = re.compile(regex)
        self.filters[column] = regex
        self.invalidateFilter()

    def clearFilter(self, column):
        del self.filters[column]
        self.invalidateFilter()

    def clearFilters(self):
        self.filters = {}
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.filters:
            return True

        results = []
        for key, regex in self.filters.items():
            text = ''
            index = self.sourceModel().index(source_row, key, source_parent)
            if index.isValid():
                text = self.sourceModel().data(index, Qt.DisplayRole)
                if text is None:
                    text = ''
            if isinstance(regex, AbstractFilter):
                print("Is filter")
                results.append(regex.matches(text))
            else:
                results.append(regex.match(text))

        if self.multi_filter_mode == MultiFilterMode.OR:
            return any(results)
        return all(results)
