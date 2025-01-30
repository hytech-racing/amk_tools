import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle("Basic PyQt5 Window")

        # Set window size
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

        # Create a label
        label = QLabel("Hello, this is a basic PyQt5 window!", self)

        # Set up a layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicWindow()
    window.show()
    sys.exit(app.exec_())