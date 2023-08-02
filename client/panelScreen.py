import json
import os
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QComboBox
from PyQt5.QtCore import QFile, QTextStream, QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from specificPatientScreen import SpecificPatientScreen

class PanelScreen(QWidget):
    def __init__(self, app, client):
        super().__init__()
        self.app = app
        self.client = client
        self.setWindowTitle('Monitoring Heart Rate Application')
        self.resize(1500, 800)  # Set the window size
        # Initialize an empty list to store patient data
        self.patients_data = []
        # Create a QTimer instance
        self.timer = QTimer(self)
        # Set the interval (in milliseconds) for the timer to trigger the get_hr_value() function
        interval_milliseconds = 1000  # 1 second
        self.timer.setInterval(interval_milliseconds)
        # Connect the timeout signal of the timer to the get_hr_value() and get_pic() functions
        self.timer.timeout.connect(self.get_hr_value)
        self.timer.timeout.connect(self.get_pic)

        # Load and apply the CSS styles from the style.css file
        style_file = QFile('style.css')
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_stream = QTextStream(style_file)
            app.setStyleSheet(style_stream.readAll())

        # Add title label
        title_label = QLabel('Panel Patient Control', self)
        title_label.move(660, 0)  # x,y coordinates value from top-left corner
        title_label.setObjectName('title_label')  # set object name for using it in the css file

        # Add the combobox to select the Patient1
        self.patient1_combobox = QComboBox(self)
        self.patient1_combobox.move(430, 370)  # x,y coordinates value from top-left corner
        # Title of Patient1 label
        self.patient1Title_label = QLabel('', self)
        self.patient1Title_label.move(430, 400)  # x,y coordinates value from top-left corner
        self.patient1Title_label.setObjectName('patientTitle_label')  # set object name for using it in the css file
        # Frequency of Patient1 label
        freq1_label = QLabel('Frequency:', self)
        freq1_label.move(430, 640)  # x,y coordinates value from top-left corner
        freq1_label.setObjectName('freq_label')  # set object name for using it in the css file
        # Heart rate of Patient1 label
        self.hr1_label = QLabel('Heart rate:', self)
        self.hr1_label.move(430, 670)  # x,y coordinates value from top-left corner
        self.hr1_label.setObjectName('hr_label')  # set object name for using it in the css file
        # Enter to Patient1 Button
        self.enter1_button = QPushButton('Enter', self)
        self.enter1_button.move(430, 700)  # x,y coordinates value from top-left corner
        self.enter1_button.clicked.connect(lambda: self.enter_clicked('1'))  # Connect to the enter_clicked function with parameter 1
        # Create a window to display the facial footage of Patient1
        self.facial_footage1 = QLabel(self)
        self.facial_footage1.move(430, 450)
        self.facial_footage1.setFixedSize(150, 150)
        self.facial_footage1.setStyleSheet("border: 2px solid black;")

        # Add the combobox to select the Patient2
        self.patient2_combobox = QComboBox(self)
        self.patient2_combobox.move(680, 370)  # x,y coordinates value from top-left corner
        # Title of Patient2 label
        self.patient2Title_label = QLabel('', self)
        self.patient2Title_label.move(680, 400)  # x,y coordinates value from top-left corner
        self.patient2Title_label.setObjectName('patientTitle_label')  # set object name for using it in the css file
        # Frequency of Patient2 label
        freq2_label = QLabel('Frequency:', self)
        freq2_label.move(680, 640)  # x,y coordinates value from top-left corner
        freq2_label.setObjectName('freq_label')  # set object name for using it in the css file
        # Heart rate of Patient2 label
        self.hr2_label = QLabel('Heart rate:', self)
        self.hr2_label.move(680, 670)  # x,y coordinates value from top-left corner
        self.hr2_label.setObjectName('hr_label')  # set object name for using it in the css file
        # Enter to Patient2 Button
        self.enter2_button = QPushButton('Enter', self)
        self.enter2_button.move(680, 700)  # x,y coordinates value from top-left corner
        self.enter2_button.clicked.connect(lambda: self.enter_clicked('2'))  # Connect to the enter_clicked function with parameter 2
        # Create a window to display the facial footage of Patient2
        self.facial_footage2 = QLabel(self)
        self.facial_footage2.move(680, 450)
        self.facial_footage2.setFixedSize(150, 150)
        self.facial_footage2.setStyleSheet("border: 2px solid black;")

        # Add the combobox to select the Patient3
        self.patient3_combobox = QComboBox(self)
        self.patient3_combobox.move(930, 370)  # x,y coordinates value from top-left corner
        # Title of Patient3 label
        self.patient3Title_label = QLabel('', self)
        self.patient3Title_label.move(930, 400)  # x,y coordinates value from top-left corner
        self.patient3Title_label.setObjectName('patientTitle_label')  # set object name for using it in the css file
        # Frequency of Patient3 label
        freq3_label = QLabel('Frequency:', self)
        freq3_label.move(930, 640)  # x,y coordinates value from top-left corner
        freq3_label.setObjectName('freq_label')  # set object name for using it in the css file
        # Heart rate of Patient3 label
        self.hr3_label = QLabel('Heart rate:', self)
        self.hr3_label.move(930, 670)  # x,y coordinates value from top-left corner
        self.hr3_label.setObjectName('hr_label')  # set object name for using it in the css file
        # Enter to Patient3 Button
        self.enter3_button = QPushButton('Enter', self)
        self.enter3_button.move(930, 700)  # x,y coordinates value from top-left corner
        self.enter3_button.clicked.connect(lambda: self.enter_clicked('3'))  # Connect to the enter_clicked function with parameter 3
        # Create a window to display the facial footage of Patient3
        self.facial_footage3 = QLabel(self)
        self.facial_footage3.move(930, 450)
        self.facial_footage3.setFixedSize(150, 150)
        self.facial_footage3.setStyleSheet("border: 2px solid black;")

        # Back button
        back_button = QPushButton('Back', self)
        back_button.move(10, 10)  # Adjust the position of the back button
        back_button.clicked.connect(self.back_clicked)  # Connect the button's clicked signal to the go_back method

        # Update button states based on JSON data
        self.update_button_states_in_gui()

        # Update the combo boxes with patients' names from the server
        self.update_patients_comboboxes()

        # Initialize the text of the labels Patient 1, 2, 3
        self.initialize_patient_labels()

        # Start the timer and calling get_hr_value() and get_pic() every 1 second
        self.timer.start()

        # Connect the activated signal of each combo box to the method
        # that retrieves the selected value
        self.patient1_combobox.activated.connect(lambda: self.get_selected_value_from_combobox("1"))
        self.patient2_combobox.activated.connect(lambda: self.get_selected_value_from_combobox("2"))
        self.patient3_combobox.activated.connect(lambda: self.get_selected_value_from_combobox("3"))

        # Display the pics of the patients
        #self.get_pic()

    # When the user exit from the window
    def closeEvent(self, event):
        # Send a request to the server to leave the panel screen
        self.client.send('LEAVE_PANEL_SCREEN'.encode("utf-8"))
        event.accept()  # Accept the close event

    # Triggered when enter button pressed
    def enter_clicked(self, patient):
        # Send a request to the server to leave the panel screen
        self.client.send('LEAVE_PANEL_SCREEN'.encode("utf-8"))

        if patient == '1':
            self.update_button_state_in_json('1', "no")
        elif patient == '2':
            self.update_button_state_in_json('2', "no")
        elif patient == '3':
            self.update_button_state_in_json('3', "no")

        self.window_specificPatient_screen = SpecificPatientScreen(self.app, self.client, patient)
        self.window_specificPatient_screen.show()
        self.hide()

    # Go back to the previous window
    def back_clicked(self):
        # Send a request to the server to leave the panel screen
        self.client.send('LEAVE_PANEL_SCREEN'.encode("utf-8"))

        from menuScreen import MenuScreen
        self.window_menu_screen = MenuScreen(self.app, self.client)
        self.window_menu_screen.show()
        self.hide()

    # Update button states based on JSON data
    def update_button_states_in_gui(self):
        # Send a 'get button states' request to the server
        self.client.send('GET_BUTTON_STATES'.encode("utf-8"))

        # Receive the button states from the server
        button_states = self.client.recv(1024).decode("utf-8")
        # Parse the JSON string into a Python object
        button_states = json.loads(button_states)

        for state in button_states:
            button_id = state['id']
            enabled = state['enabled']

            if button_id == '1':
                self.enter1_button.setEnabled(enabled == 'yes')
            elif button_id == '2':
                self.enter2_button.setEnabled(enabled == 'yes')
            elif button_id == '3':
                self.enter3_button.setEnabled(enabled == 'yes')

    # Update button state in JSON data base
    def update_button_state_in_json(self, patient_id, enabled):
        # Prepare the patient data to be sent to the server
        patient_data = {
            "enabled": enabled,
            "id": patient_id
        }

        # Send a 'UPDATE_BUTTON_STATES' request to the server
        self.client.send('UPDATE_BUTTON_STATES'.encode("utf-8"))

        # Send the patient data to the server
        self.client.send(json.dumps(patient_data).encode("utf-8"))

    # Function to update the combo boxes with patients' names
    def update_patients_comboboxes(self):
        # Send the request for patients' data
        self.client.send('GET_PATIENTS_DATA'.encode('utf-8'))

        # Receive the data from the server and decode it
        received_data = self.client.recv(1024).decode('utf-8')

        # Parse the received data into a list of patients' information
        self.patients_data = json.loads(received_data)

        # Clear the combo boxes
        self.patient1_combobox.clear()
        self.patient2_combobox.clear()
        self.patient3_combobox.clear()

        # Add patient names (first name and family name) to the combo boxes
        for patient in self.patients_data:
            first_name = patient['firstName']
            last_name = patient['lastName']
            self.patient1_combobox.addItem(f"{first_name} {last_name}")
            self.patient2_combobox.addItem(f"{first_name} {last_name}")
            self.patient3_combobox.addItem(f"{first_name} {last_name}")

    # Function to initialize the text of the Patient1/2/3 labels
    def initialize_patient_labels(self):
        # Send the request for patientsInTreatment data
        self.client.send('GET_PATIENTS_IN_TREATMENT_DATA'.encode('utf-8'))

        # Receive the data from the server and decode it
        received_data = self.client.recv(1024).decode('utf-8')

        # Parse the received data into a list of patients' information
        patients_in_treatment = json.loads(received_data)

        # Set the text of the labels Patient 1, 2, 3 based on the data
        for patient in patients_in_treatment:
            patient_num = patient['patient']
            first_name = patient['firstName']
            last_name = patient['lastName']

            if patient_num == '1':
                self.patient1Title_label.setText(f'{first_name} {last_name}')
            elif patient_num == '2':
                self.patient2Title_label.setText(f'{first_name} {last_name}')
            elif patient_num == '3':
                self.patient3Title_label.setText(f'{first_name} {last_name}')

    # Update the patients that in treatment so when other clients access to the panel screen,
    # It will show them the updated patient name in the label
    def get_selected_value_from_combobox(self, num):
        # Get the selected text from the respective combo box
        if num == "1":
            selected_patient = self.patient1_combobox.currentText()
            self.update_patients_in_treatment(selected_patient, num)
            self.patient1Title_label.setText(f'{selected_patient}')
        elif num == "2":
            selected_patient = self.patient2_combobox.currentText()
            self.update_patients_in_treatment(selected_patient, num)
            self.patient2Title_label.setText(f'{selected_patient}')
        elif num == "3":
            selected_patient = self.patient3_combobox.currentText()
            self.update_patients_in_treatment(selected_patient, num)
            self.patient3Title_label.setText(f'{selected_patient}')
        else:
            selected_patient = None

    # Sub function of get_selected_value_from_combobox()
    def update_patients_in_treatment(self, selected_patient, num):
        first_name, last_name = selected_patient.split()

        # Prepare the patient data to be sent to the server
        patient_data = {
            "firstName": first_name,
            "lastName": last_name,
            "patient": num
        }

        self.client.send('UPDATE_PATIENTS_IN_TREATMENT_DATA'.encode('utf-8'))
        # Send the patient data to the server
        self.client.send(json.dumps(patient_data).encode("utf-8"))

    # Receive the heart rate of the patients from the server, and display it on the gui
    # This function called every 1 second because the heart rate updated
    def get_hr_value(self):
        self.client.send('GET_HEART_RATE'.encode('utf-8'))

        # Receive the result from the server
        result = self.client.recv(1024).decode("utf-8")

        # Parse the received JSON data into a dictionary
        data = json.loads(result)

        hr1 = data['heart_rate1']
        hr2 = data['heart_rate2']
        hr3 = data['heart_rate3']
        # Display the updated heart rate on the labels
        self.hr1_label.setText(str(hr1))
        self.hr2_label.setText(str(hr2))
        self.hr3_label.setText(str(hr3))

    # Function to get and display the patient images in the facial footage QLabel
    def get_pic(self):
        for patient_num in ['1', '2', '3']:
            # Construct the image file name based on the patient number (1, 2, or 3)
            image_name = f"patient_{patient_num}_image.jpg"
            image_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'pics', image_name)

            # Check if the image file exists
            if os.path.exists(image_path):
                # Load the image using OpenCV
                image = cv2.imread(image_path)

                # Convert the image from BGR to RGB format
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Convert the RGB image to QImage
                image_qt = QImage(
                    image_rgb.data,
                    image_rgb.shape[1],
                    image_rgb.shape[0],
                    QImage.Format_RGB888
                )

                # Resize the image to match the size of the QLabel
                image_qt = image_qt.scaled(
                    self.facial_footage1.width(),
                    self.facial_footage1.height()
                )

                # Convert the QImage to QPixmap for display
                pixmap = QPixmap.fromImage(image_qt)

                # Set the pixmap on the corresponding facial footage QLabel
                if patient_num == '1':
                    self.facial_footage1.setPixmap(pixmap)
                    self.facial_footage1.setAlignment(Qt.AlignCenter)
                elif patient_num == '2':
                    self.facial_footage2.setPixmap(pixmap)
                    self.facial_footage2.setAlignment(Qt.AlignCenter)
                elif patient_num == '3':
                    self.facial_footage3.setPixmap(pixmap)
                    self.facial_footage3.setAlignment(Qt.AlignCenter)
            else:
                # If the image file does not exist, clear the corresponding facial footage QLabel
                if patient_num == '1':
                    self.facial_footage1.clear()
                elif patient_num == '2':
                    self.facial_footage2.clear()
                elif patient_num == '3':
                    self.facial_footage3.clear()




