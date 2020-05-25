#!/usr/bin/python

import numpy as np
from scipy.interpolate import interp1d

def oxy_b(dt, tau):
    inv_b = 1 + 2*(tau/dt)
    return 1/inv_b

def oxy_a(dt, tau):
    return 1 - 2*oxy_b(dt, tau)

def correct_response_time(t, DO, tau):

    # array for the loop
    N = DO.shape[0]
    mean_oxy  = np.array((N-1)*[np.nan])
    mean_time = np.array((N-1)*[np.nan])

    # convert time to seconds
    t_sec = t*24*60*60

    # loop through oxygen data
    for i in range(N-1):
        dt = t_sec[i+1] - t_sec[i]

        # do the correction using the mean filter, get the mean time
        mean_oxy[i]  = (1/(2*oxy_b(dt, tau)))*(DO[i+1] - oxy_a(dt, tau)*DO[i])
        mean_time[i] = t_sec[i] + dt/2
    
    # interpolate back to original times for output
    f = interp1d(mean_time, mean_oxy, kind='linear', bounds_error=False, fill_falue='extrapolate')
    DO_out = f(t_sec)

    return DO_out