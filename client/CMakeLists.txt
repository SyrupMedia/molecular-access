set(HEADER_FILES
    include/molecular-client.hpp
)

set(SOURCE_FILES
    src/molecular-client.cpp
)

set(MAIN src/main.cpp)

add_executable(molaccess-client ${HEADER_FILES} ${SOURCE_FILES} ${MAIN})

target_include_directories(molaccess-client PUBLIC include)

link(molaccess-client)