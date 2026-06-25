function plotErrorSeries(times, errors, filePath, plotTitle, yLabelText)
%PLOTERRORSERIES Save constraint error curves.

ensureDir(fileparts(filePath));
fig = figure('Visible', 'off');
plot(times, errors, 'LineWidth', 1.6);
title(plotTitle);
xlabel('time [s]');
ylabel(yLabelText);
grid on;
labels = arrayfun(@(idx) sprintf('constraint %d', idx), 1:size(errors, 2), 'UniformOutput', false);
legend(labels, 'Location', 'northeast');
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
