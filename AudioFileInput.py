import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from numpy import dtype
from typing import ValuesView
import heapq
from scipy.io import wavfile
from sklearn.cluster import KMeans


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
    noteLength = time/3

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
    print("Count of values over threshold: ", indices_over_threshold.sum())
    print("Frequencies over threshold: ", freq[indices_over_threshold])

    # taken from a website https://pages.mtu.edu/~suits/notefreqs.html
    pitches = [["C2", 65.41], ["C#2/Db2", 69.30], ["D2", 73.42], ["D#2/Eb2", 77.78], ["E2", 82.41], ["F2", 87.31],
               ["F#2/Gb2", 92.5], ["G2", 98], ["G#2/Ab2", 103.83], ["A2", 110], ["A#2/Bb2", 116.54], ["B2", 123.47],
               ["C3", 130.81], ["C#3/Db3", 138.59], ["D3", 146.83], ["D#3/Eb3", 155.56], ["E3", 164.81], ["F3", 174.61],
               ["F#3/Gb3", 185], ["G3", 196], ["G#3/Ab3", 207.65], ["A3", 220], ["A#3/Bb3", 233.08], ["B3", 246.94],
               ["C4", 261.63], ["C#4/Db4", 277.18], ["D4", 293.66], ["D#4/Eb4", 311.13], ["E4", 329.63], ["F4", 349.23],
               ["F#4/Gb4", 369.99], ["G4", 392], ["G#4/Ab4", 415.3], ["A4", 440], ["A#4/Bb4", 466.16], ["B4", 493.88],
               ["C5", 523.25], ["C#5/Db5", 554.37], ["D5", 587.33], ["D#5/Eb5", 622.25], ["E5", 659.25], ["F5", 698.46],
               ["F#5/Gb5", 739.99], ["G5", 783.99], ["G#5/Ab5", 830.61], ["A5", 880], ["A#5/Bb5", 932.33],
               ["B5", 987.77], ["C6", 1046.60]]

    freq_diff = pitches - freq[indices_over_threshold]
    note_freq = ((pitches - freq_diff) < 2)
    print(pitches[note_freq])

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

    plt.plot(freq[:5000], fft_spectrum_abs[:5000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.show()



