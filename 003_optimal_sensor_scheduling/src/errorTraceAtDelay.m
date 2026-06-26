function value = errorTraceAtDelay(system, tau)
%ERRORTRACEATDELAY Remote estimation error trace at holding time tau.

if system.cacheMaxDelay >= tau && ~isempty(system.errorTraceCache)
    value = system.errorTraceCache(tau + 1);
else
    value = trace(remoteErrorCovariance(system, tau));
end
end
