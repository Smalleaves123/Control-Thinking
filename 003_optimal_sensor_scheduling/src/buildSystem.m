function system = buildSystem(A, C, Q, R, lambda, commCost)
%BUILDSYSTEM Create one process description.

system = struct();
system.A = A;
system.C = C;
system.Q = Q;
system.R = R;
system.lambda = lambda;
system.commCost = commCost;
system.P = steadyStateKalmanCovariance(A, C, Q, R);
system.cacheMaxDelay = -1;
system.errorTraceCache = [];
system.thresholdAverageErrorCache = [];
system.whittleIndexCache = [];
end
