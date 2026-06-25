function plotRankBar(rankValue, expectedRank, filePath)
%PLOTRANKBAR Save the angle-rigidity rank check.

ensureDir(fileparts(filePath));
fig = figure('Visible', 'off');
bar([rankValue, expectedRank]);
set(gca, 'XTickLabel', {'rank(R_a)', '2N-4'});
ylabel('rank');
title('Angle Rigidity Rank Check');
grid on;
ylim([0, max(rankValue, expectedRank) + 1]);
print(fig, filePath, '-dpng', '-r180');
close(fig);
end
