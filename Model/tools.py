import numpy as np

# Rescale a vector to a new defined maxima and minima
# Can omit tolower and toupper to simple normalise between 0 and 1
def rescale(signal, tolimits=(0, 1), fromlimits=None):
    tolower, toupper = tolimits
    if fromlimits is None:
        fromlower = min(signal)
        fromupper = max(signal)
    else:
        fromlower = fromlimits[0]
        fromupper = fromlimits[1]
    signal_norm = (signal - fromlower) / (fromupper - fromlower)
    signal_rescale = tolower + signal_norm * (toupper - tolower)
    return signal_rescale

def rescale_wav(signal, tolower=0, toupper=1):
    signal_norm = (signal - -32768) / (32767 - -32768)
    signal_rescale = tolower + signal_norm * (toupper - tolower)
    return signal_rescale


def amp2db(sig, reference=1):
    db = 20*np.log10(np.maximum(np.abs(sig), 1e-5)/reference)
    return db

def dbgain(signal, gain):
    x = np.power(10, gain)
    signal_amp = np.multiply(signal, np.power(10, gain/20))
    return signal_amp


