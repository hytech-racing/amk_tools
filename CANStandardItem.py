from PyQt5.QtGui import QStandardItem

class CANStandardItem(QStandardItem):
    def __init__(self, text, message, binding):
        super().__init__(text)
        self.message = message
        self.binding = binding
    
    def setData(self, value, role):
        info = self.message.mappings[self.binding]
        print("Updating to " + value)
        try:
            info["function"](int(value))
        except Exception as e:
            print("this wus a bad output!!!")
            return
            

        super().setData(value, role)