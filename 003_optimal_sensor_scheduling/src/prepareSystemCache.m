function system = prepareSystemCache(system, maxDelay)
%PREPARESYSTEMCACHE Precompute traces and Whittle indices up to maxDelay.

if system.cacheMaxDelay >= maxDelay
    return;
end

traces = zeros(maxDelay + 1, 1);
covariance = system.P;
traces(1) = trace(covariance);
for delay = 1:maxDelay
    covariance = applyOpenLoop(system, covariance);
    traces(delay + 1) = trace(covariance);
end

thresholdErrors = zeros(maxDelay + 1, 1);
for threshold = 0:maxDelay
    thresholdErrors(threshold + 1) = thresholdAverageErrorFromCache(system, traces, threshold, maxDelay);
end

prefix = cumsum(traces);
indices = zeros(maxDelay + 1, 1);
for tau = 0:maxDelay
    lambda = system.lambda;
    indices(tau + 1) = lambda * (lambda * tau + 1) / (1 - lambda) ...
        * ((tau + 1) * thresholdErrors(tau + 1) - prefix(tau + 1)) ...
        - system.commCost;
end

system.cacheMaxDelay = maxDelay;
system.errorTraceCache = traces;
system.thresholdAverageErrorCache = thresholdErrors;
system.whittleIndexCache = indices;
end

function averageError = thresholdAverageErrorFromCache(system, traces, threshold, maxDelay)
lambda = system.lambda;
baseWeight = lambda / (lambda * threshold + 1);

if isscalar(system.A)
    beta = system.A^2;
    xThreshold = remoteErrorCovariance(system, threshold);
    prefix = sum(traces(1:threshold + 1));
    alpha = 1 - lambda;
    if abs(beta - 1) <= 1e-12
        tail = alpha / (1 - alpha) * xThreshold + system.Q * alpha / (1 - alpha)^2;
    else
        tailState = alpha * beta / (1 - alpha * beta) * xThreshold;
        tailNoise = system.Q / (beta - 1) * (alpha * beta / (1 - alpha * beta) - alpha / (1 - alpha));
        tail = tailState + tailNoise;
    end
    averageError = baseWeight * (prefix + tail);
    return;
end

weights = zeros(maxDelay + 1, 1);
for delay = 0:maxDelay
    if delay <= threshold
        weights(delay + 1) = baseWeight;
    else
        weights(delay + 1) = baseWeight * (1 - lambda)^(delay - threshold);
    end
end

tailMass = max(0, 1 - sum(weights));
weights(end) = weights(end) + tailMass;
averageError = sum(weights .* traces);
end
