module neuron

export HHparams, HHneurons, IzhiParams, IzhiNeurons, MNparams, MNneurons, update!

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

type MNparams <: NeuronParams
    # Current params
    k::Array{Float64,1}
    # Voltage params
    C::Float64
    G::Float64
    El::Float64
    # Threshold params
    θinf::Float64
    a::Float64
    b::Float64
    # Spike update rule params
    R::Array{Float64,1}
    A::Array{Float64,1}
    Vr::Float64
    θr::Float64

    MNparams(El, θinf, k, C, G, a, b, R, A, Vr, θr) = new(k,C,G,El,θinf,a,b,R,A,Vr,θr)
end

type MNneurons <: Neurons
    num_neur::Int64         # Number of Neurons in population
    params::MNparams        # Neuron parameters
    V::Array{Float64,1}     # Variables
    θ::Array{Float64,1}
    Iint::Array{Float64,2}
    lastSpike::Array{Float64,1}
    MNneurons(num_neur, params) = new(num_neur, params, params.El*ones(num_neur), params.θinf*ones(num_neur), zeros(num_neur, length(params.R)),  zeros(num_neur))
end

function update!(neurons::MNneurons, input, dt)
    # Calculate state variable updates
    neurons.θ += dt * (neurons.params.a * (neurons.V - neurons.params.El) - neurons.params.b * (neurons.θ - neurons.params.θinf))
    neurons.V += dt * (input + vec(sum(neurons.Iint,2)) - neurons.params.G * (neurons.V - neurons.params.El))./neurons.params.C
    neurons.Iint .-= dt * (neurons.params.k' .* neurons.Iint)

    # Find where spikes occur
    isspike(v) = (v .>= neurons.θ)
    spikeInd = find(isspike(neurons.V))
    neurons.lastSpike += dt
    neurons.lastSpike[spikeInd] = 0.

    # Spike update rules
    # TODO: NOT sure if this works (particularly I)
    neurons.V[spikeInd] = neurons.params.Vr
    neurons.Iint[spikeInd,:] = neurons.params.R' .* neurons.Iint[spikeInd,:] .+ neurons.params.A'
    neurons.θ[spikeInd] = max.(neurons.θ, neurons.params.θr)[spikeInd]

    return neurons.V, neurons.θ, spikeInd
end

type MNBCparams <: NeuronParams
    # Membrane capacitances
    Cm::Float64
    Ct::Float64
    # Spike update rule params
    Vr::Float64
    θr::Float64
    # Switch-cap parameters
    Csm::Float64
    Cst::Float64

    # Leakage capacitance
    Cl::Float64
    # Leakage clock frequency (Phi1, Phi2 on chip)
    flm::Float64
    flt::Float64
    # Leakage conductances - calculated from Cl and Fl(m,t)
    glm::FLoat64
    glt::Float64


    MNBCparams() = new(glm,glt,Cm,Ct,Cl,Vr,θr,Csm,Cst)
end

type MNBCneurons <: Neurons
    num_neur::Int64         # Number of Neurons in population
    params::MNparams        # Neuron parameters
    V::Array{Float64,1}     # Variables
    θ::Array{Float64,1}
    Iint::Array{Float64,2}
    lastSpike::Array{Float64,1}
    MNneurons(num_neur, params) = new(num_neur, params, params.El*ones(num_neur), params.θinf*ones(num_neur), zeros(num_neur,length(params.R)),  zeros(num_neur))
end

function update!(neurons::MNBCneurons, input, dt)
    # Calculate state variable updates
    neurons.θ += dt * (neurons.params.a * (neurons.V - neurons.params.El) - neurons.params.b * (neurons.θ - neurons.params.θinf))
    neurons.V += dt * (input + vec(sum(neurons.Iint,2)) - neurons.params.G * (neurons.V - neurons.params.El))./neurons.params.C
    neurons.Iint .-= dt * (neurons.params.k' .* neurons.Iint)

    # Find where spikes occur
    isspike(v) = (v .>= neurons.θ)
    spikeInd = find(isspike(neurons.V))
    neurons.lastSpike += dt
    neurons.lastSpike[spikeInd] = 0.

    # Spike update rules
    # TODO: NOT sure if this works (particularly I)
    neurons.V[spikeInd] = neurons.params.Vr
    neurons.Iint[spikeInd,:] = neurons.params.R' .* neurons.Iint[spikeInd,:] .+ neurons.params.A'
    neurons.θ[spikeInd] = max.(neurons.θ, neurons.params.θr)[spikeInd]

    return neurons.V, neurons.θ, spikeInd
end

end
