import sys
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


        importAction = QAction("Import", self)
        importAction.triggered.connect(self.importJsonFile)

        exportAction = QAction("Export", self)

        fileMenu.addAction(importAction)
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


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicWindow()
    window.show()
    sys.exit(app.exec_())