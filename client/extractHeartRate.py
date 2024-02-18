import numpy as np

data_list = [94.81338028169014, 94.68055555555556, 95.2855596449448, 94.56986464968153, 94.83954326923077, 94.48964968152866, 93.7489388794567, 94.51273885350318, 93.09166196122717, 94.31574675324676, 93.93739388794567, 94.03120387940122, 94.4052483974359, 94.6141826923077, 93.97180089724418, 93.5751201923077, 93.4853896103896, 93.25218949044586, 93.85227272727273, 93.81230095541402, 94.22014331210191, 95.02830188679245, 94.87159455128206, 94.78485576923077, 94.02157802964254, 93.55154965211891, 93.91935483870968, 93.95505376344086, 93.66477768090671, 93.89434942628274, 93.97435897435898, 93.51846349745331, 93.7947607707296, 93.28926146010187, 93.27101018675721, 93.3819008443386, 93.11608658743633, 93.30475382003395, 93.36290322580645, 93.25084889643463, 93.15644107105207, 93.54881154499151, 93.94252873563218, 93.60446009389672, 93.46658233185748, 93.76735632183907, 93.63011494252873, 93.57588652482269, 93.28472222222223, 93.67610269914417, 93.40787037037038, 93.85549258936356, 93.86988505747127, 94.12581168831169, 94.13115449915111, 95.00588491717524, 94.7699074074074, 95.11159546643418, 95.32777657501623, 95.10185185185185, 95.11094158674804, 95.30579773321709, 94.82151300236407, 94.64420803782505, 94.40023640661938, 94.58137931034483, 94.85185185185185, 94.74444444444444, 94.39606481481482, 94.78333333333333, 94.6274231678487, 94.75437486822686, 94.93034482758621, 94.87241379310345, 94.55281690140845, 94.86430260047281, 94.87494252873563, 94.8906103286385, 94.22538730634683, 94.54799054373522, 94.73724137931035, 94.48935185185185, 94.8719540229885, 94.57221389305347, 94.76077072959515, 94.52907123080796, 94.56275862068965, 94.5519740129935, 94.96137521222411, 94.98368794326241, 94.68990687138182, 95.20653821173414, 94.7080459770115, 94.63682247092386, 94.76212420452052, 94.74215198094825, 94.94954337899543, 94.94397163120567, 95.2194856146469, 94.98228503184713, 95.68, 95.51338028169015, 95.19638186573671, 95.10735632183908, 95.53064123376623, 95.14210985178727, 95.31495204882302, 95.17253820033956, 95.68526591107236, 95.403443766347, 95.55745308876239, 95.40961247023165, 95.04474885844749, 95.29247311827957, 94.87784946236559, 95.02789598108747, 95.20759271450515, 95.4494623655914, 95.20700704977568, 95.70353084415585, 94.9150234741784, 95.9863782051282, 94.6210401891253, 95.31956989247311, 95.08953258722843, 95.57701345866268, 94.87375886524822, 94.52121061771273, 94.79600938967135, 95.03748910200522, 95.53596338273758, 94.78493150684932, 94.96027397260274, 95.10884353741497, 95.11843971631205, 94.5406103286385, 94.50532454361054, 94.23295019157088, 94.66549295774648, 94.50183908045977, 94.37006496751624, 94.7027397260274, 94.6311844077961, 95.19834350479512, 94.65547945205479, 94.60422535211268, 94.97935483870968, 95.0894623655914, 95.03956989247312, 94.94850574712643, 95.0906103286385, 95.37283300416941, 95.31211279641103, 94.87283105022831, 95.13076423468283, 94.89434942628274, 94.62237442922374, 95.21290322580646, 94.81712328767124, 94.95224586288415, 94.97146118721462, 94.62022988505747, 94.71195402298851, 94.37777777777778, 94.82978723404256, 94.70182648401827, 94.91839350566119, 95.23922927040485, 95.02827586206897, 95.02332170880558, 94.59892473118279, 94.25824314120312, 94.86322580645161, 94.87551418055857, 94.82999128160418, 94.62229885057471, 94.94912318683697, 94.33195402298851, 94.3671264367816, 94.67633686945226, 95.56290064102564, 94.42062818336163, 94.48105650573717, 94.29793103448276, 94.28995433789954, 94.54121863799283, 94.23881278538813, 94.24529118856896, 94.30850833513747, 94.15957446808511, 94.13448275862069, 94.2680459770115, 94.14215053763441, 94.55698924731183, 94.74713141372591, 94.42402376910017, 94.56229707792208, 94.15698924731183, 94.20166631061738, 94.46989247311828, 94.62787265443812, 95.00573005093379, 95.19090544871794, 94.55462365591397, 94.62294381542405, 94.72035889767143, 95.48517628205128, 94.34977168949771, 94.68068965517242, 94.63287671232877, 95.52751423149905, 94.77124183006536, 94.75354838709677, 95.11236198311323, 94.90838709677419, 94.57885057471265, 94.86965517241379, 95.29876596665945, 95.33578696687594, 94.67488584474886, 94.99025763152197, 94.95352112676056, 94.8169848584595, 94.62054794520547, 94.36120543293718, 94.99632183908047, 94.16206896551724, 94.15957446808511, 94.33782505910166, 94.13440860215054, 94.28620689655172, 94.3303348325837, 94.58192488262911, 94.38215962441315, 94.58219178082192, 94.54367816091954, 94.16616691654173, 94.13133874239351, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


class ExtractHeartRate:
    def __init__(self, green_channel):
        self.green_channel = green_channel
        self.heart_rate = 0
        self.frequency = 0

    def low_pass_filter(self, raw_padded_list, list_size_without_padding):
        for i in range(list_size_without_padding - 2):
            window = raw_padded_list[i:i + 3]
            average = sum(window) / 3.0
            raw_padded_list[i] = average
        raw_padded_list[list_size_without_padding - 2] = 0
        raw_padded_list[list_size_without_padding - 1] = 0

    def high_pass_filter(self,  raw_padded_list, list_size_without_padding):
        for i in range(0, list_size_without_padding - 30, 30):
            window = raw_padded_list[i:i + 30]
            average = sum(window) / 30.0
            for j in range(30):
                raw_padded_list[i+j] -= average

    def calc_hr_process(self, padded_list, sampling_rate, list_size_without_padding, bin_plotter):
        if self.green_channel is None:
            return 0, 0, "Face did not detected"
        
        #run low pass filter
        self.low_pass_filter(padded_list, list_size_without_padding)
        #run high pass filter
        self.high_pass_filter(padded_list, list_size_without_padding)

        fourier = np.fft.fft(padded_list)
        fourier_abs_values = np.absolute(fourier)
        bin_plotter.update_bin_plot(fourier_abs_values)
        length_of_padded_list = len(padded_list)

        start_max_value = float('-inf')
        start_max_index = -1
        start_range = self.calculate_start_range(sampling_rate, length_of_padded_list)
        # Loop through the first half of the array to find max index of the max value
        for i in range(start_range, round(list_size_without_padding/2)):
            current_value = fourier_abs_values[i]
            # Update max_value and max_index if a greater value is found
            if current_value > start_max_value:
                start_max_value = current_value
                start_max_index = i

        max_index = self.max_filter(start_max_index, start_max_value, fourier_abs_values, list_size_without_padding)
        print(max_index)
        self.frequency = (sampling_rate * max_index) / length_of_padded_list
        self.heart_rate = 60 * self.frequency
        return self.heart_rate, self.frequency, None
        
    def max_filter(self, start_max_index ,start_max_value, fourier_abs_values, list_size_without_padding):
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
        freq = 45 / 60
        start_index = freq * length_of_padded_list / sampling_rate
        return round(start_index)
