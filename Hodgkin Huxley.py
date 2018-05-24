
# coding: utf-8

# In[149]:


import numpy as np
import matplotlib.pyplot as plt
import math

init_volt = -65;

gNa = 120;
gK = 36;
gL = 0.3;
VNa = 50;
VK = -77;
VL = -54.4;
C = 1;

del_t = 0.01;

# input current array
# output voltage
# compute n m h v


# In[150]:


#gating variable equations
def alphan(val):
    return 0.01*(val+55)/(1-math.exp(-1*(val+55)/10))

def alpham(val):
    return 0.1*(val+40)/(1-math.exp(-1*(val+40)/10))

def alphah(val):
    return 0.07*math.exp(-1*(val+65)/20)

def betan(val):
    return 0.125*math.exp(-1*(val+65)/80)

def betam(val):
    return 4*math.exp(-1*(val+65)/18)

def betah(val):
    return 1/(1+math.exp(-1*(val+35)/10))


# In[151]:


# input time
# np.ones_like initialize
def hodgehux(curr,dt):
    V = np.ones(len(curr)+1);
    n = np.zeros(len(curr)+1);
    m = np.zeros(len(curr)+1);
    h = np.zeros(len(curr)+1);
    V[0] = init_volt;
    n[0] = alphan(V[0])/(alphan(V[0])+betan(V[0]));
    m[0] = alpham(V[0])/(alpham(V[0])+betam(V[0]));
    h[0] = alphah(V[0])/(alphah(V[0])+betah(V[0]));
    # what are the initial values of n, m, h

    for i in range(len(curr)):
        dV = (curr[i]-gNa*(m[i]**3)*h[i]*(V[i]-VNa)-gK*(n[i]**4)*(V[i]-VK)-gL*(V[i]-VL))/C;
        V[i+1] = V[i]+dV*dt;

        dn = alphan(V[i])*(1-n[i])-betan(V[i])*n[i];
        n[i+1] = n[i]+dn*dt;

        dm = alpham(V[i])*(1-m[i])-betam(V[i])*m[i];
        m[i+1] = m[i]+dm*dt;

        dh = alphah(V[i])*(1-h[i])-betah(V[i])*h[i];
        h[i+1] = h[i]+dh*dt;

    return V,n,m,h

# what is t in the euler equation
# is voltage array 1 larger than current array?
# what is n in the n,m,h equations?
# plot
# shape input.shape


# In[161]:


# plot current vs time
# plot voltage vs time
# plot gating variables vs time
# multiplot

totaltime = 200;
curr = np.zeros(int(totaltime/del_t));
curr[int(20/del_t):int(20.1/del_t)] = 100;

# pulse current, steady current 0.001
V,n,m,h = hodgehux(curr,del_t);
time = np.arange(len(V))*del_t;

#time = np.arange(0,np.size(),dt);
plt.plot(time,V)
plt.show()
#plt.plot(time,currin,time,V)


# In[157]:

plt.plot(time,n,time,m,time,h)
plt.show()
