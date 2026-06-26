function result = runRelativeValueIteration2D(systems, maxActive, maxDelay, maxIterations)
%RUNRELATIVEVALUEITERATION2D Relative value iteration on a truncated grid.

gridSize = maxDelay + 1;
values = zeros(gridSize, gridSize);
policy = zeros(gridSize, gridSize);
actions = computeActionVectors(2, maxActive);

for iter = 1:maxIterations
    newValues = zeros(gridSize, gridSize);
    newPolicy = zeros(gridSize, gridSize);

    for tau1 = 0:maxDelay
        for tau2 = 0:maxDelay
            bestCost = inf;
            bestActionIndex = 1;
            for actionIndex = 1:size(actions, 1)
                action = actions(actionIndex, :);
                stageCost = errorTraceAtDelay(systems(1), tau1) + errorTraceAtDelay(systems(2), tau2) ...
                    + systems(1).commCost * action(1) + systems(2).commCost * action(2);

                expectedValue = 0.0;
                nextStates1 = nextDelayDistribution(tau1, action(1), systems(1).lambda, maxDelay);
                nextStates2 = nextDelayDistribution(tau2, action(2), systems(2).lambda, maxDelay);
                for row1 = 1:size(nextStates1, 1)
                    for row2 = 1:size(nextStates2, 1)
                        probability = nextStates1(row1, 2) * nextStates2(row2, 2);
                        expectedValue = expectedValue + probability * values(nextStates1(row1, 1) + 1, nextStates2(row2, 1) + 1);
                    end
                end

                totalCost = stageCost + expectedValue;
                if totalCost < bestCost
                    bestCost = totalCost;
                    bestActionIndex = actionIndex;
                end
            end

            newValues(tau1 + 1, tau2 + 1) = bestCost;
            chosen = actions(bestActionIndex, :);
            if all(chosen == [0, 0])
                newPolicy(tau1 + 1, tau2 + 1) = 0;
            elseif all(chosen == [1, 0])
                newPolicy(tau1 + 1, tau2 + 1) = 1;
            elseif all(chosen == [0, 1])
                newPolicy(tau1 + 1, tau2 + 1) = 2;
            else
                newPolicy(tau1 + 1, tau2 + 1) = 3;
            end
        end
    end

    newValues = newValues - newValues(1, 1);
    if max(abs(newValues(:) - values(:))) <= 1e-7 && isequal(newPolicy, policy)
        values = newValues;
        policy = newPolicy;
        break;
    end

    values = newValues;
    policy = newPolicy;
end

result = struct();
result.values = values;
result.policy = policy;
result.actions = actions;
end

function transitions = nextDelayDistribution(currentDelay, scheduled, lambda, maxDelay)
if scheduled == 1
    failedDelay = min(currentDelay + 1, maxDelay);
    transitions = [
        0, lambda;
        failedDelay, 1 - lambda
    ];
    if failedDelay == 0
        transitions = [0, 1];
    end
else
    transitions = [min(currentDelay + 1, maxDelay), 1];
end
end
