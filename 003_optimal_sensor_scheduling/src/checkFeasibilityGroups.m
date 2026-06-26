function groupCount = checkFeasibilityGroups(systems)
%CHECKFEASIBILITYGROUPS Algorithm 1 in a direct implementation.

unstable = [];
for idx = 1:numel(systems)
    if max(abs(eig(systems(idx).A))) >= 1
        unstable(end + 1) = idx; %#ok<AGROW>
    end
end

if isempty(unstable)
    groupCount = 0;
    return;
end

[~, order] = sort(arrayfun(@(idx) max(abs(eig(systems(idx).A))), unstable), 'descend');
sortedIndices = unstable(order);

groups = {sortedIndices(1)};
for ptr = 2:numel(sortedIndices)
    idx = sortedIndices(ptr);
    placed = false;
    for groupId = 1:numel(groups)
        members = [groups{groupId}, idx];
        maxRho = max(arrayfun(@(member) max(abs(eig(systems(member).A))), members));
        maxLoss = max(arrayfun(@(member) 1 - systems(member).lambda, members));
        if maxRho^2 * maxLoss < 1
            groups{groupId}(end + 1) = idx; %#ok<AGROW>
            placed = true;
            break;
        end
    end
    if ~placed
        groups{end + 1} = idx; %#ok<AGROW>
    end
end

groupCount = numel(groups);
end
