set(HEADER_FILES
    include/molecular-daemon.hpp
)

set(SOURCE_FILES
    src/molecular-daemon.cpp
)

set(MAIN src/main.cpp)

add_executable(molaccessd ${HEADER_FILES} ${SOURCE_FILES} ${MAIN})

target_include_directories(molaccessd PUBLIC include)

link(molaccessd)