import sys
import json_gen
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon

class BasicWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

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

    def importJsonFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import JSON File", "", "JSON Files (*.json)")
        if filePath:
            # Open the selected file and read its contents
            with open(filePath, "r") as file:
                json_data = file.read()

                # This only displays raw JSON to window. -----------------
                # TODO initialize table with proper attributes, see Excel
                #      example
                #
                # Create a QTextEdit widget to display the JSON data
                textEdit = QTextEdit(self)
                textEdit.setText(json_data)
                # Add the QTextEdit widget to the window
                self.setCentralWidget(textEdit)
                # --------------------------------------------------------

    def importRawFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Raw File", "", "")
        print(filePath)
        json_gen.run(filePath) # creates JSON from raw at "testdata/data.json"
        
        # TODO potentially update test data path
        with open("test_data/data.json", "r") as file:
            json_data = file.read()
            # This only displays raw JSON to window. -----------------
            # TODO initialize table with proper attributes, see Excel
            #      example
            #
            # Create a QTextEdit widget to display the JSON data
            textEdit = QTextEdit(self)
            textEdit.setText(json_data)
            # Add the QTextEdit widget to the window
            self.setCentralWidget(textEdit)
            # --------------------------------------------------------


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicWindow()
    window.show()
    sys.exit(app.exec_())