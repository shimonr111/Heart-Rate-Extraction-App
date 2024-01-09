from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class Temp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monitoring Heart Rate Application')
        self.resize(1500, 800)  # Set the window size

        # Create a window to display the HR
        self.hr_window = QWidget(self)
        self.hr_window.setGeometry(1000, 80, 400, 400)
        self.hr_window.setStyleSheet("border: 2px solid black;")
        layout = QVBoxLayout(self.hr_window)

        # Create Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.hr_window)

        # Generate some random data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        # Plot the data
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title('Random Plot')
        # Redraw the canvas
        self.canvas.draw()

        layout.addWidget(self.canvas)
        self.hr_window.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    specific_patient_screen = Temp()
    specific_patient_screen.show()
    app.exec_()
