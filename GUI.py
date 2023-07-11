import sys
import numpy as np
import matplotlib.pyplot as plt
#from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMessageBox, QComboBox, QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from opcua import Client


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
        #dropdown_button.currentIndexChanged.connect(self.on_dropdown_selected)


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


        #Create reject button
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

        # Generate initial plot data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        initial_plot.plot(x, y)

        # Generate optimized plot data
        x_opt = np.linspace(0, 10, 200)
        y_opt = np.cos(x_opt)
        optimized_plot.plot(x_opt, y_opt)

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
        

    def plot(self, x, y):
        self.ax.plot(x, y)
        self.canvas.draw()
        self.ax.plot(x, y, color='black')  # Set the line color to red



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())






















    # import sys
# import random
# from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         # Set window title and icon
#         self.setWindowTitle("Two Plots GUI")
#         self.setWindowIcon(QIcon("icon.png"))

#         # Create the main layout
#         layout = QVBoxLayout()

#         # Create the initial plot widget
#         initial_plot_widget = QWidget()
#         initial_plot_layout = QVBoxLayout()
#         initial_plot_widget.setLayout(initial_plot_layout)
#         layout.addWidget(initial_plot_widget)

#         # Create the optimized plot widget
#         optimized_plot_widget = QWidget()
#         optimized_plot_layout = QVBoxLayout()
#         optimized_plot_widget.setLayout(optimized_plot_layout)
#         layout.addWidget(optimized_plot_widget)

#         # Create the initial plot
#         self.initial_plot = Figure(figsize=(5, 4), dpi=100)
#         self.initial_canvas = FigureCanvas(self.initial_plot)
#         initial_plot_layout.addWidget(self.initial_canvas)

#         # Create the optimized plot
#         self.optimized_plot = Figure(figsize=(5, 4), dpi=100)
#         self.optimized_canvas = FigureCanvas(self.optimized_plot)
#         optimized_plot_layout.addWidget(self.optimized_canvas)

#         # Set the main widget
#         main_widget = QWidget()
#         main_widget.setLayout(layout)
#         self.setCentralWidget(main_widget)

#         # Update the plots with random data
#         self.update_plots()

#     def update_plots(self):
#         # Clear the previous plots
#         self.initial_plot.clear()
#         self.optimized_plot.clear()

#         # Generate random data for the initial plot
#         initial_data = [random.randint(1, 10) for i in range(10)]
#         initial_ax = self.initial_plot.add_subplot(111)
#         initial_ax.plot(initial_data)

#         # Generate random data for the optimized plot
#         optimized_data = [random.randint(1, 10) for i in range(10)]
#         optimized_ax = self.optimized_plot.add_subplot(111)
#         optimized_ax.plot(optimized_data)

#         # Redraw the canvases to display the updated plots
#         self.initial_canvas.draw()
#         self.optimized_canvas.draw()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())