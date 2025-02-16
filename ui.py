import sys
import json, json_gen
import Verification
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel

class CANTableModel(QAbstractTableModel):
    def __init__(self, data = None):
        super().__init__()
        self.headers = ["Name", "Value", "Description"]
        self.data_list = []

    def rowCount(self, parent=None):
        return len(self.data_list)

    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.data_list[index.row()][index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.data_list[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            self.handle_dynamic_update(index.row(), value)
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

    def flags(self, index):
        """Enable editing for the value column."""
        if index.column() == 1:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def importJsonFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import JSON File", "", "JSON Files (*.json)")
        if filePath:
            # Open the selected file and read its contents
            with open(filePath, "r") as file:
                json_data = json.load(file)

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        print(filePath)
        json_gen.run(filePath) # creates JSON from raw at "testdata/data.json"
        
        # TODO potentially update test data path
        with open("test_data/data.json", "r") as file:
            json_data = json.load(file)

    def initUI(self):
        self.setWindowTitle("name")
        self.setGeometry(100, 100, 1600, 900)
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


        # initial ui
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
    
        # initial table
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        self.model = CANTableModel()
        self.table_view.setModel(self.model)
        self.table_view.setColumnWidth(0, 350)
        self.table_view.setColumnWidth(1, 200)
        self.table_view.setColumnWidth(2, 1000)


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())