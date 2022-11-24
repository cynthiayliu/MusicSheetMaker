import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

HALF_CHROMATIC_STEP = pow(1.0593843639335332, 0.5)

class AudioFileInput:
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (9, 7)

    sampFreq, sound = wavfile.read('Note Tester.wav')
    print(sound.dtype, sampFreq)
    sound = sound / 2.0 ** 15
    print(sound.shape)
    length_in_s = sound.shape[0] / sampFreq
    print(length_in_s)
    time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s
    print(time)

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

    signal = sound[:, 0]
    fft_spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1. / sampFreq)
    fft_spectrum_abs = np.abs(fft_spectrum)

    max_value = np.max(fft_spectrum_abs)

    amplitude_threshold = max_value * 0.5
    indices_over_threshold = (fft_spectrum_abs > amplitude_threshold)

    num_freq = indices_over_threshold.sum()
    freq_over_threshold = freq[indices_over_threshold].tolist()

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
    print(pitch_key_to_freq)

    pitches_present = set()
    for detected_freq in freq_over_threshold:
        for pitch_name in pitch_key_to_freq.keys():
            pitch_freq = pitch_key_to_freq[pitch_name]

            if pitch_freq / HALF_CHROMATIC_STEP < detected_freq < pitch_freq * HALF_CHROMATIC_STEP:
                pitches_present.add(pitch_name)

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

    print(freq)
    print(fft_spectrum_abs)

    plt.plot(freq[:5000], fft_spectrum_abs[:5000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.show()



