import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMessageBox, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from opcua import Client
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set window title
        self.setWindowTitle("GUI Transparency")
        self.setStyleSheet("background-color: lightblue;")

        # Create a QComboBox for the dropdown button
        dropdown_button = QComboBox()
        dropdown_button.addItem("Option 1")
        dropdown_button.addItem("Option 2")
        dropdown_button.addItem("Option 3")
        dropdown_button.addItem("Option 4")

        # Create main layout
        layout = QVBoxLayout()

        # Create horizontal layout for dropdown and spacer
        top_layout = QHBoxLayout()

        # Add horizontal spacer item to push the dropdown button to the right
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_layout.addItem(spacer_item)

        top_layout.addWidget(dropdown_button)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        # Create initial plot widget
        initial_plot = PlotWidget(self, title="Initial Plot")
        layout.addWidget(initial_plot)

        # Create optimized plot widget
        optimized_plot = PlotWidget(self, title="Optimized Plot")
        layout.addWidget(optimized_plot)

        # Create accept and reject buttons
        button_layout = QHBoxLayout()
        accept_button = QPushButton("Accept")
        accept_button.setStyleSheet("background-color: green; color: white;")
        accept_button.clicked.connect(self.on_accept)
        accept_button.setFixedSize(80, 30)

        # Create reject button
        reject_button = QPushButton("Reject")
        reject_button.setStyleSheet("background-color: red; color: white;")
        reject_button.clicked.connect(self.on_reject)
        reject_button.setFixedSize(80, 30)

        button_layout.addWidget(accept_button)
        button_layout.addWidget(reject_button)
        layout.addLayout(button_layout)

        # Create central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # File paths of the generated plots
        initial_plot_path = "path/to/initial_plot.png"
        optimized_plot_path = "path/to/optimized_plot.png"

        # Load and display the plot images in the plot widgets
        initial_plot.load_plot_image(initial_plot_path)
        optimized_plot.load_plot_image(optimized_plot_path)

    def on_accept(self):
        result = QMessageBox.question(
            self, "Accept Parameters",
            "Do you want to accept the optimized parameters?",
            QMessageBox.Yes | QMessageBox.No
        )
        if result == QMessageBox.Yes:
            print("Accepted")
            # Perform further actions for accepting parameters

            # Connect to OPC UA server
            client = Client("opc.tcp://plc_address:port")
            client.connect()

            # Browse OPC UA address space and find the target node to write parameters
            # target_node = "modbus_buffer"."iSpeedandTime"...
            #"DigitalTwin_To_Recipe"."SS1_accept"

            # Write the accepted parameters to the target node
            # client.write_value(target_node, accepted_parameters)

            # Disconnect from OPC UA server
            client.disconnect()
        else:
            print("Not Accepted")

    def on_reject(self):
        result = QMessageBox.question(
            self, "Reject Parameters",
            "Do you want to reject the optimized parameters?",
            QMessageBox.Yes | QMessageBox.No
        )
        if result == QMessageBox.Yes:
            print("Rejected")
            # Perform actions for rejecting parameters
        else:
            print("Not Rejected")


class PlotWidget(QWidget):
    def __init__(self, parent=None, title=""):
        super(PlotWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def load_plot_image(self, file_path):
        # Load the plot image from the specified file path
        pixmap = QPixmap(file_path)

        # Scale the image to fit the widget size
        pixmap = pixmap.scaled(self.size(), aspectRatioMode=Qt.KeepAspectRatio)

        # Set the image as the background of the widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
