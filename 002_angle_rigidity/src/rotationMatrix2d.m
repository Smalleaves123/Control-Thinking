function R = rotationMatrix2d(theta)
%ROTATIONMATRIX2D Counterclockwise 2-D rotation matrix.

R = [cos(theta), -sin(theta); sin(theta), cos(theta)];
end
