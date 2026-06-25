function value = rigidityRank(positions, triplets)
%RIGIDITYRANK Numerical rank of the angle rigidity matrix.

value = rank(angleRigidityMatrix(positions, triplets), 1e-8);
end
