cmake_minimum_required (VERSION 2.8)
project (REFPROP)
enable_language(Fortran)

#######################################
#           BUILD OPTIONS             #
#-------------------------------------#
# These options are available to be   #
# modified in the build process.      #
# packages may want to modify these   #
# to suit, or just leave as defaults. #
#######################################

SET (REFPROP_FORTRAN_PATH
        "FORTRAN"
        CACHE STRING
        "The path to the directory of the FORTRAN source files")
                         
# make sure that the default is a RELEASE
if (NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE RELEASE CACHE STRING
      "Choose the type of build, options are: None Debug Release."
      FORCE)
endif ()
 
# FFLAGS depend on the compiler
get_filename_component (Fortran_COMPILER_NAME ${CMAKE_Fortran_COMPILER} NAME)

# My default, no symbol aliases are used
set (ALIASES_STRING "")

set (REFPROP_LINK_FLAGS "")

if (Fortran_COMPILER_NAME MATCHES "gfortran.*")
  # gfortran
  set (CMAKE_Fortran_FLAGS_RELEASE "-funroll-all-loops -fno-f2c -O3")
  set (CMAKE_Fortran_FLAGS_DEBUG   "-fno-f2c -O0 -g")
  
  # Now we need to determine whether gfortran uses --defsym or -alias to 
  # define symbol aliases for the linker
  execute_process(COMMAND gfortran -Wl,--defsym
                  RESULT_VARIABLE DEFSYM_CHECK_RESULT
                  OUTPUT_VARIABLE DEFSYM_CHECK_OUTPUT
                  ERROR_VARIABLE DEFSYM_CHECK_OUTPUT
                  )
  # If there is a note in the output about defsym syntax error, 
  # defsym is the alias keyword, but it didn't understand the argument.
  # That's good, it means we should use --defsym to define aliases
  string(FIND "${DEFSYM_CHECK_OUTPUT}" "syntax error" DEFSYM_STR_INDEX) 
  if (${DEFSYM_STR_INDEX} GREATER 0)
    set(DEFSYM_FLAG "--using-defsym")
  endif()
  message(STATUS "DEFSYM_FLAG: ${DEFSYM_FLAG}") 
  execute_process(COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/generate_aliases.py" --mangling setupdll_ -O "${CMAKE_CURRENT_BINARY_DIR}/aliases_string.txt" --FORTRAN-path "${REFPROP_FORTRAN_PATH}" ${DEFSYM_FLAG}
                  RESULT_VARIABLE GEN_ALIASES_RESULT
                  OUTPUT_VARIABLE GEN_ALIASES_OUTPUT
                  ERROR_VARIABLE GEN_ALIASES_OUTPUT
                  )
  message(STATUS "${GEN_ALIASES_OUTPUT}") 
  file(READ "${CMAKE_CURRENT_BINARY_DIR}/aliases_string.txt" ALIASES_STRING)

  # Start off with the aliases
  set (REFPROP_LINK_FLAGS "${ALIASES_STRING}")

  # On OSX, we want to statically link the libquadmath library, but gfortran is VERY
  # insistent that it wants a dynamically linked libquadmath.  See also this open bug
  # for gfortran: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46539
  # For Mac systems
  if ("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
    execute_process(COMMAND gfortran -print-file-name=libquadmath.a
                    RESULT_VARIABLE LIBQUADMATH_CHECK_RESULT
                    OUTPUT_VARIABLE LIBQUADMATH_CHECK_OUTPUT
                    ERROR_VARIABLE LIBQUADMATH_CHECK_OUTPUT
                    )
    string(STRIP ${LIBQUADMATH_CHECK_OUTPUT} LIBQUADMATH_PATH)
    message(STATUS "Path to libquadmath.a:" "${LIBQUADMATH_PATH}")
    file(COPY ${LIBQUADMATH_PATH} 
         DESTINATION .)
    message(STATUS "Copied libquadmath.a here.")

    # Now we construct the flags to be passed to linker
    set(REFPROP_LINK_FLAGS "${REFPROP_LINK_FLAGS} -static -static-libgfortran -static-libgcc ")

    # This, in concert with the libquadmath logic above, ensures that libquadmath is statically
    # linked rather than being dynamically linked.  We want a static link so that the shared
    # library can be distributed to users without gfortran
    set(REFPROP_LINK_FLAGS "${REFPROP_LINK_FLAGS} -L. ")
  endif()

elseif (Fortran_COMPILER_NAME MATCHES "ifort.*")
  # Force visual studio to statically link the c runtime to avoid dependency on MSVCRXXX.dll
  set (CMAKE_Fortran_FLAGS_RELEASE "-f77rtl -O3 /threads /libs:static /MT")
  set (CMAKE_Fortran_FLAGS_DEBUG   "-f77rtl -debug:full -Od /libs:static /MT")
else ()
  message ("CMAKE_Fortran_COMPILER full path: " ${CMAKE_Fortran_COMPILER})
  message ("Fortran compiler: " ${Fortran_COMPILER_NAME})
  message ("No optimized Fortran compiler flags are known, we just try -O2...")
  set (CMAKE_Fortran_FLAGS_RELEASE "-O2")
  set (CMAKE_Fortran_FLAGS_DEBUG   "-O0 -g")
endif()

# TODO: set to either REFPROP or REFPRP64
set(NAME "REFPRP64")

# Collect the source files
file(GLOB APP_SOURCES "${REFPROP_FORTRAN_PATH}/*.FOR")

add_library(${NAME} SHARED ${APP_SOURCES})

if (WIN32)
  # Don't add a 'lib' prefix to the shared library if windows
  set_target_properties(${NAME} PROPERTIES PREFIX "")
endif()

set_target_properties(${NAME} PROPERTIES APPEND_STRING PROPERTY LINK_FLAGS "${REFPROP_LINK_FLAGS}")