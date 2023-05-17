#/*===================================================================================*/
#/*************************************************************************************/
#/**
# * @file      CMakeLists.txt
# * @brief     CMake build script
# * @details   Script to build elearcommon supporting different platforms
# * @see       https://cmake.org/cmake-tutorial
# * @author    Ashish Bajaj, ashish@elear.solutions
# * @author    Amiya Santra, amiyasantra@elear.solutions
# * @copyright Copyright (c) 2016-2019 Elear Solutions Tech Private Limited. All rights
# *            reserved.
# * @license   To any person (the "Recipient") obtaining a copy of this software and
# *            associated documentation files (the "Software"):\n
# *            All information contained in or disclosed by this software is
# *            confidential and proprietary information of Elear Solutions Tech
# *            Private Limited and all rights therein are expressly reserved.
# *            By accepting this material the recipient agrees that this material and
# *            the information contained therein is held in confidence and in trust
# *            and will NOT be used, copied, modified, merged, published, distributed,
# *            sublicensed, reproduced in whole or in part, nor its contents revealed
# *            in any manner to others without the express written permission of
# *            Elear Solutions Tech Private Limited.
# */
#/*************************************************************************************/
#/*===================================================================================*/
cmake_minimum_required(VERSION 3.1)

# Updated from CMP0015 to support ios
cmake_policy(SET CMP0042 NEW)

# Define the project name
project(mbedtls)

# conan support for cross compilation
if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  conan_basic_setup()
endif()

# Set default platform to linux if none was specified
if(NOT DEFINED Platform)
  set(Platform "Linux" CACHE STRING "Linux")
  message( STATUS "Target platform: " ${Platform} )
endif()

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(WARNING "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release")
endif()
message(WARNING "Build type is set to: " ${CMAKE_BUILD_TYPE})

# Set global compilation flags at project level
# CMAKE_BUILD_TYPE implicitly adds the following options:
#     Release: -O3 -DNDEBUG
#     Debug: -g
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pedantic-errors -Wall -D_GNU_SOURCE -Os -fPIC")

if(NOT ${Platform} STREQUAL "Linux")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wgnu-zero-variadic-macro-arguments")
endif()
if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
  if(CMAKE_C_COMPILER_VERSION VERSION_LESS "4.9.0.0")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99")
  else()
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c11")
  endif()
else()
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c11")
endif()

# The following file GLOB command will search for all files within the current
# directory that match the specified expressions (*.c and *.h), and assign the
# resulting files to the variable SRCS. SRCS is a list of all C source and
# header files in the current directory.

