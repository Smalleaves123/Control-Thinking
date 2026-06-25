function controls = bearingControlInput(positions, edges, desiredBearings, gain, misalignedAgent, theta)
%BEARINGCONTROLINPUT Bearing-based comparison controller in equation (61).

agentCount = size(positions, 1);
controls = zeros(agentCount, 2);

for idx = 1:size(edges, 1)
    i = edges(idx, 1);
    j = edges(idx, 2);
    zij = bearing2d(positions, i, j);
    desired = desiredBearings(idx, :);

    if i == misalignedAgent
        desired = (rotationMatrix2d(theta) * desired')';
    end

    P = projectionMatrix(zij);
    controls(i, :) = controls(i, :) - gain * (P * desired')';
end
end
