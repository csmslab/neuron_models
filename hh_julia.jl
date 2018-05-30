using Plots
gr();
tic();
α_n(v) = (0.01 * (v + 55))/(1-exp(-(v+55)/10))
β_n(v) = 0.125 * exp(-(v + 65)/80)
α_m(v) = (0.1 * (v + 40))/(1-exp(-(v+40)/10))
β_m(v) = 4.0 * exp(-(v + 65)/18)
α_h(v) = 0.07 * exp(-(v + 65)/20)
β_h(v) = 1/(1 + exp(-(v + 35)/10))

gNa = 120
gK = 36
gL = 0.3

V_Na = 50
V_K = -77
V_L = -54.4
C = 1

t_total = 200
dt = 0.01
steps_total = convert(Int64,t_total/dt)
curr = fill(0.0,(steps_total,1))
curr[convert(Int64,20/dt):convert(Int64,(20.1/dt))] = 100;


Vm = fill(-65.0,(steps_total,1));
n = zeros(steps_total);
m = zeros(steps_total);
h = zeros(steps_total);

n[1] = α_n(Vm[1])/(α_n(Vm[1]) + β_n(Vm[1]));
m[1] = α_m(Vm[1])/(α_m(Vm[1]) + β_m(Vm[1]));
h[1] = α_h(Vm[1])/(α_h(Vm[1]) + β_h(Vm[1]));

for i in 1:steps_total-1
    dV = (curr[i] - gNa * (m[i]^3) * h[i] * (Vm[i] - V_Na) - gK * (n[i]^4) * (Vm[i] - V_K) - gL * (Vm[i] - V_L))/C;
    Vm[i+1] = Vm[i] + dV*dt;

    dn = α_n(Vm[i])*(1 - n[i]) - β_n(Vm[i])*n[i];
    n[i + 1] = n[i] + dn*dt;

    dm = α_m(Vm[i])*(1-m[i])-β_m(Vm[i])*m[i];
    m[i+1] = m[i]+dm*dt;

    dh = α_h(Vm[i])*(1-h[i])-β_h(Vm[i])*h[i];
    h[i+1] = h[i]+dh*dt;
end

t = 0.0:dt:t_total-dt;
out = [Vm curr];
toc()
plt = plot(t,out,label=["Membrane voltage", "Input current"],show=true)
display(plt)
