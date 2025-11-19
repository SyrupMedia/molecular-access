cmake_minimum_required(VERSION 3.14)
project(molecular-access)

set(CMAKE_BUILD_RPATH_USE_ORIGIN ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)

set(CMAKE_SHARED_LIBRARY_PREFIX "_")
set(CMAKE_STATIC_LIBRARY_PREFIX "_")

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

set(COMPILE_WARNING_AS_ERROR ON)

option(MOLACCESS_BUILD_TESTS OFF)

option(MOLACCESS_MINGW_CROSS_COMPILATION OFF)

#if(MOLACCESS_MINGW_CROSS_COMPILATION)
#    if(NOT CMAKE_GENERATOR STREQUAL "Ninja")
#        message(
#            FATAL_ERROR "Generator “${CMAKE_GENERATOR}” is unsupported!\nInstall Ninja.")
#    endif()
#    
#    set(CMAKE_TOOLCHAIN_FILE TC-mingw.cmake)
#endif()

add_compile_definitions(SWIG_PYTHON_INTERPRETER_NO_DEBUG)

add_subdirectory(libs/submodules/libipc)

get_target_property(IPC_INCLUDES ipc INCLUDE_DIRECTORIES)

macro(link TARGET)
    target_link_libraries(${TARGET}
        ipc
    )

    target_include_directories(${TARGET} PUBLIC ${IPC_INCLUDES} core/include)
endmacro()

add_subdirectory(core)

if(MOLACCESS_BUILD_TESTS)
    add_subdirectory(tests)
endif()