function writeJson(filePath, data)
%WRITEJSON Write a struct as JSON text.

text = jsonencode(data);
fid = fopen(filePath, 'w');
if fid < 0
    error('writeJson:OpenFailed', 'Cannot open %s for writing.', filePath);
end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', text);
end
