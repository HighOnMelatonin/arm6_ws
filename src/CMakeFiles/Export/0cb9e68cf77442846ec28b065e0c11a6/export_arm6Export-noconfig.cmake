#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "arm6::arm6" for configuration ""
set_property(TARGET arm6::arm6 APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(arm6::arm6 PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libarm6.so"
  IMPORTED_SONAME_NOCONFIG "libarm6.so"
  )

list(APPEND _cmake_import_check_targets arm6::arm6 )
list(APPEND _cmake_import_check_files_for_arm6::arm6 "${_IMPORT_PREFIX}/lib/libarm6.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
