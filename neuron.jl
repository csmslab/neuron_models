module neuron

abstract Neuron

type HHneuron <: Neuron
    gNa::Float64
    gK::Float64
    gL::Float64
    VNa::Float64
    VK::Float64
    VL::Float64
    C::Float64

    Vmem::Float64
    m::Float64
    n::Float64
    h::Float64
    HHneuron(gNa,gK,gL,VNa,VK,VL,C) = new(gNa,gK,gL,VNa,VK,VL,C)
end

end
