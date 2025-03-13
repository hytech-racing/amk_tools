from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMessageBox

def showWarning(title, message):
    box = QMessageBox()
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle(title)
    box.setText(message)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec_()
class CANStandardItem(QStandardItem):
    def __init__(self, text, message, binding, tree_update):
        super().__init__(str(text))
        self.message = message
        self.binding = binding
        self.tree_update = tree_update
    
    def setData(self, value, role):
        info = self.message.mappings[self.binding]
        try:
            info["function"](int(value))
        except Exception as e:
            # TODO here
            showWarning("Bad Value", f"{e}\n\n \"{value}\" is not a valid value.")
            return
    
        super().setData(value, role)
        self.tree_update()