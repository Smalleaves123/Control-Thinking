function [averageError, commRate] = simulateThresholdStationaryCost(system, threshold, maxDelay)
%SIMULATETHRESHOLDSTATIONARYCOST Stationary cost under a threshold policy.

if system.cacheMaxDelay < maxDelay || isempty(system.errorTraceCache)
    system = prepareSystemCache(system, maxDelay);
end

lambda = system.lambda;
baseWeight = lambda / (lambda * threshold + 1);

delays = 0:maxDelay;
weights = zeros(size(delays));
for idx = 1:numel(delays)
    delay = delays(idx);
    if delay <= threshold
        weights(idx) = baseWeight;
    else
        weights(idx) = baseWeight * (1 - lambda)^(delay - threshold);
    end
end

tailMass = max(0, 1 - sum(weights));
weights(end) = weights(end) + tailMass;
averageError = sum(weights(:) .* system.errorTraceCache);
commRate = sum(weights(delays >= threshold));
end
