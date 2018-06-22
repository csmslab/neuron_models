using neuron
using Plots

num_neurons = 10
t_total = 10
dt = 0.001
steps_total = convert(Int64,t_total/dt)
curr = zeros(steps_total,num_neurons)
El = -0.07
θinf = -0.05
k = [200., 20.]
C = 1.
G = 50.
a = 0.
b = 10.
R = [0., 1.]
A = [0., 0.]
Vr = -0.07
θr = -0.06
testParams = MNparams(El, θinf, k, C, G, a, b, R, A, Vr, θr)
testNeurons = MNneurons(num_neurons, testParams)


for i in 1:num_neurons
    curr[convert(Int64,2/dt):convert(Int64,(6/dt)),i] = 1 + i*5e-6;
end

V = zeros(steps_total, num_neurons)
θ = zeros(steps_total, num_neurons)
spikes = zeros(steps_total, num_neurons)

for i in 1:steps_total
    V[i,:], θ[i,:], spikeInds = update!(testNeurons, curr[i,:], dt)
    spikes[i, spikeInds] = 1
end

#TODO fix the scattering thing
plot(V)
plot!(θ)
scatter!(spikes[2:end,:].*V[1:end-1,:])
plot!(xlim=(2000,6000))
