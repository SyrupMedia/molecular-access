set(HEADER_FILES
    include/molaccess.hpp
    include/molaccess_ipc.hpp
)

set(SOURCE_FILES
    src/molaccess.cpp
)
set(MAIN src/main.cpp)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

add_library(molaccess STATIC ${HEADER_FILES} ${SOURCE_FILES})
add_library(core ALIAS molaccess)

set_target_properties(molaccess PROPERTIES OUTPUT_NAME "molaccess")
set_target_properties(molaccess PROPERTIES LINKER_LANGUAGE CXX)

target_include_directories(molaccess PUBLIC include)

target_link_libraries(molaccess)

link(molaccess)

add_subdirectory(src/bindings)

install(TARGETS molaccess DESTINATION lib)
install(FILES ${HEADER_FILES} DESTINATION include/molaccess)