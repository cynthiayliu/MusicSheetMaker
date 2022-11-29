import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

HALF_CHROMATIC_STEP = pow(1.0593843639335332, 0.5) # square root of ratio between between neighboring chromatic steps
# to find the nearest note
NOTE_SAMPLING_INTERVAL = 0.05  # seconds


class AudioFileInput:
    def read_audio_file(self, filename):
        if ".wav" in filename:
            return wavfile.read(filename)
        else:
            raise NotImplementedError("Audio file format not supported!")

    def sample_audio_file_into_notes(self, filename):
        """

        :param filename:
        """
        # TODO extend code to accept more than wav files
        # use pydub library and ffmpeg to read mp3 and many other file types. Wav files can also be read without using
        # ffmpeg

        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['figure.figsize'] = (9, 7)

        sampling_rate, sound = self.read_audio_file(filename)
        sampling_interval = 1 / sampling_rate
        print(sound.dtype, sampling_rate, sampling_interval)
        sound = sound / 2.0 ** 15
        print(sound.shape)
        length_in_s = round(sound.shape[0] / float(sampling_rate), 2)
        print(length_in_s)

        badVariableName = 1
        print(badVariableName + 1)

        # plt.subplot(2, 1, 1)
        # plt.plot(time, sound[:, 0], 'r')
        # plt.xlabel("time, s [left channel]")
        # plt.ylabel("signal, relative units")
        # plt.subplot(2, 1, 2)
        # plt.plot(time, sound[:, 1], 'b')
        # plt.xlabel("time, s [right channel]")
        # plt.ylabel("signal, relative units")
        # plt.tight_layout()
        # plt.show()

        # signal = sound[:, 0]
        # plt.plot(time[6000:7000], signal[6000:7000])
        # plt.xlabel("time, s")
        # plt.ylabel("signal, relative units")
        # plt.show()

        left_channel = sound[:, 0]
        print("left_channel shape: ", left_channel.shape)
        # sampled_signal = signal[0:1000]
        # print("sampled_signal.shape: ", sampled_signal.shape)

        step_size = int(NOTE_SAMPLING_INTERVAL * sampling_rate)
        for sample_start in range(0, sound.shape[0], step_size):
            sample_end = sample_start + step_size

            notes = self.resolve_notes_from_sample(left_channel[sample_start:sample_end], sampling_rate, 4)
            print("sample interval: ", sample_start, sample_end, notes)

    def resolve_notes_from_sample(self, signal, sampling_rate, debug_level):
        """

        :param signal:
        :param sampling_rate:
        :param debug_level: Influences how much debug behavior is run. level <= 4 -> nothing, 5-9 -> prints notes, 10-14 prints extra, 15+ shows chart
        :return:
        """
        fft_spectrum = np.fft.rfft(signal)
        freq = np.fft.rfftfreq(signal.size, d=1. / sampling_rate)
        fft_spectrum_abs = np.abs(fft_spectrum)

        max_value = np.max(fft_spectrum_abs)

        amplitude_threshold = max_value * 0.75
        indices_over_threshold = (fft_spectrum_abs > amplitude_threshold)

        # num_freq = indices_over_threshold.sum()
        freq_over_threshold = freq[indices_over_threshold].tolist()

        if debug_level > 10:
            print("Count of values over threshold: ", indices_over_threshold.sum())
            print("Frequencies over threshold: ", freq_over_threshold)

        # taken from a website https://pages.mtu.edu/~suits/notefreqs.html
        pitches = {65.41: "C2", 69.3: "C#2/Db2", 73.42: "D2", 77.78: "D#2/Eb2", 82.41: "E2", 87.31: "F2",
                   92.5: "F#2/Gb2", 98: "G2", 103.83: "G#2/Ab2", 110: "A2", 116.54: "A#2/Bb2",
                   123.47: "B2", 130.81: "C3", 138.59: "C#3/Db3", 146.83: "D3", 155.56: "D#3/Eb3",
                   164.81: "E3", 174.61: "F3", 185: "F#3/Gb3", 196: "G3", 207.65: "G#3/Ab3", 220: "A3",
                   233.08: "A#3/Bb3", 246.94: "B3", 261.63: "C4", 277.18: "C#4/Db4", 293.66: "D4",
                   311.13: "D#4/Eb4", 329.63: "E4", 349.23: "F4", 369.99: "F#4/Gb4", 392: "G4",
                   415.3: "G#4/Ab4", 440: "A4", 466.16: "A#4/Bb4", 493.88: "B4", 523.25: "C5",
                   554.37: "C#5/Db5", 587.33: "D5", 622.25: "D#5/Eb5", 659.25: "E5", 698.46: "F5", 739.99: "F#5/Gb5",
                   783.99: "G5", 830.61: "G#5/Ab5", 880: "A5", 932.33: "A#5/Bb5", 987.77: "B5", 1046.6: "C6"}

        pitch_key_to_freq = {v: k for k, v in pitches.items()}
        # print(pitch_key_to_freq)

        pitches_present = set()
        for detected_freq in freq_over_threshold:
            for pitch_name in pitch_key_to_freq.keys():
                pitch_freq = pitch_key_to_freq[pitch_name]

                if pitch_freq / HALF_CHROMATIC_STEP < detected_freq < pitch_freq * HALF_CHROMATIC_STEP:
                    pitches_present.add(pitch_name)

        if debug_level > 5:
            print("Pitches in this timestep: ", pitches_present)

        # print("Amplitudes over threshold: ", fft_spectrum_abs[indices_over_threshold])

        # values_over_threshold[i] is 1 when fft_spectrum_abs[i] is > threshold, else 0

        # What you want to do:
        # 1. You can find which amplitude values + frequencies are greater than your threshold
        # 2. You're interested in finding local maxima for values above this threshold.
        #     a. You can use a clustering algorithm to resolve what pitches can be (search for: k-means)
        #     b. you can assume a certain amount of separation between pitches (assume chromatic tone system)
        #     c. This is overly complicated and ignore the fluffy Siberian cat pawing at your face

        # A -> 440 hz (approx.) margin -> 440 * (+/-2^(1/24))
        # 439, 441, 443 -> all these map to A -> A is your output

        # plt.plot(time[6000:7000], signal[6000:7000])
        # plt.xlabel("time, s")
        # plt.ylabel("signal, relative units")
        # plt.show()

        # plt.plot(freq, fft_spectrum_abs)
        # plt.xlabel("frequency, Hz")
        # plt.ylabel("Amplitude, units")
        # plt.show()

        if debug_level > 15:
            plt.plot(freq[:5000], fft_spectrum_abs[:5000])
            plt.xlabel("frequency, Hz")
            plt.ylabel("Amplitude, units")
            plt.show()

        return pitches_present


if __name__ == "__main__":
    AudioFileInput().sample_audio_file_into_notes('Tune2Piano.wav')
