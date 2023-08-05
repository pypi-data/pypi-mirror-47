#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np
from scipy.special import erfc

############ SIMPLE MATHEMATICAL FUNCTIONS ###########
def gaussian(x,amp,freq,HWHM): # for spectral fit
    """compute a Gaussian peak

    Inputs
    ------
    x : ndarray
        the positions at which the signal should be sampled
    amp : float
        amplitude
    freq : float
        frequency/position of the Gaussian component
    HWHM : float
        half-width at half-maximum
    Returns
    -------
    out : ndarray
        the signal
    """
    return amp*np.exp(-np.log(2)*((x-freq)/HWHM)**2)

def gaussianarea(amp,HWHM,**options):
    """returns the area of a Gaussian peak 
    
    Inputs
    ------
    amp : float or ndarray
        amplitude of the peak
    HWHM : float or ndarray
        half-width at half-maximum
    
    Options 
    -------
    eseAmplitude : float or ndarray
        standard deviation on amp; Default = None
    eseHWHM : float or ndarray
        standard deviation on HWHM; Default = None

    Returns
    -------
    area : float or ndarray
        peak area
    esearea : float or ndarray
        error on peak area; will be None if no errors on amp and HWHM were provided.
    """
    area = np.sqrt(np.pi/np.log(2))*amp*HWHM
    if options.get("eseAmplitude") != None:
        eseAmplitude = options.get("eseAmplitude")
        if options.get("eseHWHM") != None:
            eseHWHM = options.get("eseHWHM")
            esearea = np.sqrt((np.pi/np.log(2)*HWHM)**2 * eseAmplitude**2 + (np.pi/np.log(2)*amp)**2 * eseHWHM**2)
    else:
        esearea = None

    return area, esearea

def lorentzian(x,amp,freq,HWHM):
    """compute a Lorentzian peak

    Inputs
    ------
    x : ndarray
        the positions at which the signal should be sampled
    amp : float
        amplitude
    freq : float
        frequency/position of the Gaussian component
    HWHM : float
        half-width at half-maximum

    Returns
    -------
    out : ndarray
        the signal
    """
    
    return amp/(1+((x-freq)/HWHM)**2)


def pseudovoigt(x,amp,freq,HWHM,LGratio):
    """compute a pseudo-Voigt peak

    Inputs
    ------
    x : ndarray
        the positions at which the signal should be sampled
    amp : float
        amplitude
    freq : float
        frequency/position of the Gaussian component
    HWHM : float
        half-width at half-maximum
    LGratio : float
        ratio pf the Lorentzian component, should be between 0 and 1 (included)
    Returns
    -------
    out : ndarray
        the signal
    """
    if (LGratio>1) or (LGratio<0):
        raise ValueError("LGratio should be comprised between 0 and 1")
    
    return LGratio*(amp/(1+((x-freq)/HWHM)**2)) + (1-LGratio)*(amp*np.exp(-np.log(2)*((x-freq)/HWHM)**2))

def pearson7(x,a0,a1,a2,a3):
    """compute a Peason7 peak

    Inputs
    ------
    x : ndarray
        the positions at which the signal should be sampled
    a0, a1, a2, a3 : float
        parameters of the Pearson7 equation
    
    Returns
    -------
    out : ndarray
        the signal

    Note
    ----
    equation is:
        out = a0 * (1/ ( (1 + ((x-a1)/a2))**2 * (2**(1/a3) -1))**a3
    """
    return a0 / ( (1.0 + ((x-a1)/a2)**2.0 * (2.0**(1.0/a3) -1.0))**a3 )

def funlog(x,a,b,c,d):
    return a*np.log(-b*(x-c))-d*x**2

def funexp(x,a,b,c):
    return a*np.exp(b*(x-c))

def poly2(x,a,b,c):
    return a + b*x + c*x*x

def linear(x,a,b):
    return a + b*x

def linear0(x,a):
    return a*x

def constant(x,a):
    return np.zeros(len(x))+a


########### SPECIFIC GAUSSIAN/VOIGTR FUNCTIONS FOR USING WITH SCIPY OPTIMIZATION PROTOCOLS

def multigaussian(x,params):
    taille = len(params)
    y = np.zeros(len(x),4)
    for i in range(taille):
        y[:,taille+1] = params[taille,0]*np.exp(-np.log(2)*((x-params[taille,1])/params[taille,2])**2)
    y[:,0] = y[:,1]+y[:,2]+y[:,3]
    return y


def gauss_lsq(params,x):
    nbpic = int(len(params)/3)
    a = np.zeros((1,nbpic))
    b = np.zeros((1,nbpic))
    c = np.zeros((1,nbpic))
    y = np.zeros((len(x),nbpic))
    for n in range(nbpic):
        m = 2*n # little trick for correct indexation
        a[0,n] = params[n+m]
        b[0,n] = params[n+m+1]
        c[0,n] = params[n+m+2]
        y[:,n] = a[0,n]*np.exp(-np.log(2)*((x[:]-b[0,n])/c[0,n])**2)
    ytot = sum(y,1)

    return ytot

def gauss_lsq_lfix(params,x):
    nbpic = int((len(params)-2)/2)
    a = np.zeros((1,nbpic))
    b = np.zeros((1,nbpic))
    c = np.zeros((1,2)) # FWMH fixed and in first position of params
    c[0,0] = params[0]
    c[0,1] = params[1]
    b[0,:] = params[2:(nbpic+2)]
    a[0,:] = params[nbpic+2:(2*nbpic+2)]
    y = np.zeros((len(x),nbpic))
    for n in range(nbpic):
        if n == 0:
            y[:,n] = a[0,n]*np.exp(-np.log(2)*((x[:]-b[0,n])/c[0,0])**2)
        else:
            y[:,n] = a[0,n]*np.exp(-np.log(2)*((x[:]-b[0,n])/c[0,1])**2)
    ytot = sum(y,1)

    return ytot

########### SPECIFIC FUNCTIONS FOR CHEMICAL DIFFUSION


def diffshort(x, t, C0, C1, D):
    """
    Simple equation for the diffusion into a semi-infinite slab, see Crank 1975
    C0 is the concentration in the core
    C1 is the concentration at the border
    D is the diffusion coefficient in log10 unit, m^2.s^-1
    x is the profil length in meters
    t is the time in seconds
    """

    Cx = (C1 - C0) * erfc(x / (2. * np.sqrt((10**D)*t))) + C0

    return Cx

def difffull(x1, x2, t, C0, C1, D):
    """
    Simple equation for the diffusion into a semi-infinite slab, see Crank 1975
    C0 is the concentration in the core
    C1 is the concentration at the border
    D is the diffusion coefficient in log10 unit, m^2.s^-1
    x1 and x2 are the profil lengths from beginning and end respectively, in meters
    t is the time in seconds
    """
    x = (x2-x1)
    Cx = (C1 - C0) * ( erfc(x / (2. * np.sqrt((10**D)*t))) +  erfc((x) / (2. * np.sqrt((10**D)*t))))+ C0

    return Cx
