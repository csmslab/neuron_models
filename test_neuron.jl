using neuron
using Plots

testParams = HHparams(120, 36, 0.3, 50, -77, -54.4, -65, 1)
testIzhiParams = IzhiParams(0.2,0.02,-65,2)
num_neurons = 500
testNeurons = HHneurons(num_neurons, testParams)
testIzhis = IzhiNeurons(num_neurons, testIzhiParams)
t_total = 200
dt = 0.01
steps_total = convert(Int64,t_total/dt)
curr = zeros(steps_total,num_neurons)

for i in 1:num_neurons
    curr[convert(Int64,2/dt):convert(Int64,(140/dt)),i] = i*10;
end

vMem = zeros(steps_total,num_neurons)
vMemIzhi = zeros(steps_total,num_neurons)
spikes = zeros(steps_total,num_neurons)
spikesIzhi = zeros(steps_total,num_neurons)

for i in 1:steps_total
    vMem[i,:], spikeInds = update!(testNeurons, curr[i,:], dt)
    spikes[i, spikeInds] = 1
    
    vMemIzhi[i,:], spikeIndsIzhi = update!(testIzhis, curr[i,:], dt)
    spikesIzhi[i,spikeIndsIzhi] = 1
end
