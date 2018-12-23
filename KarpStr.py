import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio

class GuitarString:
    def __init__(self, pitch, starting_sample, sampling_freq, stretch_factor):
        self.pitch = pitch
        self.starting_sample = starting_sample
        self.sampling_freq = sampling_freq
        self.stretch_factor = stretch_factor
        self.init_wavetable()
        self.current_sample = 0
        self.previous_value = 0

    def init_wavetable(self):
        wavetable_size = self.sampling_freq // int(self.pitch)
        self.wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)

    def get_sample(self):
        if self.current_sample >= self.starting_sample:
            current_sample_mod = self.current_sample % self.wavetable.size
            r = np.random.binomial(1, 1 - 1/self.stretch_factor)
            if r == 0:
                self.wavetable[current_sample_mod] = 0.5 * (self.wavetable[current_sample_mod] + self.previous_value)
            sample = self.wavetable[current_sample_mod]
            self.previous_value = sample
            self.current_sample += 1
        else:
            self.current_sample += 1
            sample = 0
        return sample

fs = 44100

freqs = [98, 123, 147, 196, 294, 392, 392, 294, 196, 147, 123, 98]
unit_delay = fs//50
delays = [unit_delay * _ for _ in range(len(freqs))]
stretch_factors = [2 * f/98 for f in freqs]

strings = []
counter = 0
for freq, delay, stretch_factor in zip(freqs, delays, stretch_factors):
    counter += 1
    string = GuitarString(freq, delay if counter < 7 else delay + unit_delay*50, fs, stretch_factor)
    strings.append(string)

guitar_sound = [sum(string.get_sample() for string in strings) for _ in range(fs * 6)]

Audio(guitar_sound, rate=fs)
