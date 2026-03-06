find_package(Python COMPONENTS Interpreter Development REQUIRED)

find_package(SWIG COMPONENTS python REQUIRED)
include(UseSWIG)

set_property(SOURCE molecular.i PROPERTY CPLUSPLUS ON)
swig_add_library(molaccesspy TYPE SHARED LANGUAGE python SOURCES molecular.i molaccess_python.cpp)

target_include_directories(molaccesspy PUBLIC ./)

target_link_libraries(molaccesspy molaccess Python::Python)

# not sure whether this is still needed
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    target_link_libraries(molaccesspy -mwindows)
endif()

link(molaccesspy)

install(TARGETS molaccesspy DESTINATION lib)
