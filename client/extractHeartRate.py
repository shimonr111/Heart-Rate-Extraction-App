import numpy as np
from scipy.signal import butter, lfilter, find_peaks


def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band', analog=False)
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff_frequency, sampling_frequency, order=4):
    nyquist = 0.5 * sampling_frequency
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff_frequency, sampling_frequency, order=4):
    b, a = butter_lowpass(cutoff_frequency, sampling_frequency, order=order)
    y = lfilter(b, a, data)
    return y

class ExtractHeartRate:
    def __init__(self, green_channel):
        self.green_channel = green_channel
        self.heart_rate = 0
        self.frequency = 0


    def low_pass_filter(self, raw_padded_list, list_size_without_padding):
        for i in range(1, list_size_without_padding - 2):
            window = raw_padded_list[(i-1):(i-1) + 3]
            average = sum(window) / 3.0
            raw_padded_list[i] = average
        raw_padded_list[0] = raw_padded_list[1]
        raw_padded_list[list_size_without_padding - 1] = raw_padded_list[list_size_without_padding - 2]

    def high_pass_filter(self,  raw_padded_list, list_size_without_padding):
        for i in range(0, list_size_without_padding - 11, 11):
            window = raw_padded_list[i:i + 11]
            average = sum(window) / 11.0
            for j in range(11):
                raw_padded_list[i+j] -= average

    def lp(self, data, window_base):
        y = np.zeros_like(data)
        window_size = 2 * window_base + 1
        for i in range(len(data) - window_size - 1):
            window = data[i:i + window_size]
            avg = np.mean(window)
            y[i + window_base] = avg
        # pad start
        for i in range(window_base):
            y[i] = y[window_base]
        # pad end
        for i in range(1, window_base + 1):
            y[-i] = y[len(data)-window_base-1]
        return y

    '''def calc_hr_process(self, list_green_channel_avg, sampling_rate, list_size_without_padding, bin_plotter):
        if self.green_channel is None:
            return 0, 0, "Face did not detected"

        print(list_green_channel_avg)
        new_list = list(list_green_channel_avg[:list_size_without_padding])
        lp_list = self.lp(new_list, 1)
        hp_list = self.lp(lp_list, 5)
        result_list = [low - high for low, high in zip(lp_list, hp_list)]
        #calculate a binary vector for values over 0 set 1 else 0 from padded_list in size list_size_without_padding
        binary_vector = self.create_binary_vector(result_list, list_size_without_padding)
        bin_plotter.update_bin_plot(binary_vector)
        #find location of shift from 0 to 1
        shift_vector_widths = self.find_shift_widths(binary_vector)
        # Sorting the shift_widths in ascending order
        sorted_shift_widths = sorted(shift_vector_widths)
        # Filter the values in the range [5, 9]
        filtered_shift_widths = [width for width in sorted_shift_widths if 5 <= width <= 9]
        trimmed_data = self.trim_list(filtered_shift_widths, 0.4)
        # Calculate the mean of trimmed_data using numpy
        mean_value = np.mean(trimmed_data)
        self.heart_rate = 600 / mean_value
        return round(self.heart_rate), 1.0, None'''

    '''
    def calc_hr_process(self, padded_list, sampling_rate, list_size_without_padding, bin_plotter, counter):
        if self.green_channel is None:
            return 0, 0, "Face did not detected"

        # take interval of new values only
        new_list = list(padded_list[counter - 300:counter])
        values_greater_than_zero = [value for value in new_list if value > 0]
        clean_image_vector = self.clean_sd(values_greater_than_zero)
        # Apply the bandpass filter
        
        clean_image_vector_after_lp = self.lp(clean_image_vector, 1)
        clean_image_vector_after_hp = self.lp(clean_image_vector, 5)
        clean_image_vector_after_bp = [low - high for low, high in
                                       zip(clean_image_vector_after_lp, clean_image_vector_after_hp)]
        
        bin_plotter.update_bin_plot(clean_image_vector)
        # Find peaks in the signal
        peaks, _ = find_peaks(clean_image_vector)
        # Count the number of peaks
        num_peaks = len(peaks)
        self.frequency = 1
        self.heart_rate = 1800 / (len(clean_image_vector) / num_peaks)
        return self.heart_rate, self.frequency, None
        '''

    def calc_hr_process(self, padded_list, sampling_rate, list_size_without_padding, bin_plotter, counter):
        if self.green_channel is None:
            return 0, 0, "Face did not detected"

        # take interval of new values only
        new_list = list(padded_list[counter - 600:counter])

        # Calculate the average
        average_value = sum(new_list) / len(new_list)

        # Subtract average_value from each element in new_list using a loop
        for i in range(len(new_list)):
            new_list[i] -= average_value

        print(new_list)

        fourier = np.fft.fft(new_list)
        fourier_abs_values = np.absolute(fourier)
        bin_plotter.update_bin_plot(fourier_abs_values)
        length_of_padded_list = 600

        start_max_value = float('-inf')
        start_max_index = -1
        start_range = self.calculate_start_range(sampling_rate, length_of_padded_list)
        end_range = self.calculate_end_range(sampling_rate, length_of_padded_list)
        # Loop through the first half of the array to find max index of the max value
        for i in range(start_range, end_range):
            current_value = fourier_abs_values[i]
            # Update max_value and max_index if a greater value is found
            if current_value > start_max_value:
                start_max_value = current_value
                start_max_index = i
        self.frequency = (sampling_rate * start_max_index) / length_of_padded_list
        self.heart_rate = self.frequency * 60
        return self.heart_rate, self.frequency, None

    def max_filter(self, start_max_index, start_max_value, fourier_abs_values, list_size_without_padding):
        #take 50% of the value of start max value
        partial_max_value = start_max_value * 0.65
        # Find the index of the closest value to myval
        end_max_index = start_max_index
        #scan over the list of fourier abs values and find the last and calc the avg max index
        for i in range(start_max_index, round(list_size_without_padding/2)):
            current_value = fourier_abs_values[i]
            if current_value >= partial_max_value:
                end_max_index = i
        return round((end_max_index + start_max_index)/2)

    def calculate_start_range(self, sampling_rate, length_of_padded_list):
        freq = 60 / 60
        start_index = freq * length_of_padded_list / sampling_rate
        return round(start_index)

    def calculate_end_range(self, sampling_rate, length_of_padded_list):
        freq = 140 / 60
        end_index = freq * length_of_padded_list / sampling_rate
        return round(end_index)

    def create_binary_vector(self, padded_list, list_size_without_padding):
        # Ensure that the list is padded up to the desired size
        padded_list = padded_list[:list_size_without_padding]

        # Create a binary vector
        binary_vector = [1 if value > 0 else 0 for value in padded_list]

        return binary_vector

    def find_shift_widths(self, binary_vector):
        shift_widths = []
        current_width = 0

        for i in range(len(binary_vector)):
            if binary_vector[i] == 1:
                current_width += 1
            elif current_width > 0:
                shift_widths.append(current_width)
                current_width = 0

        return shift_widths

    def trim_list(self, input_list, percentage_to_remove):
        num_elements_to_remove = int(len(input_list) * percentage_to_remove)
        trimmed_list = input_list[num_elements_to_remove:-num_elements_to_remove]
        return trimmed_list

    def calculate_std_for_groups(self, padded_list, group_size):
        std_list = []

        # Iterate over the groups in the padded list
        for i in range(0, 300 - group_size + 1, group_size):
            group = padded_list[i:i + group_size]

            # Calculate the standard deviation for the current group
            group_std = np.std(group)

            # Save the standard deviation in the result list
            std_list.append(group_std)

        return std_list

    def clean_sd(self, x):
        k0 = 10  # block length
        k1 = len(x) // k0  # number of blocks
        k2 = np.zeros((k0, k1))

        for ik in range(k1):
            k2[:, ik] = x[ik * k0: (ik + 1) * k0]

        ky = k2.copy()
        k3 = np.mean(x)
        k2 = k2 - k3
        k2 = k2 ** 2
        k4 = np.sum(k2, axis=0)
        k5 = np.sort(k4)
        k6 = int(k1 * 0.9)
        k7 = k5[k6]
        k8 = np.where(k4 < k7)[0]
        k9 = ky[:, k8]
        y = k9.flatten()

        return y

    def remove_noise_and_pad(self, padded_list, std_list, group_size):
        # Determine the threshold for the worst 5% of std_list
        threshold_index = int(len(std_list) * 0.05)
        sorted_std_indices = np.argsort(std_list)
        noisy_indices = sorted_std_indices[-threshold_index:]

        # Create padded_list_without_noise with original values without noise
        padded_list_without_noise = list(padded_list)
        for i in range(300 - group_size + 1):
            # If the group index belongs to the noisy indices, fill with zeros
            if i // group_size in noisy_indices:
                padded_list_without_noise[i:i + group_size] = [0] * group_size

        return padded_list_without_noise

    def move_zeros_to_end(self, new_padded_list):
        non_zero_values = [value for value in new_padded_list if value > 0]
        zero_values = [value for value in new_padded_list if value == 0]

        # Create a new_padded_list with non-zero values followed by zero values
        updated_padded_list = non_zero_values + zero_values

        return updated_padded_list