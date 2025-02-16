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
        self.data_list = [
            ["Total Send Messages", "0", "Number of messages to send"],
            ["Total Receive Messages", "0", "Number of messages to receive"],
        ]
        self.saved_messages_send = {}
        self.saved_signals_send = {}
        self.saved_signals_recv = {}

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

    def handle_dynamic_update(self, row, value):
        """Dynamically updates the table when total_send or total_recv_msgs is modified."""
        if row == 0:  # Total Send Messages changed
            try:
                total_send = int(value)
                self.update_send_messages(total_send)
            except ValueError:
                pass  # Ignore non-numeric values

    def update_send_messages(self, total_send):
        """Dynamically add or remove send messages while preserving values, even when set to 0."""
        self.beginResetModel()

        # Extract all existing values before clearing the table
        existing_values = {row[0]: row[1] for row in self.data_list if "Send Message" in row[0]}

        # Save all existing messages before clearing them
        self.saved_messages_send.update(existing_values)

        # Keep the first row (Total Send Messages) and last row (Total Receive Messages)
        total_receive_row = self.data_list[-1]  # Save Total Receive Messages row
        self.data_list = self.data_list[:1]  # Keep only Total Send Messages row

        # If total_send is 0, do NOT lose saved messages; just clear the displayed ones
        if total_send == 0:
            self.data_list.append(total_receive_row)
            self.endResetModel()
            return

        # Restore previously deleted values if available
        for i in range(total_send):
            message_key = f"Send Message {i+1}"

            self.data_list.append([f"{message_key} - CAN_ID", 
                                self.saved_messages_send.get(f"{message_key} - CAN_ID", ""), 
                                "CAN Identifier"])
            
            self.data_list.append([f"{message_key} - Cycle Time", 
                                self.saved_messages_send.get(f"{message_key} - Cycle Time", ""), 
                                "Cycle time in ms"])
            
            self.data_list.append([f"{message_key} - Data Length", 
                                self.saved_messages_send.get(f"{message_key} - Data Length", ""), 
                                "Data length in bytes"])
            
            self.data_list.append([f"{message_key} - Attr", 
                                self.saved_messages_send.get(f"{message_key} - Attr", ""), 
                                "Attribute value"])
            
            self.data_list.append([f"{message_key} - Total Signals", 
                                self.saved_messages_send.get(f"{message_key} - Total Signals", ""), 
                                "Number of signals in this message"])

        # Reinsert the Total Receive Messages row at the end
        self.data_list.append(total_receive_row)

        self.endResetModel()



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
                self.populate_table(json_data)

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        print(filePath)
        json_gen.run(filePath) # creates JSON from raw at "testdata/data.json"
        
        # TODO potentially update test data path
        with open("test_data/data.json", "r") as file:
            json_data = json.load(file)
            self.populate_table(json_data)

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


    def populate_table(self, json_data):
        """Populate the table dynamically based on total_send and signals."""
        if not json_data:
            return

        total_send = json_data.get("total_send", 0)
        send_msgs = json_data.get("send_msgs", [])

        table_data = []
        table_data.append(["Total Send", total_send, "Total number of send messages"])

        for msg in send_msgs:
            table_data.append(["CAN_ID", msg["CAN_ID"], "CAN Identifier"])
            table_data.append(["Cycle Time", msg["cycle_time"], "Cycle time in ms"])
            table_data.append(["Data Length", msg["data_length"], "Data length in bytes"])
            table_data.append(["Attr", msg["attr"], "Attribute value"])
            table_data.append(["Total Signals", msg["total_signals"], "Number of signals in this message"])

            for signal in msg.get("signals", []):
                signal_desc = f"Type: {signal['signal_type']}, Bit Length: {signal['bit_length']}, Start Bit: {signal['start_bit']}, Attr: {signal['sig_attr']}"
                table_data.append([f"Signal {signal['index']}", signal_desc, "Signal properties"])

        self.model.update_data(table_data)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())