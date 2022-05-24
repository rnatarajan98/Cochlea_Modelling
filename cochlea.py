from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import IHC
import basilarmembrane
import copy

class cochlea:
    def __init__(self, audio=None, fs=None):
        if audio is not None:
            set_input(audio, fs)
    
    def set_input(self, audio, fs):
        self.fs = fs
        self.signal_input = audio
                
    def set_BM(self, filter_type, flims, nfilt):
        self.bm = dict()
        if filter_type == "gammatone":
            self.bm['type'] = "gammatone"
            filt_locs = basilarmembrane.gammatone_freqs(flims, nfilt)
            self.bm['bands'] = {str(f): {"filter":basilarmembrane.gammatone(f, self.fs)} for f in filt_locs}        
        
    def filter_bm(self):
        for band in self.bm['bands'].values():
            filt = band['filter']
            sig_filt = filt.filter(self.signal_input)
            band['signal_bm'] = sig_filt
    
    def filter_ihc(self):
        self.ihc = dict()
        signal_ihc = []
        for f, band in self.bm['bands'].items():
            signal_bm = copy.deepcopy(band['signal_bm'])
            signal_halfwave = IHC.halfwave_rectification(signal_bm)
            #signal_halfwave = signal_bm
            signal_lowpass = IHC.lowpass(signal_halfwave, self.fs, 1, 1000)
            self.ihc[f] = signal_lowpass
            signal_ihc.append(signal_lowpass)
        return signal_ihc
    
    def visualise_filters(self):
        for band in self.bm['bands'].values():
            b, a = band['filter'].b, band['filter'].a
            w, h = signal.freqz(b, a, fs=self.fs)

            plt.plot(w, 20 * np.log10(abs(h)))

        #plt.xscale('log')
        plt.title('Gammatone filter frequency response')
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude [dB]')
        plt.margins(0, 0.1)
        #plt.axvline(ffilt, color='xkcd:pale grey') # cutoff frequency
        plt.xlim(0, 7000)
        plt.grid(which='both', axis='both')