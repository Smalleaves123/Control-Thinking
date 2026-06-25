function P = projectionMatrix(z)
%PROJECTIONMATRIX Orthogonal projection P_z = I - z z^T.

z = z(:) / norm(z);
P = eye(2) - z * z';
end
