set(HEADER_FILES
    include/molecular-daemon.hpp
)

set(SOURCE_FILES
    src/molecular-daemon.cpp
)

set(MAIN src/main.cpp)

add_library(molaccess ${HEADER_FILES} ${SOURCE_FILES})

target_include_directories(molaccess PUBLIC include)

link(molaccess)