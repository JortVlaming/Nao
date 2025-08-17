cmake_minimum_required(VERSION 3.14)
project(_nao VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(BUILD_TESTING OFF CACHE BOOL "Disable testing" FORCE)

# --- pybind11 ---
add_subdirectory(extern/pybind11)

# --- NAOqi SDK path ---
# Allow user to pass -DQI_SDK_PATH=... or fallback to defaults
if(NOT QI_SDK_PATH AND DEFINED ENV{QI_SDK_PATH})
    message(NOTICE "Taking QI SDK path from environment")
    set(QI_SDK_PATH $ENV{QI_SDK_PATH})
endif()

if(NOT QI_SDK_PATH)
    message(NOTICE "attempting to auto detect QI SDK")
    if(UNIX AND NOT APPLE)
        set(QI_SDK_PATH "/opt/naoqi-sdk")
    elseif(APPLE)
        set(QI_SDK_PATH "/usr/local/naoqi-sdk")
    elseif(WIN32)
        set(QI_SDK_PATH "C:/Program Files/naoqi-sdk")
    else()
        message(FATAL_ERROR "Please set QI_SDK_PATH (e.g. -DQI_SDK_PATH=/opt/naoqi-sdk)")
    endif()
endif()

# --- find NAOqi headers and library ---
find_path(QI_INCLUDE_DIR
        NAMES qi/session.hpp
        HINTS ${QI_SDK_PATH}
        PATH_SUFFIXES include
)

find_library(QI_LIBRARY
        NAMES qi
        HINTS ${QI_SDK_PATH}
        PATH_SUFFIXES lib
)

if(NOT QI_INCLUDE_DIR OR NOT QI_LIBRARY)
    message(FATAL_ERROR "Could not find NAOqi SDK under ${QI_SDK_PATH}")
endif()

message(STATUS "Found NAOqi headers in: ${QI_INCLUDE_DIR}")
message(STATUS "Found NAOqi library: ${QI_LIBRARY}")

# --- pybind11 module ---
file(GLOB_RECURSE NAO_SRC CONFIGURE_DEPENDS src/*.cpp)

pybind11_add_module(_nao_bindings ${NAO_SRC})
target_compile_definitions(_nao_bindings PRIVATE _GLIBCXX_USE_CXX11_ABI=0)

target_include_directories(_nao_bindings PRIVATE
        ${QI_INCLUDE_DIR}
        extern/libqi
)

target_link_libraries(_nao_bindings PRIVATE ${QI_LIBRARY})

# --- Install to Python site-packages ---
execute_process(
        COMMAND "${PYTHON_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
        OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "Python site-packages: ${PYTHON_SITE_PACKAGES}")

install(TARGETS _nao_bindings
        LIBRARY DESTINATION "${PYTHON_SITE_PACKAGES}/nao"   # Unix-like shared libs
        ARCHIVE DESTINATION "${PYTHON_SITE_PACKAGES}/nao"   # Static libs
        RUNTIME DESTINATION "${PYTHON_SITE_PACKAGES}/nao"   # Windows DLLs
)
