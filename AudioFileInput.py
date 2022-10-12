import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import dtype
from scipy.io import wavfile


class AudioFileInput:
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (9, 7)

    sampFreq, sound = wavfile.read('MoonlightSonataExcerpt.wav')
    print(sound.dtype, sampFreq)
    sound = sound / 2.0 ** 15
    print(sound.shape)
    length_in_s = sound.shape[0] / sampFreq
    print(length_in_s)
    time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

    plt.plot(time[6000:7000], sound[6000:7000])
    plt.xlabel("time, s")
    plt.ylabel("signal, relative units")
    plt.show()

    fft_spectrum = np.fft.rfft(sound)
    freq = np.fft.rfftfreq(sound.size, d=1. / sampFreq)
    fft_spectrum_abs = np.abs(fft_spectrum)
    plt.plot(freq, fft_spectrum_abs)
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.show()

    plt.plot(freq[:3000], fft_spectrum_abs[:3000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.show()



