%RUN_TWO_SENSOR_POLICY_EXAMPLE Reproduce the n = 2 monotone policy example.

clear; clc;
projectRoot = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(projectRoot, 'src'));

maxDelay = 20;
maxIterations = 500;
m = 1;

systemsNoCost = [
    buildSystem([1.1, 1; 0, 1], [2, 0; 0, 1], eye(2), eye(2), 0.8, 0);
    buildSystem([1, 1; 0, 1.2], eye(2), eye(2), eye(2), 0.9, 0)
];

systemsWithCost = [
    buildSystem([1.1, 1; 0, 1], [2, 0; 0, 1], eye(2), eye(2), 0.8, 20);
    buildSystem([1, 1; 0, 1.2], eye(2), eye(2), eye(2), 0.9, 10)
];

resultNoCost = runRelativeValueIteration2D(systemsNoCost, m, maxDelay, maxIterations);
resultWithCost = runRelativeValueIteration2D(systemsWithCost, m, maxDelay, maxIterations);

figuresDir = fullfile(projectRoot, 'results', 'figures');
logsDir = fullfile(projectRoot, 'results', 'logs');
ensureDir(figuresDir);
ensureDir(logsDir);

plotPolicyMap(resultNoCost.policy, fullfile(figuresDir, 'two_sensor_policy_no_cost.png'), ...
    'Optimal Policy for n = 2, m = 1 (No Transmission Cost)');
plotPolicyMap(resultWithCost.policy, fullfile(figuresDir, 'two_sensor_policy_with_cost.png'), ...
    'Optimal Policy for n = 2, m = 1 (With Transmission Cost)');

metrics = struct();
metrics.max_delay = maxDelay;
metrics.no_cost_feasible_groups = checkFeasibilityGroups(systemsNoCost);
metrics.with_cost_feasible_groups = checkFeasibilityGroups(systemsWithCost);
metrics.no_cost_unique_actions = numel(unique(resultNoCost.policy(:)));
metrics.with_cost_unique_actions = numel(unique(resultWithCost.policy(:)));

writeJson(fullfile(logsDir, 'two_sensor_policy_metrics.json'), metrics);
disp(jsonencode(metrics));
