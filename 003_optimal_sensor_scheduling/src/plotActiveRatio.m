function plotActiveRatio(labels, ratios, filePath)
%PLOTACTIVERATIO Plot active-sensor ratio for the revised index policy.

ensureDir(fileparts(filePath));
fig = figure('Visible', 'off');
plot(1:numel(labels), ratios, '-o', 'LineWidth', 2);
set(gca, 'XTick', 1:numel(labels), 'XTickLabel', labels);
ylabel('avg active sensors / m');
title('Active-Sensor Ratio Under Revised Whittle Index');
ylim([0, 1.1]);
grid on;
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
