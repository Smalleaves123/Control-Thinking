function P = steadyStateKalmanCovariance(A, C, Q, R)
%STEADYSTATEKALMANCOVARIANCE Fixed-point iteration for local Kalman covariance.

P = Q;
for iter = 1:5000
    S = C * P * C' + R;
    K = A * P * C' / S;
    nextP = A * P * A' + Q - K * C * P * A';
    if norm(nextP - P, 'fro') <= 1e-10 * max(1, norm(P, 'fro'))
        P = nextP;
        return;
    end
    P = nextP;
end
end
