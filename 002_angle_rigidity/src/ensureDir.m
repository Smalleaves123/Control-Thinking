function ensureDir(pathName)
%ENSUREDIR Create a directory if needed.

if ~exist(pathName, 'dir')
    mkdir(pathName);
end
end
