function Ra = angleRigidityMatrix(positions, triplets)
%ANGLERIGIDITYMATRIX Build the angle rigidity matrix R_a(p).

agentCount = size(positions, 1);
constraintCount = size(triplets, 1);
Ra = zeros(constraintCount, 2 * agentCount);

for rowIdx = 1:constraintCount
    i = triplets(rowIdx, 1);
    j = triplets(rowIdx, 2);
    k = triplets(rowIdx, 3);

    zjk = bearing2d(positions, j, k);
    zji = bearing2d(positions, j, i);
    lji = norm(positions(i, :) - positions(j, :));
    ljk = norm(positions(k, :) - positions(j, :));
    beta = unsignedAngleAt(positions, i, j, k);
    sinBeta = sin(beta);

    if abs(sinBeta) <= 1e-9
        error('angleRigidityMatrix:DegenerateTriplet', 'Triplet %d is nearly collinear.', rowIdx);
    end

    Nkji = -(zjk * projectionMatrix(zji)) / (lji * sinBeta);
    Nijk = -(zji * projectionMatrix(zjk)) / (ljk * sinBeta);

    Ra(rowIdx, 2*i-1:2*i) = Nkji;
    Ra(rowIdx, 2*j-1:2*j) = -(Nkji + Nijk);
    Ra(rowIdx, 2*k-1:2*k) = Nijk;
end
end
