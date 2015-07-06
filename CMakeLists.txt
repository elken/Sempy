cmake_minimum_required(VERSION 3.1.0)
project(teaTray CXX)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTKMM gtkmm-3.0 REQUIRED)
pkg_check_modules(CURLPP curlpp REQUIRED)
pkg_check_modules(LIBNOTIFY libnotifymm-1.0 REQUIRED)

find_package(Boost REQUIRED)

include_directories(${GTKMM_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${LIBNOTIFY_INCLUDE_DIRS})

add_executable(teaTray src/index.cpp src/tray.cpp src/request.cpp)

target_link_libraries(teaTray ${GTKMM_LIBRARIES} ${CURLPP_LIBRARIES} ${Boost_LIBRARIES} ${LIBNOTIFY_LIBRARIES})

add_custom_command(TARGET teaTray POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SOURCE_DIR}/res $<TARGET_FILE_DIR:teaTray>)

add_definitions(${GTKMM_CFLAGS_OTHER})
