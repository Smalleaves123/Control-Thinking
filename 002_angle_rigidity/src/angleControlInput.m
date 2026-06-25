function controls = angleControlInput(positions, triplets, desiredAngles, gain, misalignedAgent, theta)
%ANGLECONTROLINPUT Unified angle-only controller in equation (58).

agentCount = size(positions, 1);
controls = zeros(agentCount, 2);

for idx = 1:size(triplets, 1)
    j = triplets(idx, 1);
    i = triplets(idx, 2);
    k = triplets(idx, 3);

    alpha = unsignedAngleAt(positions, j, i, k);
    term = bearing2d(positions, i, j) + bearing2d(positions, i, k);

    if i == misalignedAgent
        localTerm = (rotationMatrix2d(theta) * term')';
        term = (rotationMatrix2d(-theta) * localTerm')';
    end

    controls(i, :) = controls(i, :) - gain * (alpha - desiredAngles(idx)) * term;
end
end
