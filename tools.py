# Rescale a vector to a new defined maxima and minima
# Can omit tolower and toupper to simple normalise between 0 and 1
def rescale(signal, tolower=0, toupper=1):
    print(min(signal), max(signal))
    signal_norm = (signal - min(signal)) / (max(signal) - min(signal))
    signal_rescale = tolower + signal_norm * (toupper - tolower)
    return signal_rescale