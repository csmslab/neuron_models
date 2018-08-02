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

currStart = round(Int64, 0.02/dt)
currStop = round(Int64, 0.5/dt)
for i in 1:num_neurons
    curr[currStart:currStop, i] = 1 + i*5e-6;
end

V = zeros(steps_total, num_neurons)
θ = zeros(steps_total, num_neurons)
spikes = spzeros(steps_total, num_neurons)

for i in 1:steps_total
    V[i,:], θ[i,:], spikeInds = update!(testNeurons, curr[i,:], dt)
    if ~isempty(spikeInds) && i != 1
        spikes[i, spikeInds] = V[i-1,spikeInds]
    end
end

spikeTimes, spikeNeurs, spikeVals = findnz(spikes)
plot(V)
plot!(θ)
scatter!(spikeTimes, spikeVals)
#plot!(xlim=(currStart, currStop))
