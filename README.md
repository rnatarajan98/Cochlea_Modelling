# Cochlea_Modelling
A Python based model of the cochlea, created as part of a PhD application
for the Lesica Lab



The model is split into three stages, each architecturally structured and
parametrized in order to match observations of the auditory system.

Note that the model is built in an object oriented way, so as to allow
precise alterations of the configuration. Currently, due to time constraints
only 1 implementation is provided for stages 1 and 3, though the stage 2 
currently allows for alternate models to be implemented and compared. In 
future, further models would be implemented for all stages.

#######################
STAGE 0 - Preprocessing

Audio files are imported from a wave file, and initially normalised between
-1 and. Further processing is applied to match a particular dB reference, 
depending on the particular model configuration. This is important noting 
that several implementations may be nonlinear.


#######################
STAGE 2 - The basilar membrane

The first stage is the basilar membrane stage, which here is modelled as 
a bank of linear gammatone filters. While other, more functionally 
accurate nonlinear filterbanks exist, such as the Dual resonance non-linear
filterbank, time constraints did not permit implementation of these models.

This filterbank effectively performs a discrete frequency decomposition into
various bands, ranging from 20Hz to 20kHz to reflect human hearing range.
Each band is fed into a different population of stage 2 and 3 models.

As it stands, the linearity of the gammatone filterbank allows for the usage
of nonlinear models in the later stages, which may otherwise require difference
dB referencing.

#######################
STAGE 2 - The inner hair cell

The inner hair cell is known to phase lock to lower frequencies, but not 
to higher frequencies. This can be modelled in several ways, some of which
are implemented in this model.

The two main implementations are:
1.  Halfwave rectification of the basilar membrane output followed by lowpass
    filtering of 1st order at 1000Hz
2.  As in Bernstein1999, the hilbert filter is used to extract the envelope of 
    the basilar signal, which is given a compressive nonlinearity by raising
    the power of the resulting waveform by 0.23, before combining with the 
    original fine structure. The resulting signal is then given an expansion
    stage by squaring the signal, followed by a 1st order lowpass filtering
    at 425Hz.
        A computational trick is applied as per the Bernstein paper, in which
        instead of computing the fine structure, the hilbert filtered signal
        is given an exponent of -0.77 before being multiplied by the original
        signal.


#######################
STAGE 3 - The Auditory Nerve

Here, stochastic firing of the auditory nerve is calculated as per Meddis 1999,
in which the population of neurotransmitters is calculated both in the cell
and the nerve cleft. Signal at the hair cell (stage 2) corresponds to increased
cell permeability, which causes flow of transmitter from the cell into the cleft,
which in the absence of sound is replenished. Probability of firing is calculated
as a function of cleft transmitter amount.

In this way, cell firing rate at rest is approximately 50 per second, and when
excited, rests at 150 per second. This is demonstrated in main.ipynb.

Spike trains and raster plots are both provided as visualisations of the autitory
nerve activity.




#######################
Two audio files are provided for analysis of the model, one consisting of two 
puretone sinusoids at a 200Hz and 2000Hz, aiming to reveal behaviour at 
low and high frequencies. The other audio file contains a fullband jazz song 
(Take 5 - Dave Brubeck). This file details response of the model to real world
audio information.



Several implemenetation of the model are provided, detailing the response of 
the model under different configurations to the two audio files. main.ipynb
contains the most insightful and effective modelling - bernstein1999 IHC 
responding to the two sinusoids.