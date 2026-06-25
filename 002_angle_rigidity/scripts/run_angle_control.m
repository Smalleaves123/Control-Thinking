%RUN_ANGLE_CONTROL Five-agent angle-rigidity formation-control example.

clear; clc;
projectRoot = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(projectRoot, 'src'));

dt = 0.01;
steps = 5000;
gain = 1.0;
misalignedAgent = 1;
theta = deg2rad(5.0);

spec = paperFiveAgentSpec();
controller = @(positions) angleControlInput( ...
    positions, spec.angleTriplets, spec.desiredAngles, gain, misalignedAgent, theta);

trajectory = simulateFormation(spec.initialPositions, controller, dt, steps);
times = (0:steps)' * dt;

angleErrors = zeros(steps + 1, size(spec.angleTriplets, 1));
for idx = 1:(steps + 1)
    positions = squeeze(trajectory(idx, :, :));
    angleErrors(idx, :) = (currentAngles(positions, spec.angleTriplets) - spec.desiredAngles)';
end

metrics = angleSimulationMetrics(trajectory, spec.angleTriplets, spec.desiredAngles);

figuresDir = fullfile(projectRoot, 'results', 'figures');
logsDir = fullfile(projectRoot, 'results', 'logs');
ensureDir(figuresDir);
ensureDir(logsDir);

plotFormationTrajectory( ...
    trajectory, ...
    fullfile(figuresDir, 'angle_control_trajectory.png'), ...
    'Angle Rigidity-Based Control With Local-Frame Misalignment');
plotErrorSeries( ...
    times, angleErrors, ...
    fullfile(figuresDir, 'angle_control_errors.png'), ...
    'Angle Errors Under Angle Rigidity-Based Control', ...
    'angle error [rad]');
plotRankBar( ...
    metrics.final_rank, metrics.expected_rank, ...
    fullfile(figuresDir, 'angle_rigidity_rank.png'));

writeJson(fullfile(logsDir, 'angle_control_metrics.json'), metrics);
disp(jsonencode(metrics));
