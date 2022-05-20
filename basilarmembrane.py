from scipy import signal


#Glasberg and Moore, 1990)
def ERB(f):
    erb = 0.108*f + 24.7
    return erb


def gammatone(f_center, fs):
    #Models a 4th order gammatone filter with an 8th order IIR
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.gammatone.html#rf19e61802808-1
    filter = signal.gammatone(f_center, ftype='iir', fs=fs)
    return filter