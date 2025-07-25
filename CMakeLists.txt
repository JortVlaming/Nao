cmake_minimum_required(VERSION 3.14)
project(_nao VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(BUILD_TESTING OFF CACHE BOOL "Disable testing" FORCE)

add_subdirectory(extern/pybind11)

if(NOT QI_SDK_PATH)
    message(NOTICE "attempting to identify qi directory")
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

message(NOTICE "qi directory identified as ${QI_SDK_PATH}")

include_directories("${QI_SDK_PATH}/include")
link_directories("${QI_SDK_PATH}/lib")

pybind11_add_module(_nao_bindings src/main.cpp src/robot.cpp)
target_compile_definitions(_nao_bindings PRIVATE _GLIBCXX_USE_CXX11_ABI=0)

target_link_libraries(_nao_bindings
        PRIVATE
        qi
)


target_include_directories(_nao_bindings PRIVATE
        extern/libqi
)

target_include_directories(_nao_bindings PRIVATE "${QI_SDK_PATH}/include")
target_link_directories(_nao_bindings PRIVATE "${QI_SDK_PATH}/lib")

execute_process(
        COMMAND "${PYTHON_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
        OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(NOTICE "site-packages: ${PYTHON_SITE_PACKAGES}")
message(NOTICE "so place: ${PYTHON_SITE_PACKAGES}/nao")

install(TARGETS _nao_bindings
        LIBRARY DESTINATION "${PYTHON_SITE_PACKAGES}/nao"
)

