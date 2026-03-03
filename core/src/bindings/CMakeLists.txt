set(HEADER_FILES
    ../../include/molaccess.hpp
    ../../include/molaccess_ipc.hpp
    molaccess_python.hpp
)

set(BINDING_FILES 
    molecular_wrap.cxx
    molaccess_python.cpp
)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

add_library(molaccesspy SHARED ${HEADER_FILES} ${BINDING_FILES})

set_target_properties(molaccesspy PROPERTIES OUTPUT_NAME "molaccesspy")
set_target_properties(molaccesspy PROPERTIES LINKER_LANGUAGE CXX)

target_include_directories(molaccesspy PUBLIC include)

target_include_directories(molaccesspy PUBLIC ${Python3_INCLUDE_DIRS})

target_link_libraries(molaccesspy molaccess Python::Python)

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    target_link_libraries(molaccesspy -mwindows)
endif()

link(molaccesspy)

install(TARGETS molaccesspy DESTINATION lib)
