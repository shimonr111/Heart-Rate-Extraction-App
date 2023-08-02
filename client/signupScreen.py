from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QFile, QTextStream
import json

class SignupScreen(QWidget):
    def __init__(self, app, client):
        super().__init__()
        self.app = app
        self.client = client
        self.setWindowTitle('Monitoring Heart Rate Application')
        self.resize(1500, 800)  # Set the window size

        # Load and apply the CSS styles from the style.css file
        style_file = QFile('style.css')
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_stream = QTextStream(style_file)
            app.setStyleSheet(style_stream.readAll())

        # Add title label
        title_label = QLabel('Sign Up', self)
        title_label.move(660, 0)  # x,y coordinates value from top-left corner
        title_label.setObjectName('title_label')  # set object name for using it in the css file

        # ID label
        id_label = QLabel('ID:', self)
        id_label.move(500, 200)  # x,y coordinates value from top-left corner
        id_label.setObjectName('id_label')  # set object name for using it in the css file
        # ID input
        self.id_input = QLineEdit(self)
        self.id_input.move(620, 200)  # x,y coordinates value from top-left corner
        self.id_input.setObjectName('id_input')  # set object name for using it in the css file
        self.id_input.setFixedWidth(200)  # Decrease the width to 200 pixels

        # First Name label
        firstName_label = QLabel('First Name:', self)
        firstName_label.move(500, 300)  # x,y coordinates value from top-left corner
        firstName_label.setObjectName('firstName_label')  # set object name for using it in the css file
        # First Name input
        self.firstName_input = QLineEdit(self)
        self.firstName_input.move(620, 300)  # x,y coordinates value from top-left corner
        self.firstName_input.setObjectName('firstName_input')  # set object name for using it in the css file
        self.firstName_input.setFixedWidth(200)  # Decrease the width to 200 pixels

        # Last Name label
        lastName_label = QLabel('Last Name:', self)
        lastName_label.move(500, 400)  # x,y coordinates value from top-left corner
        lastName_label.setObjectName('lastName_label')  # set object name for using it in the css file
        # Last Name input
        self.lastName_input = QLineEdit(self)
        self.lastName_input.move(620, 400)  # x,y coordinates value from top-left corner
        self.lastName_input.setObjectName('lastName_input')  # set object name for using it in the css file
        self.lastName_input.setFixedWidth(200)  # Decrease the width to 200 pixels

        # Add patient Button
        add_button = QPushButton('Add patient', self)
        add_button.move(660, 500)  # x,y coordinates value from top-left corner
        add_button.clicked.connect(self.add_clicked)

        # Back button
        back_button = QPushButton('Back', self)
        back_button.move(10, 10)  # Adjust the position of the back button
        back_button.clicked.connect(self.back_clicked)  # Connect the button's clicked signal to the go_back method

        # Add patient label
        self.add_label = QLabel('', self)
        self.add_label.move(630, 550)

    # Go back to the previous window
    def back_clicked(self):
        from menuScreen import MenuScreen
        self.window_menu_screen = MenuScreen(self.app, self.client)
        self.window_menu_screen.show()
        self.hide()

    # Triggered when add patient button clicked
    def add_clicked(self):
        entered_id = self.id_input.text()
        entered_firstName = self.firstName_input.text()
        entered_lastName = self.lastName_input.text()

        # Hide the previous add label
        self.add_label.hide()

        # Prepare the patient data to be sent to the server
        patient_data = {
            "id": entered_id,
            "firstName": entered_firstName,
            "lastName": entered_lastName
        }

        # Send a 'add patient request' to the server
        self.client.send('ADD_PATIENT_REQUEST'.encode("utf-8"))

        # Send the patient data to the server
        self.client.send(json.dumps(patient_data).encode("utf-8"))

        # Receive the login result from the server
        added_result = self.client.recv(1024).decode("utf-8")

        # Added new patient failed
        if added_result == "True":
            self.add_label.setText('The id already exist in the system')
            self.add_label.show()
        # Added new patient succeed
        else:
            self.add_label.setText('Added new patient!')
            self.add_label.show()

