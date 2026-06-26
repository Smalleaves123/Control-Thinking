function result = simulateSchedulingScenario(systems, policyName, maxActive, horizon, maxDelay)
%SIMULATESCHEDULINGSCENARIO Run one scenario under a given heuristic.

sensorCount = numel(systems);
delays = zeros(sensorCount, 1);
totalStageCosts = zeros(horizon, 1);
activeCounts = zeros(horizon, 1);

for step = 1:horizon
    [activeFlags, ~] = selectSensors(policyName, systems, delays, maxActive, maxDelay);
    activeCounts(step) = sum(activeFlags);

    stageCost = 0.0;
    for idx = 1:sensorCount
        stageCost = stageCost + systems(idx).errorTraceCache(delays(idx) + 1);
        if activeFlags(idx)
            stageCost = stageCost + systems(idx).commCost;
            if rand() <= systems(idx).lambda
                delays(idx) = 0;
            else
                delays(idx) = min(delays(idx) + 1, maxDelay);
            end
        else
            delays(idx) = min(delays(idx) + 1, maxDelay);
        end
    end
    totalStageCosts(step) = stageCost;
end

result = struct();
result.averageCost = mean(totalStageCosts);
result.activeRatio = mean(activeCounts) / maxActive;
end
