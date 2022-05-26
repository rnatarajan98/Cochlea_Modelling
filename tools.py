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


def f2db(f):
    db = 20*np.log10(np.maximum(np.abs(f), 1e-5))
    return db

def db2f(db):
    f = 10&(db/20)
    return f