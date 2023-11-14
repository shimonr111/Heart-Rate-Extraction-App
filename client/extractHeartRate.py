import numpy as np
from scipy.signal import find_peaks


class ExtractHeartRate:
    def __init__(self, green_channel, timer):
        self.green_channel = green_channel
        self.timer = timer
        self.heart_rate = 0

    def calc_hr_process(self):
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
