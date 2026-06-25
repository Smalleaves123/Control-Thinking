function alpha = unsignedAngleAt(positions, j, i, k)
%UNSIGNEDANGLEAT Interior angle alpha_jik at agent i.

zij = bearing2d(positions, i, j);
zik = bearing2d(positions, i, k);
dotValue = max(-1, min(1, dot(zij, zik)));
alpha = acos(dotValue);
end
