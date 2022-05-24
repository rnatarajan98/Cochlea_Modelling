from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import IHC

class filterbank:
    def __init__(self, filter_type, flims, nfilt, fs):
            self.fs = fs
            self.nfilt = nfilt
            self.flims = flims
            
            if filter_type == "gammatone":
                self.type = "gammatone"
                filt_locs = gammatone_freqs(self.flims, self.nfilt)
                self.bands = {str(f): {"filter":gammatone(f, fs)} for f in filt_locs}
                
    def visualise_filters(self):
        for band in self.bands.values():
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
        
    def filter_bm(self, input):
        self.signal_input = input
        for band in self.bands.values():
            filt = band['filter']
            sig_filt = filt.filter(input)
            band['signal_bm'] = sig_filt
    
    def filter_ihc(self):
        signal_ihc = []
        for band in self.bands.values():
            signal_halfwave = IHC.halfwave_rectification(band['signal_bm'])
            band['signal_IHC'] = signal_halfwave
            print(signal_halfwave)
            signal_lowpass = IHC.lowpass(signal_halfwave, self.fs, 1, 1000)
            print(signal_lowpass)
            print("")
            signal_ihc.append(signal_lowpass)
        return signal_ihc
        

class gammatone:
    def __init__(self, f_center, fs):
        #Models a 4th order gammatone filter with an 8th order IIR
        #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.gammatone.html#rf19e61802808-1
        self.center = f_center
        self.fs = fs
        self.b, self.a = signal.gammatone(f_center, ftype='iir', fs=fs)
        
    def filter(self, input):
        sig_filt = signal.lfilter(self.b, self.a, input)
        return sig_filt
        

#Glasberg and Moore, 1990)
def f2erb(f):
    erb = 11.17268 * np.log(1 + (46.06538 * f)/(f + 14678.40))
    return erb

def erb2f(erb):
    f = 676170.4/(47.06538 - np.exp(0.08950404*erb)) - 14678.49
    return f

def gammatone_freqs(flims, nfilt):
    erblims = [f2erb(flims[0]), f2erb(flims[1])]
    erbs = np.linspace(erblims[0], erblims[1], nfilt)
    filts = [erb2f(i) for i in erbs]
    return filts

