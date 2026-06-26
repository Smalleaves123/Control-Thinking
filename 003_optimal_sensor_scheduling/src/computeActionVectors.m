function actions = computeActionVectors(sensorCount, maxActive)
%COMPUTEACTIONVECTORS Enumerate feasible scheduling actions.

rows = [];
for mask = 0:(2^sensorCount - 1)
    bits = bitget(mask, 1:sensorCount);
    if sum(bits) <= maxActive
        rows = [rows; bits]; %#ok<AGROW>
    end
end
actions = rows;
end
