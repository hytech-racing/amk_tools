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

    # def setData(self, value, role):
    #     try:
    #         if hasattr(self.message, "mappings") and self.binding in self.message.mappings:
    #             info = self.message.mappings[self.binding]
    #             print(f"Updating {self.binding} to {value}")
    #             try:
    #                 info["function"](int(value))
    #             except Exception as e:
    #                 print("Invalid input:", e)
    #                 return
    #         else:
    #             print(f"Warning: '{self.binding}' not found in mappings of {type(self.message).__name__}")
    #             if hasattr(self.message, "mappings"):
    #                 print(f"Available mappings: {list(self.message.mappings.keys())}")
    #             else:
    #                 print(f"{type(self.message).__name__} does not have a mappings attribute.")

    #             return

    #         super().setData(value, role)
    #     except Exception as e:
    #         print(f"Error in setData: {e}")