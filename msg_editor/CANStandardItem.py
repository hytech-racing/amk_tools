from PyQt5.QtGui import QStandardItem

class CANStandardItem(QStandardItem):
    def __init__(self, text, message, binding, tree_update):
        super().__init__(str(text))
        self.message = message
        self.binding = binding
        self.tree_update = tree_update
    
    def setData(self, value, role):
        info = self.message.mappings[self.binding]
        print("Updating to " + value)
        try:
            info["function"](int(value))
        except Exception as e:
            print(e)
            return
    
        super().setData(value, role)
        self.tree_update()