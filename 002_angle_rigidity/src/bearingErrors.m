function errors = bearingErrors(trajectory, edges, desiredBearings)
%BEARINGERRORS Bearing error norms for every directed edge.

steps = size(trajectory, 1);
edgeCount = size(edges, 1);
errors = zeros(steps, edgeCount);

for step = 1:steps
    positions = squeeze(trajectory(step, :, :));
    for idx = 1:edgeCount
        i = edges(idx, 1);
        j = edges(idx, 2);
        errors(step, idx) = norm(bearing2d(positions, i, j) - desiredBearings(idx, :));
    end
end
end
