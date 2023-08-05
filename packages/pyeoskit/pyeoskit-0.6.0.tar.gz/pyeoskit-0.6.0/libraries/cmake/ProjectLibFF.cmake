include(ProjectMPIR)

set(prefix "${CMAKE_BINARY_DIR}/deps")
set(libff_library "${prefix}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}ff${CMAKE_STATIC_LIBRARY_SUFFIX}")
set(libff_inlcude_dir "${prefix}/include/libff")

ExternalProject_Add(libff
    PREFIX "${prefix}"
    DOWNLOAD_NAME libff-03b719a7.tar.gz
    DOWNLOAD_NO_PROGRESS TRUE
    URL https://github.com/learnforpractice/libff/archive/libff-shared.tar.gz
    URL_HASH SHA256=75d5536fe1a8bf124ce7741dd43b8ee56bcee655e10ba356e968938396425207
    CMAKE_ARGS
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DGMP_INCLUDE_DIR=${MPIR_INCLUDE_DIR}
        -DGMP_LIBRARY=${MPIR_LIBRARY}
        -DCURVE=ALT_BN128 -DPERFORMANCE=Off -DWITH_PROCPS=Off
        -DUSE_PT_COMPRESSION=Off
        -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
        -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
    BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR> --config Release
    LOG_BUILD 1
    INSTALL_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR> --config Release --target install
    BUILD_BYPRODUCTS "${libff_library}"
)

add_dependencies(libff mpir)

# Create snark imported library
add_library(libff::ff STATIC IMPORTED)
file(MAKE_DIRECTORY ${libff_inlcude_dir})
set_property(TARGET libff::ff PROPERTY IMPORTED_CONFIGURATIONS Release)
set_property(TARGET libff::ff PROPERTY IMPORTED_LOCATION_RELEASE ${libff_library})
set_property(TARGET libff::ff PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${libff_inlcude_dir})
set_property(TARGET libff::ff PROPERTY INTERFACE_LINK_LIBRARIES MPIR::mpir)
add_dependencies(libff::ff libff)
