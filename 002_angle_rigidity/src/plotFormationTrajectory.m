function plotFormationTrajectory(trajectory, filePath, plotTitle)
%PLOTFORMATIONTRAJECTORY Save agent trajectories.

ensureDir(fileparts(filePath));
colors = [
    0.06, 0.36, 0.29;
    0.73, 0.27, 0.19;
    0.20, 0.35, 0.58;
    0.50, 0.33, 0.49;
    0.82, 0.57, 0.11
];

fig = figure('Visible', 'off');
hold on;
lineHandles = gobjects(size(trajectory, 2), 1);
for idx = 1:size(trajectory, 2)
    series = squeeze(trajectory(:, idx, :));
    lineHandles(idx) = plot(series(:, 1), series(:, 2), 'LineWidth', 2, 'Color', colors(idx, :));
    scatter(series(1, 1), series(1, 2), 35, colors(idx, :), 'o', 'filled', 'HandleVisibility', 'off');
    scatter(series(end, 1), series(end, 2), 55, colors(idx, :), 'x', 'LineWidth', 1.5, 'HandleVisibility', 'off');
end
title(plotTitle);
xlabel('x');
ylabel('y');
axis equal;
grid on;
legend(lineHandles, {'agent 1', 'agent 2', 'agent 3', 'agent 4', 'agent 5'}, 'Location', 'best');
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
