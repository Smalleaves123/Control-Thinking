function metrics = angleSimulationMetrics(trajectory, triplets, desiredAngles)
%ANGLESIMULATIONMETRICS Final angle-control metrics.

finalPositions = squeeze(trajectory(end, :, :));
errors = currentAngles(finalPositions, triplets) - desiredAngles;
Ra = angleRigidityMatrix(finalPositions, triplets);

metrics = struct();
metrics.final_angle_rmse = sqrt(mean(errors .^ 2));
metrics.final_max_abs_angle_error = max(abs(errors));
metrics.final_rank = rigidityRank(finalPositions, triplets);
metrics.expected_rank = expectedFullRank(size(finalPositions, 1));
metrics.condition_number = cond(Ra * Ra');
end
