function trajectory = simulateFormation(initialPositions, controller, dt, steps)
%SIMULATEFORMATION Euler simulation of single-integrator agents.

agentCount = size(initialPositions, 1);
trajectory = zeros(steps + 1, agentCount, 2);
trajectory(1, :, :) = initialPositions;

positions = initialPositions;
for step = 1:steps
    positions = positions + dt * controller(positions);
    trajectory(step + 1, :, :) = positions;
end
end
