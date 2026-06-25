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

s2 = sqrt(2);
s5 = sqrt(5);
baseEdges = [
    3, 1;
    2, 1;
    3, 2;
    4, 2;
    4, 1;
    4, 3;
    5, 4;
    5, 2;
    5, 1
];
baseBearings = [
     1,              0;
     s2 / 2,        -s2 / 2;
     s2 / 2,         s2 / 2;
     0,             -1;
     s5 / 5,        -2 * s5 / 5;
    -s5 / 5,        -2 * s5 / 5;
     2 * s5 / 5,    -s5 / 5;
    -s5 / 5,        -2 * s5 / 5;
     3 / sqrt(10),  -1 / sqrt(10)
];

edgeCount = size(baseEdges, 1);
spec.bearingEdges = [baseEdges; fliplr(baseEdges)];
spec.desiredBearings = [baseBearings; -baseBearings];
end
