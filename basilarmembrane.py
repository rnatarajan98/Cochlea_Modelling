from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import IHC
        

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

