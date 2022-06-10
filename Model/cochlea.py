from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import copy

from Model.IHC import IHC
import Model.basilarmembrane as basilarmembrane
import Model.AN as AN
import Model.tools as tools

class cochlea:
    def __init__(self, audio=None, fs=None):
        if audio is not None:
            set_input(audio, fs)
    
    ######################################################################
    ###################################################################### 
    # Input setting functions
    def set_input(self, audio, fs):
        self.fs = fs
        self.signal_input = audio
        
    ######################################################################
    ###################################################################### 
    # Stage 1 - Basilar Membrane            
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
    
    def visualise_filterbank(self):
        for band in self.bm['bands'].values():
            w, h = band['filter'].visualise()

            plt.plot(w, tools.amp2db(h))

        #plt.xscale('log')
        plt.title('{} filter frequency response'.format(self.filter_type))
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude [dB]')
        plt.margins(0, 0.1)
        #plt.axvline(ffilt, color='xkcd:pale grey') # cutoff frequency
        #plt.xlim(0, 22000)
        plt.grid(which='both', axis='both')
        
    def plot_bm(self, ax):
        signal_bands = self.get_signals_bm()
        signal_min = min(min(sig) for sig in signal_bands.values())
        signal_max = max(max(sig) for sig in signal_bands.values())

        signal_stacked = {freq: i+tools.rescale(band, (-0.45, 0.45), (signal_min, signal_max)) 
                             for i, (freq, band) 
                             in enumerate(signal_bands.items())}
        
        ax = self.plot_signals(signal_stacked, ax)
        ax.set_ylabel('Band Frequency (Post BM filtering)')
        

        return ax
    
    ######################################################################
    ######################################################################    
    # Stage 2 - Basilar Membrane
    def set_ihc(self):
        ihc = IHC()
        self.ihc = {"filter": ihc} 
        
    def filter_ihc(self):
        self.ihc['bands'] = dict()
        for f, band in self.bm['bands'].items():
            signal_bm = copy.deepcopy(band['signal_bm'])
            signal_filt = self.ihc['filter'].filter(signal_bm)
            self.ihc['bands'][f] = signal_filt
            
    def get_signals_ihc(self):
        signals = dict()
        for f, band in self.ihc['bands'].items():
            signals[f] = band
        return signals

    def plot_ihc(self, ax):
        signal_bands = self.get_signals_ihc()
        signal_min = min(min(sig) for sig in signal_bands.values())
        signal_max = max(max(sig) for sig in signal_bands.values())

        signal_stacked = {freq: i+tools.rescale(band, (0, 0.45), (signal_min, signal_max)) 
                             for i, (freq, band) 
                             in enumerate(signal_bands.items())}
        
        ax = self.plot_signals(signal_stacked, ax)
        ax.set_ylabel('Band Frequency (Post IHC filtering)')
        return ax
    
    ######################################################################
    ######################################################################    
    # Stage 3 - Auditory Neuron
    def set_an(self, neuron_type="meddis1986", num_neurons=10):
        self.an = dict()
        self.an['type'] = neuron_type
        if neuron_type == "meddis1986":
            self.an['bands'] = {str(f): {"neurons": AN.Meddis1986(num_neurons, self.fs)} for f in self.ihc['bands'].keys()}
    
    def filter_an(self):
        for f, signal in self.get_signals_ihc().items():
            signal_ihc = copy.deepcopy(signal)
            self.an['bands'][f]['neurons'].simulate(signal)
            
    def plot_raster(self, ax, padding=10):
        rasters = []
        yticks = []
        yticklabels = []
        for f, band in self.an['bands'].items():
            neurons = band['neurons']
            yticks.append(len(rasters) * (neurons.num_neurons + padding))
            yticklabels.append(f)
            rasters.append(neurons.raster(padding))
            
        rasters = [item for sublist in rasters for item in sublist]
            
        ax.eventplot(rasters, colors='k')
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        return ax
    
    def get_psth(self, binwidth=0.1):
        #nbands = len(self.an['bands'])
        psths = dict()
        psth_locs = []
        
        for f, band in self.an['bands'].items():
            neurons = band['neurons']
            psths[f], psth_loc = neurons.psth()
        return psths, psth_loc
            
        
            
        
    
    
        
    
    ######################################################################
    ######################################################################    
    # General Functions
    def plot_signals(self, signal_stacked, ax):
        yticks = np.arange(0, self.nfilt, 1, dtype=int)
        yticklabels = [int(float(f)) for f in signal_stacked.keys()]

        for freq, signal in signal_stacked.items():
            ax.plot(signal, color='k')
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xlabel('Sample n')
        return ax
        
    
