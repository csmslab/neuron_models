
# coding: utf-8

# In[124]:


import numpy as np
import matplotlib.pyplot as plt
import math

volt_reset = -65;
volt_threshold = -50;
EL = -65;
tao = 25;
Rm = 10;

del_t = 0.001;


# In[125]:


def intfire(curr,dt):
    V = np.zeros(len(curr)+1);
    V[0] = volt_reset;
    reset = 0;

    for i in range(len(curr)):
        if reset == 1:
            V[i+1] = volt_reset;
            reset = 0;
        elif V[i] >= volt_threshold:
            V[i+1] = 0;
            reset = 1;
        else:
            dV = (EL-V[i]+Rm*curr[i])/tao;
            V[i+1] = V[i]+dV*dt;

    return V


# In[128]:


totaltime = 200;

curr = np.zeros(int(totaltime/del_t));
curr[int(20/del_t):int(20.1/del_t)] = 1000;

V = intfire(curr,del_t);
time = np.arange(len(V))*del_t;

plt.plot(time,V)
plt.show()
