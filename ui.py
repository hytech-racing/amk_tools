import sys
import json_gen
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class BasicWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(120)

        self.tableWidget.setHorizontalHeaderLabels(['Name',
                                                    'Dec Value',
                                                    'Note'])
        self.tableWidget.setColumnWidth(0, 400)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 1000)

        # makes Name and Note cols unable to be edited by user --DOES NOT WORK--
        for i in range(self.tableWidget.rowCount()):
            for j in [0, 2]:
                item = self.tableWidget.item(i, j)
                if item is not None:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsDropEnabled)
        
        self.setCentralWidget(self.tableWidget)
    
    def populateTable(self, json_data):
        # TODO Populate Dec Val col with proper values.
        item = QTableWidgetItem("placeholder WIP")
        self.tableWidget.setItem(0, 0, item)

    def importJsonFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import JSON File", "", "JSON Files (*.json)")
        if filePath:
            # Open the selected file and read its contents
            with open(filePath, "r") as file:
                json_data = file.read()
                self.populateTable(json_data)

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        print(filePath)
        json_gen.run(filePath) # creates JSON from raw at "testdata/data.json"
        
        # TODO potentially update test data path
        with open("test_data/data.json", "r") as file:
            json_data = file.read()
            self.populateTable(json_data)

    def initUI(self):
        self.setWindowTitle("name")
        self.setGeometry(100, 100, 1600, 900)  # (x, y, width, height)
        appIcon = QIcon("res/10617840.png")
        QApplication.setWindowIcon(appIcon)

        # Menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")


        importJsonAction = QAction("Import JSON", self)
        importJsonAction.triggered.connect(self.importJsonFile)
        importRawAction = QAction("Import RAW", self)
        importRawAction.triggered.connect(self.importRawFile)

        exportAction = QAction("Export", self)

        fileMenu.addAction(importJsonAction)
        fileMenu.addAction(importRawAction)
        fileMenu.addAction(exportAction)

        # Initialize Table
        self.createTable()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicWindow()
    window.show()
    sys.exit(app.exec_())