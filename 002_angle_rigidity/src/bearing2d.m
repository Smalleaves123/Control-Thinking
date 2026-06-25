function z = bearing2d(positions, i, j)
%BEARING2D Unit bearing z_ij = (p_j - p_i) / ||p_j - p_i||.

delta = positions(j, :) - positions(i, :);
normValue = norm(delta);
if normValue <= 1e-9
    error('bearing2d:DegeneratePair', 'Cannot compute bearing for coincident agents.');
end
z = delta / normValue;
end