file(GLOB CONFIG configs/*.c configs/*.h)
file(GLOB INCLUDE_MBEDTLS include/mbedtls/*.c include/mbedtls/*.h)
file(GLOB INCLUDE_PSA include/psa/*.c include/psa/*.h)
file(GLOB LIB_FILE library/*.c library/*.h)

include_directories(${PROJECT_SOURCE_DIR}/)
include_directories(${PROJECT_SOURCE_DIR}/include/)
include_directories(${PROJECT_SOURCE_DIR}/include/mbedtls/)
include_directories(${PROJECT_SOURCE_DIR}/library/)
include_directories(${PROJECT_SOURCE_DIR}/3rdparty/everest/include/)
include_directories(${PROJECT_SOURCE_DIR}/3rdparty/everest/include/everest/)

# Specify the libraries to be linked dynamically without conan
add_library(mbedtls SHARED ${CONFIG} ${INCLUDE_MBEDTLS} ${INCLUDE_PSA} ${LIB_FILE})
add_library(mbedtls_static STATIC ${CONFIG} ${INCLUDE_MBEDTLS} ${INCLUDE_PSA} ${LIB_FILE})

find_package(Threads REQUIRED)

# Specify the libraries to be linked dynamically
target_link_libraries(mbedtls m)
target_link_libraries(mbedtls Threads::Threads)

# Install library and header files
install (TARGETS mbedtls DESTINATION lib)
install (TARGETS mbedtls_static DESTINATION lib)
# todo: don't include *.c files in include
install (FILES ${INCLUDE_MBEDTLS} DESTINATION include/mbedtls)

# ------------------------- Begin Generic CMake Variable Logging ------------------

# if you are building in-source, this is the same as CMAKE_SOURCE_DIR, otherwise
# this is the top level directory of your build tree
message( STATUS "CMAKE_BINARY_DIR:         " ${CMAKE_BINARY_DIR} )

# if you are building in-source, this is the same as CMAKE_CURRENT_SOURCE_DIR, otherwise this
# is the directory where the compiled or generated files from the current CMakeLists.txt will go to
message( STATUS "CMAKE_CURRENT_BINARY_DIR: " ${CMAKE_CURRENT_BINARY_DIR} )

# this is the directory, from which cmake was started, i.e. the top level source directory
message( STATUS "CMAKE_SOURCE_DIR:         " ${CMAKE_SOURCE_DIR} )

# this is the directory where the currently processed CMakeLists.txt is located in
message( STATUS "CMAKE_CURRENT_SOURCE_DIR: " ${CMAKE_CURRENT_SOURCE_DIR} )

# contains the full path to the top level directory of your build tree
message( STATUS "PROJECT_BINARY_DIR: " ${PROJECT_BINARY_DIR} )

# contains the full path to the root of your project source directory,
# i.e. to the nearest directory where CMakeLists.txt contains the PROJECT() command
message( STATUS "PROJECT_SOURCE_DIR: " ${PROJECT_SOURCE_DIR} )

# set this variable to specify a common place where CMake should put all executable files
# (instead of CMAKE_CURRENT_BINARY_DIR)
message( STATUS "EXECUTABLE_OUTPUT_PATH: " ${EXECUTABLE_OUTPUT_PATH} )

# set this variable to specify a common place where CMake should put all libraries
# (instead of CMAKE_CURRENT_BINARY_DIR)
message( STATUS "LIBRARY_OUTPUT_PATH:     " ${LIBRARY_OUTPUT_PATH} )

# tell CMake to search first in directories listed in CMAKE_MODULE_PATH
# when you use FIND_PACKAGE() or INCLUDE()
message( STATUS "CMAKE_MODULE_PATH: " ${CMAKE_MODULE_PATH} )

# this is the complete path of the cmake which runs currently (e.g. /usr/local/bin/cmake)
message( STATUS "CMAKE_COMMAND: " ${CMAKE_COMMAND} )

# this is the CMake installation directory
message( STATUS "CMAKE_ROOT: " ${CMAKE_ROOT} )

# this is the filename including the complete path of the file where this variable is used.
message( STATUS "CMAKE_CURRENT_LIST_FILE: " ${CMAKE_CURRENT_LIST_FILE} )

# this is linenumber where the variable is used
message( STATUS "CMAKE_CURRENT_LIST_LINE: " ${CMAKE_CURRENT_LIST_LINE} )

# this is used when searching for include files e.g. using the FIND_PATH() command.
message( STATUS "CMAKE_INCLUDE_PATH: " ${CMAKE_INCLUDE_PATH} )

# this is used when searching for libraries e.g. using the FIND_LIBRARY() command.
message( STATUS "CMAKE_LIBRARY_PATH: " ${CMAKE_LIBRARY_PATH} )

# the complete system name, e.g. "Linux-2.4.22", "FreeBSD-5.4-RELEASE" or "Windows 5.1"
message( STATUS "CMAKE_SYSTEM: " ${CMAKE_SYSTEM} )

# the short system name, e.g. "Linux", "FreeBSD" or "Windows"
message( STATUS "CMAKE_SYSTEM_NAME: " ${CMAKE_SYSTEM_NAME} )

# only the version part of CMAKE_SYSTEM
message( STATUS "CMAKE_SYSTEM_VERSION: " ${CMAKE_SYSTEM_VERSION} )

# the processor name (e.g. "Intel(R) Pentium(R) M processor 2.00GHz")
message( STATUS "CMAKE_SYSTEM_PROCESSOR: " ${CMAKE_SYSTEM_PROCESSOR} )

# is TRUE on all UNIX-like OS's, including Apple OS X and CygWin
message( STATUS "UNIX: " ${UNIX} )

# is TRUE on Windows, including CygWin
message( STATUS "WIN32: " ${WIN32} )

# is TRUE on Apple OS X
message( STATUS "APPLE: " ${APPLE} )

# is TRUE when using the MinGW compiler in Windows
message( STATUS "MINGW: " ${MINGW} )

# is TRUE on Windows when using the CygWin version of cmake
message( STATUS "CYGWIN: " ${CYGWIN} )

# is TRUE on Windows when using a Borland compiler
message( STATUS "BORLAND: " ${BORLAND} )

# Microsoft compiler
message( STATUS "MSVC: " ${MSVC} )
message( STATUS "MSVC_IDE: " ${MSVC_IDE} )
message( STATUS "MSVC60: " ${MSVC60} )
message( STATUS "MSVC70: " ${MSVC70} )
message( STATUS "MSVC71: " ${MSVC71} )
message( STATUS "MSVC80: " ${MSVC80} )
message( STATUS "CMAKE_COMPILER_2005: " ${CMAKE_COMPILER_2005} )


# set this to true if you don't want to rebuild the object files if the rules have changed,
# but not the actual source files or headers (e.g. if you changed the some compiler switches)
message( STATUS "CMAKE_SKIP_RULE_DEPENDENCY: " ${CMAKE_SKIP_RULE_DEPENDENCY} )

# since CMake 2.1 the install rule depends on all, i.e. everything will be built before installing.
# If you don't like this, set this one to true.
message( STATUS "CMAKE_SKIP_INSTALL_ALL_DEPENDENCY: " ${CMAKE_SKIP_INSTALL_ALL_DEPENDENCY} )

# If set, runtime paths are not added when using shared libraries. Default it is set to OFF
message( STATUS "CMAKE_SKIP_RPATH: " ${CMAKE_SKIP_RPATH} )

# set this to true if you are using makefiles and want to see the full compile and link
# commands instead of only the shortened ones
message( STATUS "CMAKE_VERBOSE_MAKEFILE: " ${CMAKE_VERBOSE_MAKEFILE} )

# this will cause CMake to not put in the rules that re-run CMake. This might be useful if
# you want to use the generated build files on another machine.
message( STATUS "CMAKE_SUPPRESS_REGENERATION: " ${CMAKE_SUPPRESS_REGENERATION} )


# A simple way to get switches to the compiler is to use add_definitions().
# But there are also two variables exactly for this purpose:

# the compiler flags for compiling C sources
message( STATUS "CMAKE_C_FLAGS: " ${CMAKE_C_FLAGS} )

# the compiler flags for compiling C++ sources
message( STATUS "CMAKE_CXX_FLAGS: " ${CMAKE_CXX_FLAGS} )


# Choose the type of build.  Example: SET(CMAKE_BUILD_TYPE Debug)
message( STATUS "CMAKE_BUILD_TYPE: " ${CMAKE_BUILD_TYPE} )

# if this is set to ON, then all libraries are built as shared libraries by default.
message( STATUS "BUILD_SHARED_LIBS: " ${BUILD_SHARED_LIBS} )

# the compiler used for C files
message( STATUS "CMAKE_C_COMPILER: " ${CMAKE_C_COMPILER} )

# the compiler used for C++ files
message( STATUS "CMAKE_CXX_COMPILER: " ${CMAKE_CXX_COMPILER} )

# if the compiler is a variant of gcc, this should be set to 1
message( STATUS "CMAKE_COMPILER_IS_GNUCC: " ${CMAKE_COMPILER_IS_GNUCC} )

# if the compiler is a variant of g++, this should be set to 1
message( STATUS "CMAKE_COMPILER_IS_GNUCXX : " ${CMAKE_COMPILER_IS_GNUCXX} )

# the tools for creating libraries
message( STATUS "CMAKE_AR: " ${CMAKE_AR} )
message( STATUS "CMAKE_RANLIB: " ${CMAKE_RANLIB} )

#
#message( STATUS ": " ${} )

# ------------------------- End of Generic CMake Variable Logging ------------------
