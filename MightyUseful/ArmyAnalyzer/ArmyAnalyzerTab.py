from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSplitter, QWidget, QVBoxLayout, QGroupBox, QRadioButton

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyUseful.MplCanvas import MplCanvas


class ArmyAnalyzerTab(QWidget):

    #
    # Adding something bad to something bad somewhere... entering an infinite loop or some shit
    #
    def __init__(self, anArmy: Army):
        super().__init__()
        self.army = anArmy
        self.splitter = QSplitter(self, Qt.Vertical)

        self.hdr = QWidget()
        vbox = QVBoxLayout()
        self.hdr.setLayout(vbox)
        rarityBox = QGroupBox("Rarity")
        box4 = QVBoxLayout()
        self.showCommon = QRadioButton("Common")
        self.showCommon.toggled.connect(self.checkBoxChange)
        box4.addWidget(self.showCommon)
        self.showRare = QRadioButton("Rare")
        self.showRare.toggled.connect(self.checkBoxChange)
        box4.addWidget(self.showRare)
        self.showEpic = QRadioButton("Epic")
        self.showEpic.toggled.connect(self.checkBoxChange)
        box4.addWidget(self.showEpic)
        self.showLegendary = QRadioButton("Legendary")
        # self.showLegendary.setChecked(True)
        self.showLegendary.toggled.connect(self.checkBoxChange)
        box4.addWidget(self.showLegendary)
        rarityBox.setLayout(box4)
        vbox.addWidget(rarityBox)

        self.splitter.addWidget(self.hdr)

        self.anal = QWidget(self)
        vbox2 = QVBoxLayout()
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        series = self.army.getLegendaries()
        x = series.Level
        # plt.axvline(x=7)
        stats = x.describe()
        mean = stats['mean']
        median = stats['50%']
        lq = stats['25%']
        rq = stats['75%']
        ticks = int(stats['max'] + 1)
        sc.axes.hist(x, bins=ticks)
        sc.axes.set_xticks(ticks=range(1, ticks))
        sc.axes.set_xlabel("Level")
        sc.axes.set_ylabel("Count")

        sc.axes.axvline(x=mean, color='r', label='Average Hero Level')
        sc.axes.axvline(x=median, color='g', label='Median Hero Level')
        sc.axes.axvline(x=lq, color='g', label='Bottom Quartile', ls=':')
        sc.axes.axvline(x=rq, color='g', label='Top Quartile', ls=':')

        # plt.axvline(x=median, color='g', label='Median Hero Level', ls=':')

        sc.axes.legend(title="Rare Hero Level Distribution", bbox_to_anchor=(1.0, 1), loc='upper left')
        self.anal.setLayout(vbox2)
        vbox2.addWidget(sc)

        self.splitter.addWidget(self.anal)
        vbox.addWidget(self.splitter)

    def checkBoxChange(self, state):
        """
        Handle when user clicks a filter checkbox.
        :param state:
        :return:
        """
        pass
        # aList = []
        # if self.showCommon.isChecked():
        #     aList.append("Common")
        # if self.showRare.isChecked():
        #     aList.append("Rare")
        # if self.showEpic.isChecked():
        #     aList.append("Epic")
        # if self.showLegendary.isChecked():
        #     aList.append("Legendary")
        # reg = '(' + '|'.join(aList) + ')'
        # self.proxy.setFilterByColumn(5, reg)
