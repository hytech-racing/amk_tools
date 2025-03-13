import sys, os
import json, json_gen, gen_bytes
from Verification import CANMessage, SendMessage, ReceiveMessage, Signal, Verification
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableView, QVBoxLayout, QWidget, QAction, QMenuBar, QTreeView
from PyQt5.QtGui import QIcon, QColor, QBrush, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel
from CANStandardItem import CANStandardItem

class CANTreeModel(QStandardItemModel):
    def __init__(self, message =None):
        super().__init__()
        self.message = message if message else CANMessage(1, 0, 0, 500)
        self.populateTree()

    def make_row(self, name, value, description, obj):
        """
        Creates a row with Name, Value, and Description, bound to a specific object.
        Uses wrapper function for populateTree to save scroll position.
        """
        tree_update_func = getattr(self, 'tree_update_callback', self.populateTree)
        child1_name = CANStandardItem(name, obj, name, tree_update_func)  # Name column
        child1_value = CANStandardItem(value, obj, name, tree_update_func)  # Value column (editable)
        child1_desc = QStandardItem(description)  # Description column

        return [child1_name, child1_value, child1_desc]
    
    def populateTree(self):
        self.clear()
        self.setHorizontalHeaderLabels(["Name", "Value", "Description"])
        # print(self.parent)
        can_message = QStandardItem("CAN Message")

        self.appendRow(can_message)

        CAN_message_dictionary = self.message.get_dict()
        for key in self.message.mappings:
            can_message.appendRow(self.make_row(key, CAN_message_dictionary[key], self.message.mappings[key]["description"], self.message))

        send_header = QStandardItem("Send Messages")
        
        for i in range(self.message.total_send):
            send_message = self.message.send_messages[i]
            send_message_header = QStandardItem("Send Message " + str(i + 1))
            send_message_dictionary = send_message.getDict()

            for key in send_message.mappings:
                send_message_header.appendRow(self.make_row(key, send_message_dictionary[key], send_message.mappings[key]["description"], send_message))

            signal_header = QStandardItem("Signals")

            for ii in range(send_message.total_signals):
                signal = send_message.signals[ii]
                signal_message_header = QStandardItem("Signal " + str(ii + 1))
                signal_dict = signal.get_dict()

                for key in signal.mappings:
                    signal_message_header.appendRow(self.make_row(key, signal_dict[key], signal.mappings[key]["description"], signal))
                signal_header.appendRow(signal_message_header)
            send_message_header.appendRow(signal_header)
            send_header.appendRow(send_message_header)
        can_message.appendRow(send_header)

        receive_header = QStandardItem("Receive Messages")
        
        for i in range(self.message.total_receive):
            receive_message = self.message.receive_messages[i]
            receive_message_header = QStandardItem("Receive Message " + str(i + 1))
            receive_message_dictionary = receive_message.getDict()

            for key in receive_message.mappings:
                receive_message_header.appendRow(self.make_row(key, receive_message_dictionary[key], receive_message.mappings[key]["description"], receive_message))

            signal_header = QStandardItem("Signals")

            for ii in range(receive_message.total_signals):
                signal = receive_message.signals[ii]
                signal_message_header = QStandardItem("Signal " + str(ii + 1))
                signal_dict = signal.get_dict()

                for key in signal.mappings:
                    signal_message_header.appendRow(self.make_row(key, signal_dict[key], signal.mappings[key]["description"], signal))
                signal_header.appendRow(signal_message_header)
            receive_message_header.appendRow(signal_header)
            receive_header.appendRow(receive_message_header)
        can_message.appendRow(receive_header)

    def flags(self, index):
        if index.column() == 1:  # Only "Value" column is editable
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def updateTreeWithScroll(self):
        """
        Wrapper method to update the tree model and reset the vertical scroll position to the same
        position as before. This is a workaround to prevent the tree view from
        jumping to the top whenever the model is updated.
        """
        scroll_pos = self.tree_view.verticalScrollBar().value()
        self.model.populateTree()
        self.tree_view.verticalScrollBar().setValue(scroll_pos)
        self.tree_view.expandAll()
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setColumnWidth(0, 350)
        self.tree_view.setColumnWidth(1, 200)
        self.tree_view.setColumnWidth(2, 1000)

    def importJsonFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import JSON File", "", "JSON Files (*.json)")
        if not filePath:
            print("No import path selected.")
            return
        
        def keep_view():
            self.tree_view.expandAll()
            self.tree_view.setRootIsDecorated(False)
            self.tree_view.setColumnWidth(0, 350)
            self.tree_view.setColumnWidth(1, 200)
            self.tree_view.setColumnWidth(2, 1000)
        
        new_message = Verification.read_JSON(filePath) # returns a CANMessage
        self.model = CANTreeModel(new_message) # resets tree with new CANMessage from file
        self.model.tree_update_callback = self.updateTreeWithScroll
        self.model.rowsInserted.connect(keep_view)
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        if not filePath:
            print("No import path selected.")
            return
        try:
            json_gen.run(filePath) # creates JSON from raw at "data/data.json"
        except Exception as e:
            print("Raw CAN message file not in correct format, see testdata/AMK_raw_CAN_userlist for example.")

        def keep_view():
                self.tree_view.expandAll()
                self.tree_view.setRootIsDecorated(False)
                self.tree_view.setColumnWidth(0, 350)
                self.tree_view.setColumnWidth(1, 200)
                self.tree_view.setColumnWidth(2, 1000)

        new_message = Verification.read_JSON("data/data.json") # returns a CANMessage
        self.model = CANTreeModel(new_message)
        self.model.tree_update_callback = self.updateTreeWithScroll
        self.model.rowsInserted.connect(keep_view)
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
        if not filePath:
            print("No export path selected.")
            return

        Verification.write_JSON(filePath, self.model.message)

    def exportRawFile(self):
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        filePath, _ = QFileDialog.getSaveFileName(
            self, 
            "Export RAW File", 
            os.path.join(download_path, "exported_CANMessage"),  # Default file path
            ""
        )
        if not filePath:
            print("No export path selected.")
            return
        Verification.write_JSON("data/toRaw.json", self.model.message)
        gen_bytes.jsonToRaw("data/toRaw.json", filePath)

    def initUI(self):
        self.setWindowTitle("AMK Tool: CAN Message Editor")
        self.setGeometry(100, 100, 1600, 900)
        QApplication.setWindowIcon(QIcon("res/10617840.png"))

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
        exportRawAction.triggered.connect(self.exportRawFile)

        fileMenu.addAction(importJsonAction)
        fileMenu.addAction(importRawAction)
        fileMenu.addAction(exportJsonAction)
        fileMenu.addAction(exportRawAction)

        # initial ui
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        def keep_view():
            self.tree_view.expandAll()
            self.tree_view.setRootIsDecorated(False)
            self.tree_view.setColumnWidth(0, 350)
            self.tree_view.setColumnWidth(1, 200)
            self.tree_view.setColumnWidth(2, 1000)
            
        # initial tree
        self.tree_view = QTreeView()
        self.layout.addWidget(self.tree_view)
        self.model = CANTreeModel()
        self.model.tree_update_callback = self.updateTreeWithScroll
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()
        self.model.rowsInserted.connect(keep_view)
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