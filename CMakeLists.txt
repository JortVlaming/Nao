cmake_minimum_required(VERSION 3.14)
project(_nao VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(BUILD_TESTING OFF CACHE BOOL "Disable testing" FORCE)

add_subdirectory(extern/pybind11)
add_subdirectory(extern/libqi)

pybind11_add_module(_nao_bindings src/main.cpp)

target_include_directories(_nao_bindings PRIVATE
        extern/libqi
)

target_link_libraries(_nao_bindings PRIVATE qi)

install(TARGETS _nao_bindings
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/nao
)

