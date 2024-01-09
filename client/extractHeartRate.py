import numpy as np
from scipy.signal import find_peaks
from scipy.fftpack import fft


class ExtractHeartRate:
    def __init__(self, green_channel):
        self.green_channel = green_channel
        self.heart_rate = 0
        self.frequency = 0

    def calc_hr_process(self):
        if self.green_channel is None:
            return 0, 0, "Face did not detected"
        # Check if the face too close to the camera, or far from the camera, so it won't return good result
        # Checking it by the shape of the matrix of the forehead (the green channel)
        if not (47 <= self.green_channel.shape[0] <= 54 or 213 <= self.green_channel.shape[0] <= 222):
            if self.green_channel.shape[0] < 47 or self.green_channel.shape[1] < 213:
                return 0, 0, "Face is too far from the camera"
            else:
                return 0, 0, "Face is too close to the camera"

        length_of_green_channel = len(self.green_channel)
        # The heart rate frequency is typically within the range of 0.75 Hz to 4 Hz.
        # Therefore, a sampling rate of 30 Hz should be sufficient to capture these frequencies
        # according to the Nyquist-Shannon sampling theorem
        sampling_rate = 30
        # Computes the frequencies corresponding to the signal.
        frequencies = np.fft.fftfreq(length_of_green_channel, d=1 / sampling_rate)
        # Filter frequencies between 0.75 Hz and 4 Hz
        mask = (frequencies >= 0.75) & (frequencies <= 4)

        # The green channel is transformed to the frequency domain by applying FFT
        fft_result = fft(self.green_channel)
        # Find the peaks which will contain the indices of the detected peaks in the frequency domain
        peaks, _ = find_peaks(np.abs(fft_result[mask]).flatten())

        time_range = [15, 30]
        # The number of peaks is calculated
        peaks_count = len(peaks) / (time_range[1] - time_range[0])
        # The heart rate is determined by convert the result to beats per minute
        self.heart_rate = peaks_count / (time_range[1] - time_range[0]) * 60
        self.frequency = frequencies[peaks[0]]

        return round(self.heart_rate, 3), round(self.frequency, 3), None
