cmake_minimum_required(VERSION 3.14)
project(_nao VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(BUILD_TESTING OFF CACHE BOOL "Disable testing" FORCE)

add_subdirectory(extern/pybind11)

if(!QI_SDK_PATH)
if(WIN32)
    set(QI_SDK_PATH "C:/Program Files/naoqi-sdk")
    message(NOTICE "Platform identified as windows")
elseif(APPLE)
    set(QI_SDK_PATH "/usr/local/naoqi-sdk")
    message(NOTICE "Platform identified as macos")
elseif(UNIX)
    set(QI_SDK_PATH "/opt/naoqi-sdk")
    message(NOTICE "Platform identified as linux")
else()
    message(FATAL_ERROR "Unsupported platform (linux, windows, apple")
endif()
endif()

include_directories("${QI_SDK}/include")
link_directories("${QI_SDK}/lib")

pybind11_add_module(_nao_bindings src/main.cpp src/robot.cpp)

target_include_directories(_nao_bindings PRIVATE
        extern/libqi
)

target_link_libraries(_nao_bindings PRIVATE qi)

install(TARGETS _nao_bindings
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/nao
)

