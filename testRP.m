
% Path to directory containing REFPROP.h header file
path_to_include= '.'; 
% Path to directory containing librefprop.so (change as needed)
path_to_lib = '.';   

% Loading shared library
if ~libisloaded('refprop') %checking whether library is already loaded
    libname = 'REFPRP64'; % OSX and linux
    if ~ispc
        libname = 'libREFPRP64';
    end
    loadlibrary(libname,'REFPROP.h','includepath',path_to_include,'alias','refprop'); % loading library with alias coolprop
    % Uncomment these lines to see the functions that were exported
    % disp('loaded REFPROP shared library; loaded these functions: ')
    % libfunctions refprop
end
% Uncomment this line to see all the functions exported by REFPROP and
% their arguments
%libfunctionsview refprop

ncmax = 20;
herr_size = 255;
ierr = 0;
ncomp = 1;

% Uncomment this line and fill in if necessary to set the path to the 
% root directory for REFPROP
% -----
% [fldpath] = calllib('refprop','SETPATHdll','/path/to/REFPROP', 255);

fluid = 'WATER.FLD';
hmx = 'HMX.BNC';
ref = 'DEF';
b = (1:1:herr_size);
herr = char(b);

[ncomp,fluid,hmx,ref,ierr,herr] = calllib('refprop','SETUPdll',ncomp,fluid,hmx,ref,ierr,herr,10000,255,3,herr_size);

if ierr > 0
    fprintf('Error: %s',herr);
    return
end

t = 300; % [K]
p = 101.325; %[kPa]

z = zeros(1,ncmax);
z(1) = 1.0; % Pure water

d = 0; dl = 0; dv = 0; q = 0; e = 0; h = 0; s = 0; cv = 0; cp = 0; w = 0;

% Pointer to the mole fractions
pz = libpointer('doublePtr',z);
x = libpointer('doublePtr',zeros(1, ncmax));
y = libpointer('doublePtr',zeros(1, ncmax));

[t, p, pz, d, dl, dv, x, y, q, e, h, s, cv, cp, w, ierr, herr] = calllib('refprop','TPFLSHdll', t, p, pz, d, dl, dv, x, y, q, e, h, s, cv, cp, w, ierr, herr, herr_size);
if ierr > 0
    fprintf('Error: %s',herr);
    return
end
disp(s)
unloadlibrary('refprop')
