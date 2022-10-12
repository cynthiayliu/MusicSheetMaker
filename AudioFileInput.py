import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import dtype
from scipy.io import wavfile


class AudioFileInput:
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (9, 7)

    sampFreq, sound = wavfile.read('piano_middle_C.wav')
    print(sound.dtype, sampFreq)
    sound = sound / 2.0 ** 15
    print(sound.shape)
    length_in_s = sound.shape[0] / sampFreq
    print(length_in_s)
    time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

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

    # plt.subplot(2, 1, 1)
    # plt.plot(time, sound, 'r')
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

    signal = sound
    # plt.plot(time[6000:7000], signal[6000:7000])
    # plt.xlabel("time, s")
    # plt.ylabel("signal, relative units")
    # plt.show()
    #
    fft_spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1. / sampFreq)
    fft_spectrum_abs = np.abs(fft_spectrum)

    # plt.plot(freq, fft_spectrum_abs)
    # plt.xlabel("frequency, Hz")
    # plt.ylabel("Amplitude, units")
    # plt.show()

    plt.plot(freq[:5000], fft_spectrum_abs[:5000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.show()



