add_executable(route route/src/main.cpp)
add_executable(sanity sanity/src/main.cpp)

target_link_libraries(route molaccess)
target_link_libraries(sanity molaccess)

set_target_properties(route PROPERTIES LINKER_LANGUAGE CXX)
set_target_properties(sanity PROPERTIES LINKER_LANGUAGE CXX)

link(route)
link(sanity)

target_include_directories(route PUBLIC ${CMAKE_SOURCE_DIR}/core/include)
target_include_directories(sanity PUBLIC ${CMAKE_SOURCE_DIR}/core/include)

install(TARGETS route DESTINATION bin)
install(TARGETS sanity DESTINATION bin)