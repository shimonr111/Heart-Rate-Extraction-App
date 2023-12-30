import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import numpy as np


class VideoProcessor:
    def __init__(self, capture, video_window):
        self.capture = capture
        self.video_window = video_window
        self.green_channel = None
        self.green_channel_matrix = None

    def update_video_feed(self):
        ret, frame = self.capture.read()

        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                forehead_x = x
                forehead_y = y
                forehead_w = w
                forehead_h = int(h * 0.25)

                cv2.rectangle(frame, (forehead_x, forehead_y), (forehead_x + forehead_w, forehead_y + forehead_h),
                              (0, 0, 255), 2)

                forehead = frame[forehead_y:forehead_y + forehead_h, forehead_x:forehead_x + forehead_w]
                self.green_channel = forehead[:, :, 1]

                # Remove the unnecessary rows and columns that contain 0
                green_channel_array = np.array(self.green_channel)
                zero_rows = np.all(green_channel_array == 0, axis=1)
                zero_columns = np.all(green_channel_array == 0, axis=0)
                self.green_channel_matrix = green_channel_array[~zero_rows][:, ~zero_columns]

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = QImage(
                frame_rgb.data,
                frame_rgb.shape[1],
                frame_rgb.shape[0],
                QImage.Format_RGB888
            )

            image = image.scaled(
                self.video_window.width(),
                self.video_window.height(),
                Qt.KeepAspectRatio
            )

            pixmap = QPixmap.fromImage(image)

            self.video_window.setPixmap(pixmap)

    def get_green_channel(self):
        return self.green_channel_matrix
