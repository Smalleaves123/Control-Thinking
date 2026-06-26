function value = whittleIndex(system, tau, maxDelay)
%WHITTLEINDEX Closed-form Whittle index from Theorem 3.

if system.cacheMaxDelay < maxDelay || isempty(system.whittleIndexCache)
    system = prepareSystemCache(system, maxDelay);
end

value = system.whittleIndexCache(tau + 1);
end
