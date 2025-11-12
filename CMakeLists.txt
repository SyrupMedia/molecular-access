cmake_minimum_required(VERSION 3.14)
project(molecular-access)

add_subdirectory(libs/submodules/libipc)

get_target_property(IPC_INCLUDES ipc INCLUDE_DIRECTORIES)

macro(link TARGET)
    target_link_libraries(${TARGET}
        ipc 
    )

    target_include_directories(${TARGET} PUBLIC ${IPC_INCLUDES})    
endmacro()

add_subdirectory(daemon)
add_subdirectory(client)
