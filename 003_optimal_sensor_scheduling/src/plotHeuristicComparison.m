function plotHeuristicComparison(labels, values, filePath)
%PLOTHEURISTICCOMPARISON Plot average costs across scenarios.

ensureDir(fileparts(filePath));
fig = figure('Visible', 'off');
bar(values);
set(gca, 'XTick', 1:numel(labels), 'XTickLabel', labels);
ylabel('average total cost');
title('Heuristic Policy Comparison');
grid on;
legend({'MaxError', 'MaxDelay', 'Index', 'cIndex'}, 'Location', 'northeast');
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
