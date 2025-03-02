import sys
import json, json_gen
from Verification import CANMessage, SendMessage, ReceiveMessage, Signal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar, QTreeView
from PyQt5.QtGui import QIcon, QColor, QBrush, QStandardItem, QStandardItemModel
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
    
class CANTreeModel(QStandardItemModel):
    def __init__(self, data=None):
        super().__init__()
        self.setHorizontalHeaderLabels(["Name", "Value", "Description"])
        self.message = CANMessage(1, 2)
        self.populateTree()

    def make_row(self, name, value, description):
        child1_name = QStandardItem(name)
        child1_value = QStandardItem(value)
        child1_desc = QStandardItem(description)

        def changed_item_handling(top_left, bottom_right):
            if child1_name == "message_config" :
                self.message.update_config_mode(child1_value.data())
            self.populateTree() 

        # child1_value.dataChanged.connect(changed_item_handling)

        return [child1_name, child1_value, child1_desc]

    def populateTree(self):
        dict_to_process = self.message.get_dict()

        CANmessage = QStandardItem("CAN Message")

        for key in dict_to_process.keys():
            if not isinstance(dict_to_process[key], list):
                CANmessage.appendRow(self.make_row(key, str(dict_to_process[key]), ""))


        receive_messages = QStandardItem("Receive Messages")
        signal = QStandardItem("Signal")

        count = 0
        countSig = 0
        for send_message in dict_to_process["send_msgs"]:
            iterMessage = QStandardItem(f"Message {count}")
            CANmessage.child(1).appendRow(iterMessage)
            count = count + 1
            for key in send_message.keys():
                if not isinstance(send_message[key], list):
                    iterMessage.appendRow(self.make_row(key, str(send_message[key]), ""))
                # else:
                    





        CANmessage.child(2).appendRow(receive_messages)
        
        self.appendRow(CANmessage)

    def flags(self, index):
        if index.column() == 1:  # Only "Value" column is editable
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
        self.setWindowTitle("AMK Tool: Message Editor")
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
        # self.table_view = QTableView()
        # self.layout.addWidget(self.table_view)

        # initial tree
        self.tree_view = QTreeView()
        self.layout.addWidget(self.tree_view)
        self.model = CANTreeModel()
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setColumnWidth(0, 350)
        self.tree_view.setColumnWidth(1, 200)
        self.tree_view.setColumnWidth(2, 1000)
        # self.model = CANTableModel()
        # self.table_view.setModel(self.model)
        # self.table_view.setColumnWidth(0, 350)
        # self.table_view.setColumnWidth(1, 200)
        # self.table_view.setColumnWidth(2, 1000)


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())