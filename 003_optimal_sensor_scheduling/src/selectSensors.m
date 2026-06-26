function [activeFlags, scores] = selectSensors(policyName, systems, delays, maxActive, maxDelay)
%SELECTSENSORS Apply one scheduling heuristic.

sensorCount = numel(systems);
scores = zeros(sensorCount, 1);

switch policyName
    case 'max_error'
        for idx = 1:sensorCount
            scores(idx) = systems(idx).errorTraceCache(delays(idx) + 1);
        end
        activeFlags = pickTop(scores, maxActive);
    case 'max_delay'
        scores = delays(:);
        activeFlags = pickTop(scores, maxActive);
    case 'index'
        for idx = 1:sensorCount
            scores(idx) = systems(idx).whittleIndexCache(delays(idx) + 1);
        end
        activeFlags = pickTop(scores, maxActive);
    case 'cindex'
        for idx = 1:sensorCount
            scores(idx) = systems(idx).whittleIndexCache(delays(idx) + 1);
        end
        activeFlags = pickTop(scores, maxActive);
        activeFlags = activeFlags & (scores > 0);
    otherwise
        error('selectSensors:UnknownPolicy', 'Unknown policy %s.', policyName);
end
end

function flags = pickTop(scores, maxActive)
flags = false(numel(scores), 1);
[~, order] = sort(scores, 'descend');
take = min(maxActive, numel(scores));
flags(order(1:take)) = true;
end
