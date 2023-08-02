import cv2
import numpy as np
import json
import os
from scipy.signal import find_peaks
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtCore import QFile, QTextStream, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QElapsedTimer
from PIL import Image

class SpecificPatientScreen(QWidget):
    def __init__(self, app, client, patient):
        super().__init__()
        self.app = app
        self.client = client
        self.patient = patient
        self.capture = None  # Initialize self.capture as None
        self.setWindowTitle('Monitoring Heart Rate Application')
        self.resize(1500, 800)  # Set the window size
        self.picture_captured = False  # Initialize the flag to False - it didn't capture pic yet

        # Heart rate calculation variables
        self.green_channel = None
        self.fft_peaks = []
        self.heart_rate = 0
        self.timer_started = False
        self.timer = QElapsedTimer()

        # Timer to update heart rate every second
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_heart_rate)

        # Load and apply the CSS styles from the style.css file
        style_file = QFile('style.css')
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_stream = QTextStream(style_file)
            app.setStyleSheet(style_stream.readAll())

        # Frequency of Patient label
        freq_label = QLabel('Frequency:', self)
        freq_label.move(1200, 100)  # x,y coordinates value from top-left corner
        freq_label.setObjectName('freq_label')  # set object name for using it in the css file

        # Heart rate of Patient label
        self.hr_label = QLabel('Heart rate:', self)
        self.hr_label.move(1200, 200)  # x,y coordinates value from top-left corner
        self.hr_label.setObjectName('hr_label')  # set object name for using it in the css file

        # Combo box for choosing Live or captured video
        video_combo_box = QComboBox(self)
        video_combo_box.addItem("Video")
        video_combo_box.addItem("Webcam")
        video_combo_box.move(200, 500)

        # Open button to upload video from DB or local memory
        self.open_button = QPushButton('Open', self)
        self.open_button.move(350, 500)  # x,y coordinates value from top-left corner
        self.open_button.clicked.connect(self.open_clicked)

        video_combo_box.setFixedSize(self.open_button.sizeHint())  # Set fixed size based on the button size hint

        # Start button to start extracting the HR
        start_button = QPushButton('Start', self)
        start_button.move(500, 500)  # x,y coordinates value from top-left corner
        start_button.clicked.connect(self.start_clicked)

        # Back button
        back_button = QPushButton('Back', self)
        back_button.move(10, 10)  # Adjust the position of the back button
        back_button.clicked.connect(self.back_clicked)  # Connect the button's clicked signal to the go_back method

        # Create a window to display the HR
        self.hr_window = QLabel(self)
        self.hr_window.move(1000, 80)
        self.hr_window.setFixedSize(150, 150)
        self.hr_window.setStyleSheet("border: 2px solid black;")

        # Create a window to display the FFT Signals
        self.fft_window = QLabel(self)
        self.fft_window.move(1000, 300)
        self.fft_window.setFixedSize(300, 150)
        self.fft_window.setStyleSheet("border: 2px solid black;")

        # Create a window to display the RGB Signals
        self.rgb_window = QLabel(self)
        self.rgb_window.move(1000, 480)
        self.rgb_window.setFixedSize(300, 150)
        self.rgb_window.setStyleSheet("border: 2px solid black;")

        # Create a window to display the video
        self.video_window = QLabel(self)
        self.video_window.move(140, 50)
        self.video_window.setFixedSize(500, 400)
        self.video_window.setStyleSheet("border: 2px solid black;")

        # Create a QTimer to continuously update the video feed
        self.timerVideo = QTimer(self)
        self.timerVideo.timeout.connect(self.update_video_feed)

        # Triggered when combo box changed
        video_combo_box.currentIndexChanged.connect(self.combo_box_changed)

    # Go back to the previous window
    def back_clicked(self):
        # Stop the video feed
        if self.capture is not None:
            self.stop_video_feed()

        # Delete the patient's image
        self.delete_patient_image()

        # Send a request to the server to enter the panel screen
        self.client.send('ENTER_PANEL_SCREEN'.encode("utf-8"))
        response = self.client.recv(1024).decode("utf-8")
        # Entry is allowed, navigate to the PanelScreen page
        if response == 'ENTRY_ALLOWED':
            if self.patient == '1':
                self.update_button_state_in_json('1', "yes")
            elif self.patient == '2':
                self.update_button_state_in_json('2', "yes")
            elif self.patient == '3':
                self.update_button_state_in_json('3', "yes")

            from panelScreen import PanelScreen
            self.window_panel_screen = PanelScreen(self.app, self.client)
            self.window_panel_screen.show()
            self.hide()
            self.timer_started = False  # Stop the heart rate calculation loop
        else:
            # Entry is denied, display an error message or handle it accordingly
            QMessageBox.warning(self, "Entry Denied", "Only one client can enter the PanelScreen page.")

    # Handle combo box selection change
    def combo_box_changed(self, index):
        if index == 1:  # Webcam option selected
            self.open_button.setDisabled(True)
            self.start_video_feed()
        else:
            self.delete_patient_image()
            self.stop_video_feed()
            self.open_button.setDisabled(False)
            self.picture_captured = False
        self.timer_started = False  # Stop the heart rate calculation loop

    # Start video feed (webcam or captured video)
    def start_video_feed(self, file_path=None):
        if file_path is None:
            self.capture = cv2.VideoCapture(0)  # Open the default webcam (index 0)
        else:
            self.capture = cv2.VideoCapture(file_path)

        self.timerVideo.start(30)  # Start the timer with an interval of 30 milliseconds

    # Stop video feed
    def stop_video_feed(self):
        self.timerVideo.stop()
        self.capture.release()
        self.video_window.clear()

    # Update the video feed
    def update_video_feed(self):
        ret, frame = self.capture.read()  # Read a frame from the video feed

        if ret:
            # Convert the frame to grayscale for face and forehead detection
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Load the Haar cascade classifiers for face and eyes detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                # Calculate the forehead region of interest (ROI) coordinates
                forehead_x = x
                forehead_y = y
                forehead_w = w
                forehead_h = int(h * 0.25)

                # Draw a rectangle around the forehead
                cv2.rectangle(frame, (forehead_x, forehead_y), (forehead_x + forehead_w, forehead_y + forehead_h),
                              (0, 0, 255), 2)

                # Extract the green channel from the forehead region
                forehead = frame[forehead_y:forehead_y + forehead_h, forehead_x:forehead_x + forehead_w]
                self.green_channel = forehead[:, :, 1]  # Green channel

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to QImage
            image = QImage(
                frame_rgb.data,
                frame_rgb.shape[1],
                frame_rgb.shape[0],
                QImage.Format_RGB888
            )

            # Resize the image to match the size of the QLabel
            image = image.scaled(
                self.video_window.width(),
                self.video_window.height(),
                Qt.KeepAspectRatio
            )

            # Convert the QImage to QPixmap for display
            pixmap = QPixmap.fromImage(image)

            # Set the pixmap on the QLabel
            self.video_window.setPixmap(pixmap)

            # Capture the picture of the patient and store it in the server
            if not self.picture_captured:
                self.capture_picture()
                self.picture_captured = True  # Set the flag to True after capturing the picture

    # Open button clicked
    def open_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov)", options=options)
        if file_path:
            self.start_video_feed(file_path)

    # Start button clicked
    def start_clicked(self):
        if self.green_channel is not None:
            self.timer_started = True
            self.timer.start()
            self.update_timer.start(1000)  # Update heart rate every second

    # Update the heart rate label
    def update_heart_rate(self):
        if self.timer_started:
            result = self.calculate_heart_rate()
            self.hr_label.setText(str(result))

            # Send the updated heart rate to the server side
            data = {
                "heart_rate": result,
                "num": self.patient
            }
            json_data = json.dumps(data)
            self.client.send('HEART_RATE_UPDATE'.encode("utf-8"))
            self.client.send(json_data.encode("utf-8"))

    # Calculate the heart rate based on the green channel
    def calculate_heart_rate(self):
        if not self.timer_started:
            return 0  # Return 0 if the heart rate calculation is not started

        # Perform FFT on the Green Channel
        fft_result = np.fft.fft(self.green_channel)
        fft_result = np.abs(fft_result).flatten()
        fft_freq = np.fft.fftfreq(len(fft_result))

        # Locate peaks in the necessary frequency range
        peaks, _ = find_peaks(fft_result, height=0, threshold=0)

        # Filter peaks within the necessary frequency range
        valid_peaks = peaks[(fft_freq[peaks] >= 0.48) & (fft_freq[peaks] <= 4)]

        # Count the peaks within a set time range
        elapsed_time = self.timer.elapsed() / 1000  # Elapsed time in seconds
        if elapsed_time > 0:
            # Calculate the peak count within the set time range
            peak_count = len(valid_peaks)

            # Calculate the heart rate
            heart_rate = peak_count * 60 / elapsed_time  # Convert to BPM using elapsed time
            self.heart_rate = round(heart_rate)
        else:
            self.heart_rate = 0
        return self.heart_rate

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

    # Capture the picture of the patient
    def capture_picture(self):
        if self.green_channel is not None:
            # Get the original frame from the capture
            ret, frame = self.capture.read()

            if ret:
                # Save the frame to the "pics" folder
                pics_folder = os.path.join(os.path.dirname(__file__), '..', 'server', 'pics')
                os.makedirs(pics_folder, exist_ok=True)  # Create the "pics" folder if it doesn't exist
                image_name = "patient_" + self.patient + "_image.jpg"
                image_path = os.path.join(pics_folder, image_name)

                # Convert the frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the RGB frame to a PIL Image
                image = Image.fromarray(frame_rgb)

                # Save the image
                image.save(image_path, format="JPEG")

    # Method to delete the patient's image
    def delete_patient_image(self):
        pics_folder = os.path.join(os.path.dirname(__file__), '..', 'server', 'pics')
        image_name = "patient_" + self.patient + "_image.jpg"
        image_path = os.path.join(pics_folder, image_name)
        if os.path.exists(image_path):
            os.remove(image_path)


