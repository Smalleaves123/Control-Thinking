function systems = generateLargeScaleSystems(sensorCount, maxDelay)
%GENERATELARGESCALESYSTEMS Random first-order systems for the heuristic benchmark.

systems = repmat(struct(), sensorCount, 1);
for idx = 1:sensorCount
    A = 0.7 + 0.25 * randn();
    if abs(A) < 0.2
        A = sign(A + 1e-6) * 0.2;
    end
    C = 1 + 9 * rand();
    Q = 1 + 99 * rand();
    R = 1 + 99 * rand();
    lambda = 0.75 + 0.2 * rand();
    commCost = 5 + 10 * rand();
    systems(idx) = prepareSystemCache(buildSystem(A, C, Q, R, lambda, commCost), maxDelay);
end
end
