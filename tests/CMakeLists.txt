add_executable(route route/src/main.cpp)
add_executable(sanity sanity/src/main.cpp)

target_link_libraries(route molaccess)

link(route)
link(sanity)
