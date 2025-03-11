import sys, os
import json, json_gen
from Verification import CANMessage, SendMessage, ReceiveMessage, Signal, Verification
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar, QTreeView
from PyQt5.QtGui import QIcon, QColor, QBrush, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel
from CANStandardItem import CANStandardItem

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
    def __init__(self, message =None):
        super().__init__()
        self.message = message if message else CANMessage(1, 0, 0, 500)
        self.populateTree()

    def make_row(self, name, value, description):
        child1_name = CANStandardItem(name, self.message, name)
        child1_value = CANStandardItem(value, self.message, name)
        child1_desc = CANStandardItem(description, self.message, name)

        return [child1_name, child1_value, child1_desc]

    # def make_row(self, name, value, description, obj):
    #     """ Creates a row with Name, Value, and Description, bound to a specific object. """
    #     child1_name = CANStandardItem(name, obj, name)  # Name column
    #     child1_value = CANStandardItem(value, obj, name)  # Value column (editable)
    #     child1_desc = QStandardItem(description)  # Description column

    #     return [child1_name, child1_value, child1_desc]
    
    def populateTree(self):
        self.clear()
        self.setHorizontalHeaderLabels(["Name", "Value", "Description"])

        dict_to_process = self.message.CANMessageDict # dict
        CANmessage = QStandardItem("CAN Message")

        for key in dict_to_process.keys(): # dict
            if not isinstance(dict_to_process[key], list):
                CANmessage.appendRow(self.make_row(key, str(dict_to_process[key]), ""))



        count = 0
        for send_message in dict_to_process["send_msgs"]: # dict
            iterMessage = QStandardItem(f"Message {count}")
            CANmessage.child(1).appendRow(iterMessage)

            signalDict = send_message["signals"]
            count = count + 1
            countSig = 0
            for key in send_message.keys():
                if not isinstance(send_message[key], list):
                    iterMessage.appendRow(self.make_row(key, str(send_message[key]), ""))
                    print(f"DEBUG: Adding {key} to tree from {str(send_message)}'s {type(send_message).__name__}")
                else:
                    for sigElement in signalDict:
                        signal = QStandardItem(f"Signal {countSig}")
                        countSig = countSig + 1
                        for insideElement in sigElement:
                            signal.appendRow(self.make_row(str(insideElement), str(sigElement[insideElement]), ""))
                            print(f"DEBUG: Adding {insideElement} to tree from {str(sigElement)}'s {type(sigElement).__name__}")
                        iterMessage.appendRow(signal)
                    
        # CANmessage.child(2).appendRow() # position for receive messages
        
        self.appendRow(CANmessage)



    # def populateTree(self):
    #     """ Builds the tree structure, correctly binding objects to editable fields. """

    #     dict_to_process = self.message.get_dict()
    #     CANmessage = QStandardItem("CAN Message")

    #     # Attach CANMessage attributes (config_mode, total_send, etc.)
    #     for key in dict_to_process.keys():
    #         if not isinstance(dict_to_process[key], list):
    #             CANmessage.appendRow(self.make_row(key, str(dict_to_process[key]), "", self.message))

    #     # Attach Send Messages
    #     send_messages_item = QStandardItem("Send Messages")
    #     CANmessage.appendRow(send_messages_item)

    #     for i, send_msg in enumerate(self.message.send_messages):
    #         send_message_item = QStandardItem(f"Send Message {i}")
    #         send_messages_item.appendRow(send_message_item)

    #         # Attach SendMessage attributes (CAN_ID, data_length, cycle_time, etc.)
    #         for key in send_msg.mappings.keys():
    #             send_message_item.appendRow(self.make_row(key, getattr(send_msg, key), "", send_msg))

    #         # Attach Signals inside SendMessage
    #         signals_item = QStandardItem("Signals")
    #         send_message_item.appendRow(signals_item)

    #         for j, signal in enumerate(send_msg.signals):
    #             signal_item = QStandardItem(f"Signal {j}")
    #             signals_item.appendRow(signal_item)

    #             for key in signal.mappings.keys():
    #                 signal_item.appendRow(self.make_row(key, getattr(signal, key), "", signal))

    #     # Attach Receive Messages
    #     receive_messages_item = QStandardItem("Receive Messages")
    #     CANmessage.appendRow(receive_messages_item)

    #     for i, recv_msg in enumerate(self.message.receive_messages):
    #         receive_message_item = QStandardItem(f"Receive Message {i}")
    #         receive_messages_item.appendRow(receive_message_item)

    #         # Attach ReceiveMessage attributes (CAN_ID, data_length, telegram_failure_monitoring, etc.)
    #         for key in recv_msg.mappings.keys():
    #             receive_message_item.appendRow(self.make_row(key, getattr(recv_msg, key), "", recv_msg))

    #         # Attach Signals inside ReceiveMessage
    #         signals_item = QStandardItem("Signals")
    #         receive_message_item.appendRow(signals_item)

    #         for j, signal in enumerate(recv_msg.signals):
    #             signal_item = QStandardItem(f"Signal {j}")
    #             signals_item.appendRow(signal_item)

    #             for key in signal.mappings.keys():
    #                 signal_item.appendRow(self.make_row(key, getattr(signal, key), "", signal))

    #     # Add the completed CANMessage hierarchy to the model
    #     self.appendRow(CANmessage)

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
        new_message = Verification.read_JSON(filePath) # returns a CANMessage
        self.model = CANTreeModel(new_message)
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        json_gen.run(filePath) # creates JSON from raw at "test_data/data.json"
        new_message = Verification.read_JSON("test_data/data.json") # returns a CANMessage
        self.model = CANTreeModel(new_message)
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

    def exportJsonFile(self):
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        filePath, _ = QFileDialog.getSaveFileName(
            self, 
            "Export JSON File", 
            os.path.join(download_path, "exported_CANMessage.json"),  # Default file path
            "JSON Files (*.json)"
        )

        Verification.write_JSON(filePath, Verification.read_JSON("test_data/data.json"))

    def exportRawFile(self):
        # TODO Make this actually work, not the exact same as exportJsonFile lol
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        filePath, _ = QFileDialog.getSaveFileName(
            self, 
            "Export JSON File", 
            os.path.join(download_path, "exported_CANMessage.json"),  # Default file path
            "JSON Files (*.json)"
        )

        Verification.write_JSON(filePath, Verification.read_JSON("test_data/data.json"))

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

        exportJsonAction = QAction("Export as JSON", self)
        exportJsonAction.triggered.connect(self.exportJsonFile)
        exportRawAction = QAction("Export as RAW", self)
        exportJsonAction.triggered.connect(self.exportRawFile)


        fileMenu.addAction(importJsonAction)
        fileMenu.addAction(importRawAction)
        fileMenu.addAction(exportJsonAction)
        fileMenu.addAction(exportRawAction)


        # initial ui
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
    
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

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())