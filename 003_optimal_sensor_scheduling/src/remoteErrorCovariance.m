function Ptau = remoteErrorCovariance(system, tau)
%REMOTEERRORCOVARIANCE Evaluate h_i^tau(P_i).

Ptau = system.P;
for idx = 1:tau
    Ptau = applyOpenLoop(system, Ptau);
end
end
