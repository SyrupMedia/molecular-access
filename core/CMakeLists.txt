set(HEADER_FILES
    include/molaccess.hpp
    include/molaccess_ipc.hpp
)

set(SOURCE_FILES
    src/molaccess.cpp
)

set(BINDING_FILES 
    src/bindings/molecular_wrap.cpp
)

set(MAIN src/main.cpp)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

add_library(molaccess SHARED ${HEADER_FILES} ${SOURCE_FILES} ${BINDING_FILES})

set_target_properties(molaccess PROPERTIES OUTPUT_NAME "molaccess")
set_target_properties(molaccess PROPERTIES LINKER_LANGUAGE CXX)

target_include_directories(molaccess PUBLIC include)

target_include_directories(molaccess PUBLIC ${Python3_INCLUDE_DIRS})

target_link_libraries(molaccess Python::Python)

link(molaccess)