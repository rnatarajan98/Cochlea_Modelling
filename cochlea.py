from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from IHC import IHC
import basilarmembrane
import copy
import tools

class cochlea:
    def __init__(self, audio=None, fs=None):
        if audio is not None:
            set_input(audio, fs)
    
    def set_input(self, audio, fs):
        self.fs = fs
        self.signal_input = audio
                
    def set_BM(self, filter_type, flims, nfilt):
        self.filter_type = filter_type
        self.nfilt = nfilt
        self.bm = dict()
        if filter_type == "gammatone":
            self.bm['type'] = filter_type
            filt_locs = basilarmembrane.gammatone_freqs(flims, nfilt)
            self.bm['bands'] = {str(f): {"filter":basilarmembrane.gammatone(f, self.fs)} for f in filt_locs}      
        if filter_type == "transp":
            self.bm['type'] = filter_type
            self.bm['bands'] = {"fullband": {"filter":basilarmembrane.transparent(self.fs)}}      
        
    def filter_bm(self):
        for band in self.bm['bands'].values():
            filt = band['filter']
            sig_filt = filt.filter(self.signal_input)
            band['signal_bm'] = sig_filt
            
    def get_signals_bm(self):
        signals = dict()
        for f, band in self.bm['bands'].items():
            signals[f] = band['signal_bm']
        return signals
            
    def get_signals_ihc(self):
        signals = dict()
        for f, band in self.ihc['bands'].items():
            signals[f] = band
        return signals
            
    def set_ihc(self):
        ihc = IHC()
        self.ihc = {"filter": ihc} 
        
    def filter_ihc(self):
        self.ihc['bands'] = dict()
        for f, band in self.bm['bands'].items():
            signal_bm = copy.deepcopy(band['signal_bm'])
            signal_filt = self.ihc['filter'].filter(signal_bm)
            self.ihc['bands'][f] = signal_filt

    
    def plot_bm(self, ax):
        signal_bands = self.get_signals_bm()
        ax = self.plot_signals(signal_bands, ax)
        ax.set_ylabel('Band Frequency (Post BM filtering)')

        return ax
        
    def plot_ihc(self, ax):
        signal_bands = self.get_signals_ihc()
        ax = self.plot_signals(signal_bands, ax)
        ax.set_ylabel('Band Frequency (Post IHC filtering)')
        return ax
    
    def plot_signals(self, signal_bands, ax):
        signal_min = min(min(sig) for sig in signal_bands.values())
        signal_max = max(max(sig) for sig in signal_bands.values())

        signal_stacked = {freq: i+tools.rescale(band, (-0.45, 0.45), (signal_min, signal_max)) 
                             for i, (freq, band) 
                             in enumerate(signal_bands.items())}
        yticks = np.arange(0, self.nfilt, 1, dtype=int)
        yticklabels = [int(float(f)) for f in signal_stacked.keys()]

        for freq, signal in signal_stacked.items():
            ax.plot(signal, color='k')
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xlabel('Sample n')
        return ax
        
    
    def visualise_filters(self):
        for band in self.bm['bands'].values():
            w, h = band['filter'].visualise()

            plt.plot(w, tools.f2db(h))

        #plt.xscale('log')
        plt.title('{} filter frequency response'.format(self.filter_type))
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude [dB]')
        plt.margins(0, 0.1)
        #plt.axvline(ffilt, color='xkcd:pale grey') # cutoff frequency
        #plt.xlim(0, 22000)
        plt.grid(which='both', axis='both')