module neuron

export HHparams, HHneurons, IzhiParams, IzhiNeurons, update!

abstract type Neurons end
abstract type NeuronParams end

α_n(v) = (0.01 * (v + 55))./(1-exp.(-(v+55)./10))
β_n(v) = 0.125 * exp.(-(v + 65)./80)
α_m(v) = (0.1 * (v + 40))./(1-exp.(-(v+40)./10))
β_m(v) = 4.0 * exp.(-(v + 65)./18)
α_h(v) = 0.07 * exp.(-(v + 65)./20)
β_h(v) = 1 ./ (1 + exp.(-(v + 35)./10))

channel_inf(α,β,v) = α(v)./(α(v) + β(v))
channel_update(x,α,β,v) = α(v).*(1 - x) - β(v).*x;

type HHparams <: NeuronParams
    gNa::Float64
    gK::Float64
    gL::Float64
    vNa::Float64
    vK::Float64
    vL::Float64
    vRst::Float64
    C::Float64

    HHparams(gNa,gK,gL,vNa,vK,vL,vRst,C) = new(gNa,gK,gL,vNa,vK,vL,vRst,C)
end

type HHneurons <: Neurons
    num_neur::Int64         # Number of Neurons in population
    params::HHparams        # Neuron parameters
    vMem::Array{Float64,1}  # Variables
    m::Array{Float64,1}
    n::Array{Float64,1}
    h::Array{Float64,1}
    lastSpike::Array{Float64,1}
    HHneurons(num_neur, params) = new(num_neur, params, params.vRst*ones(num_neur), channel_inf(α_m,β_m,params.vRst)*ones(num_neur), channel_inf(α_n,β_n,params.vRst)*ones(num_neur), channel_inf(α_h,β_h,params.vRst)*ones(num_neur), zeros(num_neur))
end

function update!(neurons::HHneurons, input, dt)
    # Calculate voltage update
    iNa = neurons.params.gNa * neurons.m .^ 3. .* neurons.h .* (neurons.vMem - neurons.params.vNa)
    iK = neurons.params.gK * neurons.n .^ 4. .* (neurons.vMem - neurons.params.vK)
    iL = neurons.params.gL * (neurons.vMem - neurons.params.vL)
    vMemNext = neurons.vMem + dt .* (input - iNa - iK - iL)./neurons.params.C

    # Find where spikes occur
    # TODO: currently, spikes defined by when vMem changes from neg to pos
    isspike(v,vNext) = (v .< 0) .& (vNext .> 0)
    spikeInd = find(isspike(neurons.vMem, vMemNext))
    neurons.lastSpike += dt
    neurons.lastSpike[spikeInd] = 0.

    # Update channel gating variables and membrane voltage
    neurons.m += dt .* channel_update(neurons.m, α_m, β_m, neurons.vMem)
    neurons.n += dt .* channel_update(neurons.n, α_n, β_n, neurons.vMem)
    neurons.h += dt .* channel_update(neurons.h, α_h, β_h, neurons.vMem)
    neurons.vMem = vMemNext

    return neurons.vMem, spikeInd
end

type IzhiParams <: NeuronParams
    a::Float64
    b::Float64
    c::Float64
    d::Float64
    IzhiParams(a,b,c,d) = new(a,b,c,d)
end

type IzhiNeurons <: Neurons
    num_neur::Int64         # Number of Neurons in population
    params::IzhiParams      # Neuron parameters
    v::Array{Float64,1}     # Variables
    u::Array{Float64,1}
    lastSpike::Array{Float64,1}
    IzhiNeurons(num_neur, params) = new(num_neur, params, params.c*ones(num_neur), zeros(num_neur), zeros(num_neur))
end

function update!(neurons::IzhiNeurons, input, dt)
    # Calculate voltage update
    neurons.v += dt*(0.04*neurons.v .^2 + 5 * neurons.v + 140 - neurons.u + input)
    uNext = dt * (neurons.params.a .* (neurons.params.b * neurons.v - neurons.u))
    neurons.u += uNext
    # Find where spikes occur
    isspike(v) = (v .>= 30)
    spikeInd = find(isspike(neurons.v))
    neurons.lastSpike += dt
    neurons.lastSpike[spikeInd] = 0.

    # Update variables
    neurons.v[spikeInd] = neurons.params.c
    neurons.u[spikeInd] += neurons.params.d - uNext[spikeInd]

    return neurons.v, spikeInd
end

end
