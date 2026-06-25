function angles = currentAngles(positions, triplets)
%CURRENTANGLES Evaluate all interior angles alpha_jik.

count = size(triplets, 1);
angles = zeros(count, 1);
for idx = 1:count
    j = triplets(idx, 1);
    i = triplets(idx, 2);
    k = triplets(idx, 3);
    angles(idx) = unsignedAngleAt(positions, j, i, k);
end
end
