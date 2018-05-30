import numpy as np
import matplotlib.pyplot as plt
import math

del_t = 0.001;

stdparams = {'v_reset' : -65.,
             'v_thresh': -50.,
             'E_L'     : -65.,
             'tau'     :  25.,
             'R_m'     :  10.}

def intfire(I_in, dt, IFparams = stdparams):
    V = np.zeros(len(curr)+1);
    V[0] = IFparams['v_reset'];
    reset = 0;

    for i in range(len(curr)):
        if reset == 1:
            V[i+1] = IFparams['v_reset'];
            reset = 0;
        elif V[i] >= IFparams['v_thresh']:
            V[i+1] = 0;
            reset = 1;
        else:
            dV = (IFparams['E_L']-V[i]+IFparams['R_m']*curr[i])/IFparams['tau'];
            V[i+1] = V[i]+dV*dt;

    return V

totaltime = 200;

curr = np.zeros(int(totaltime/del_t));
curr[int(20/del_t):int(50/del_t)] = 1000;

V = intfire(curr,del_t);
time = np.arange(len(V))*del_t;

plt.plot(time,V)
plt.show()
