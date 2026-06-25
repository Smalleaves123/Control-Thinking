function spec = paperFiveAgentSpec()
%PAPERFIVEAGENTSPEC Five-agent example from Section V of the paper.

spec.initialPositions = [
     0.8, 0.2;
     0.1, 1.4;
    -1.4, 0.3;
     0.1, 2.3;
    -1.7, 1.6
];

spec.angleTriplets = [
    2, 1, 3;  % alpha_213
    1, 3, 2;  % alpha_132
    3, 2, 1;  % alpha_321
    3, 4, 2;  % alpha_342
    2, 4, 1;  % alpha_241
    2, 5, 4;  % alpha_254
    1, 5, 2   % alpha_152
];

spec.desiredAngles = [
    pi / 4;
    pi / 4;
    pi / 2;
    atan(0.5);
    atan(0.5);
    atan(0.5);
    atan(3 / sqrt(10))
];

spec.desiredBearingPositions = [
     1, 0;
     0, 1;
    -1, 0;
     0, 2;
    -2, 1
];

% The bearing-based simulation in Figs. 14-17 uses the directed constraints
% shown in Fig. 15/17 rather than the reciprocal closure we tested earlier.
spec.bearingEdges = [
    1, 4;
    1, 2;
    2, 3;
    2, 4;
    3, 4;
    3, 1;
    4, 5;
    4, 3;
    5, 2;
    5, 1
];

edgeCount = size(spec.bearingEdges, 1);
spec.desiredBearings = zeros(edgeCount, 2);
for idx = 1:edgeCount
    i = spec.bearingEdges(idx, 1);
    j = spec.bearingEdges(idx, 2);
    delta = spec.desiredBearingPositions(j, :) - spec.desiredBearingPositions(i, :);
    spec.desiredBearings(idx, :) = delta / norm(delta);
end
end
