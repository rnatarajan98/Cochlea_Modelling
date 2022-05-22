from scipy import signal
import numpy as np


#Glasberg and Moore, 1990)
def f2erb(f):
    erb = 0.108*f + 24.7
    return erb

def erb2f(erb):
    f = (erb - 24.7)/0.108 
    return f


def gammatone(f_center, fs):
    #Models a 4th order gammatone filter with an 8th order IIR
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.gammatone.html#rf19e61802808-1
    filter = signal.gammatone(f_center, ftype='iir', fs=fs)
    return filter

def gammatone_freqs(flims, nfilt):
    erblims = [f2erb(flims[0]), f2erb(flims[1])]
    erbs = np.linspace(erblims[0], erblims[1], nfilt)
    filts = [erb2f(i) for i in erbs]
    return filts
