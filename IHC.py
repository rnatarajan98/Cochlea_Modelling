from scipy import signal
import tools
import numpy as np

class IHC:
    def __init__(self):
        self.processes = []
    
    def add_halfwave(self):
        halfwave = HalfwaveRectification()
        self.processes.append(halfwave)
        
    def add_lowpass(self, fs, N=1, cutoff=1000):
        lowpass = Lowpass(fs, N, cutoff)
        self.processes.append(lowpass)
        
    def add_hilbert(self):
        hilbert = Hilbert()
        self.processes.append(hilbert)
        
    def add_bernstein1999(self, fs, N=2, cutoff=425):
        bernstein1999 = Bernstein1999(fs, N, cutoff)
        self.processes.append(bernstein1999)
        
    def filter(self, signal):
        for process in self.processes:
            signal = process.filter(signal)
        return signal
        
        

class HalfwaveRectification:
    def filter(self, signal_input):
        signal_input[signal_input<0] = 0
        return signal_input

class Lowpass:
    def __init__(self, fs, N, cutoff):
        self.fs = fs
        self.N = N
        self.cutoff = cutoff
        nyq = fs / 2
        cutoff_normalised = cutoff/nyq
        self.b, self.a = signal.butter(N, cutoff_normalised, btype='low', analog=False)
        
    def filter(self, signal_input):
        signal_out = signal.lfilter(self.b, self.a, signal_input)
        return signal_out
    
    def visualise(self, ax):
        w, h = signal.freqz(self.b, self.a, fs=self.fs)
        ax.plot(w, tools.f2db(h))
        plt.title('IHC Lowpass filter frequency response, cutoff = {}'.format(self.cutoff))
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude [dB]')
        plt.margins(0, 0.1)
        #plt.axvline(ffilt, color='xkcd:pale grey') # cutoff frequency
        #plt.xlim(0, 22000)
        plt.grid(which='both', axis='both')
        
class Hilbert:    
    def filter(self, signal_input):
        signal_output = np.abs(signal.hilbert(signal_input))
        return signal_output
    
class Bernstein1999:
    def __init__(self, fs, N, cutoff):     
        #Hilbert
        self.hilbert = Hilbert()
        
        #Lowpass
        self.fs = fs
        self.N = N
        self.cutoff = cutoff
        nyq = fs / 2
        cutoff_normalised = cutoff/nyq
        self.b, self.a = signal.butter(N, cutoff_normalised, btype='low', analog=False)
    
    def filter(self, signal_input):
        signal_output = np.power((np.power(self.hilbert.filter(signal_input), -0.77) * signal_input), 2)
        return signal_output
        
        
        
    
        
        
