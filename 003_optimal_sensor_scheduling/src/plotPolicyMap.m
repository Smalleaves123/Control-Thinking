function plotPolicyMap(policyGrid, filePath, plotTitle)
%PLOTPOLICYMAP Save the optimal policy map for n = 2.

ensureDir(fileparts(filePath));
fig = figure('Visible', 'off');
imagesc(0:size(policyGrid, 2) - 1, 0:size(policyGrid, 1) - 1, policyGrid);
set(gca, 'YDir', 'normal');
colormap([
    0.90, 0.90, 0.90;
    0.13, 0.47, 0.71;
    0.85, 0.33, 0.10;
    0.49, 0.18, 0.56
]);
colorbar('Ticks', [0.375, 1.125, 1.875, 2.625], 'TickLabels', {'none', 'sensor 1', 'sensor 2', 'both'});
title(plotTitle);
xlabel('\tau_2');
ylabel('\tau_1');
grid on;
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
