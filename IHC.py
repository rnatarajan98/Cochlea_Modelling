from scipy import signal

def halfwave_rectification(signal_input):
    signal_input[signal_input<0] = 0
    return signal_input

def lowpass(signal_input, fs, N=1, Wn=1000):
    nyq = fs / 2
    cutoff_normalised = Wn/nyq
    b, a = signal.butter(N, cutoff_normalised, btype='low', analog=False)
    signal_out = signal.lfilter(b, a, signal_input)
    return signal_out
    
   