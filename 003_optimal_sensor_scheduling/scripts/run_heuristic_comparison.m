%RUN_HEURISTIC_COMPARISON Reproduce the heuristic comparison benchmark.

clear; clc;
projectRoot = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(projectRoot, 'src'));

rand('seed', 7);
randn('seed', 7);

scenarioSizes = [20, 30, 40];
scenarioChannels = [8, 12, 16];
% Use local-friendly defaults here. For a heavier server run, the paper uses
% horizon = 1000 and trials = 100.
horizon = 200;
trials = 8;
maxDelay = 100;
policyNames = {'max_error', 'max_delay', 'index', 'cindex'};
policyLabels = {'MaxError', 'MaxDelay', 'Index', 'cIndex'};

averageCosts = zeros(numel(scenarioSizes), numel(policyNames));
activeRatios = zeros(numel(scenarioSizes), 1);

for scenarioIdx = 1:numel(scenarioSizes)
    sensorCount = scenarioSizes(scenarioIdx);
    maxActive = scenarioChannels(scenarioIdx);
    trialCosts = zeros(trials, numel(policyNames));
    trialRatios = zeros(trials, 1);

    for trial = 1:trials
        systems = generateLargeScaleSystems(sensorCount, maxDelay);
        for policyIdx = 1:numel(policyNames)
            simulation = simulateSchedulingScenario(systems, policyNames{policyIdx}, maxActive, horizon, maxDelay);
            trialCosts(trial, policyIdx) = simulation.averageCost;
            if strcmp(policyNames{policyIdx}, 'cindex')
                trialRatios(trial) = simulation.activeRatio;
            end
        end
    end

    averageCosts(scenarioIdx, :) = mean(trialCosts, 1);
    activeRatios(scenarioIdx) = mean(trialRatios);
end

labels = arrayfun(@(n, m) sprintf('n=%d,m=%d', n, m), scenarioSizes, scenarioChannels, 'UniformOutput', false);

figuresDir = fullfile(projectRoot, 'results', 'figures');
logsDir = fullfile(projectRoot, 'results', 'logs');
ensureDir(figuresDir);
ensureDir(logsDir);

plotHeuristicComparison(labels, averageCosts, fullfile(figuresDir, 'heuristic_policy_comparison.png'));
plotActiveRatio(labels, activeRatios, fullfile(figuresDir, 'revised_index_active_ratio.png'));

metrics = struct();
metrics.labels = {labels};
metrics.policy_labels = {policyLabels};
metrics.average_costs = averageCosts;
metrics.active_ratios = activeRatios;

writeJson(fullfile(logsDir, 'heuristic_comparison_metrics.json'), metrics);
disp(jsonencode(metrics));
