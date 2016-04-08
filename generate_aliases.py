from __future__ import print_function
import sys, os

def tokenize(path_to_REFPROP_lib_h, path_to_FORTRAN):
    """
    Consume the REFPROP header and generate a list of functions 
    included in the shared library with their mixed-case windows-style
    symbols
    """
    with open(path_to_REFPROP_lib_h, 'r') as fp:
        lines = fp.readlines()
    tokens = []
    for line in lines:
        if line.strip().startswith('X('):
            tok = line.rstrip('\\\n').strip().split('X(')[1].strip().rstrip(')')
            tokens.append(tok)
    unresolved_tokens = []
    # Now check that each of the functions can be found in at least one of the REFPROP files
    # First try PASS_FTN
    with open(os.path.join(path_to_FORTRAN,"PASS_FTN.FOR"), 'r') as fp:
        PASS_FTN = fp.read()
        for token in tokens:
            if ' '+token not in PASS_FTN:
                unresolved_tokens.append(token)
    print("unresolved_tokens:",unresolved_tokens,'; skipping these aliases')
    for unresolved in unresolved_tokens:
        tokens.pop(tokens.index(unresolved))
    return tokens

def generate_aliases(tokens, mangling):
    """
    Arguments
    ---------
    tokens: list of strings
        The mixed-case windows-style names obtained from tokenize (SETUPdll for instance)
    mangling: str 
        The way in which the SETUPdll function is mangled. ("_setupdll_" for instance)

    Returns
    -------
    aliases: list of tuples
        In each tuple is the windows name, followed by the mangled name
    """

    if mangling == 'setupdll_':
        return [(t,t.lower()+'_') for t in tokens]
    elif mangling == '_setupdll':
        return [(t,'_'+t.lower()) for t in tokens]
    elif mangling == 'setupdll':
        return [(t,t.lower()) for t in tokens]
    else:
        raise KeyError("I don't understand your mangling [{0:s}]".format(mangling))

def write_aliases(output_file, aliases, using_defsym):
    with open(output_file, 'w') as fp:
        fp.write('-Wl')
        if using_defsym:
            for mixed_case, new in aliases:
                # For some bizarre reason, OSX always wants a preceding underscore
                # See https://developer.apple.com/library/mac/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/DynamicLibraryDesignGuidelines.html
                if sys.platform == 'darwin':
                    mixed_case = '_' + mixed_case
                    new = '_' + new
                fp.write(',--defsym,{0:s}={1:s}'.format(mixed_case,new))
        else:
            for mixed_case, new in aliases:
                # For some bizarre reason, OSX always wants a preceding underscore
                # See https://developer.apple.com/library/mac/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/DynamicLibraryDesignGuidelines.html
                if sys.platform == 'darwin':
                    mixed_case = '_' + mixed_case
                    new = '_' + new
                fp.write(',-alias,{0:s},{1:s}'.format(new,mixed_case))

def write_def_file(output_file, aliases):
    """
    Write a .DEF file that lists the symbols to be exported from the DLL

    Only needed in MINGW on windows
    """
    with open(output_file,'w') as fp:
        fp.write('EXPORTS ')
        for mixed_case, new in aliases:
            fp.write(mixed_case + " = " + new + '\n')

if __name__=='__main__':

    print(sys.platform)

    # Uncomment for local testing of this script
    #sys.argv += ['--mangling','setupdll_','-O','aliases.txt','--FORTRAN-path','R:/911FILES','--DEF-file','defs.DEF']

    # Parse args first
    import argparse
    parser = argparse.ArgumentParser(description='Run the symbol alias generator.')
    parser.add_argument('--mangling', '-M', required = True, choices=['setupdll','setupdll_','_setupdll'], help="A string for the mangled name of the SETUPdll function")
    parser.add_argument('--output-file', '-O', required = True, help="The file to which the command line snippet will be written")
    parser.add_argument('--using-defsym', nargs='?', const=True, default=False, help="If defined, --defsym aliases will be generated, otherwise -alias aliases will be generated")
    parser.add_argument('--FORTRAN-path', nargs=1, default="", help="If defined, the path to the directory containing the FORTRAN source files, otherwise, FORTRAN relative to the working directory")
    parser.add_argument('--DEF-file', nargs=1, default="", help="If defined, the path to the DEF file with the exported symbols (MINGW on windows only)")
    args = parser.parse_args()
    
    this_folder = os.path.dirname(__file__)
    # Get path to header
    header_path = os.path.join(this_folder,'externals','REFPROP-headers','REFPROP_lib.h')
    # Path to FORTRAN directory
    if args.FORTRAN_path == "":
        FORTRAN_path = os.path.join(this_folder,'FORTRAN')
    else:
        FORTRAN_path = args.FORTRAN_path[0]
    # Extract function names
    tokens = tokenize(header_path, FORTRAN_path)
    # Generate the aliases
    aliases = generate_aliases(tokens, args.mangling)
    # Write the aliases to file given by the command line argument output-file
    write_aliases(args.output_file, aliases, args.using_defsym)
    if args.DEF_file:
        # Write DEF file for MINGW gfortran
        write_def_file(args.DEF_file[0], aliases)