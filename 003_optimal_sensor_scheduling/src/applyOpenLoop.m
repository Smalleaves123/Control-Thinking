function nextX = applyOpenLoop(system, X)
%APPLYOPENLOOP One application of h_i(X) = A X A^T + Q.

nextX = system.A * X * system.A' + system.Q;
end
