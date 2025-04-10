cmake_minimum_required(VERSION 3.18)

project(BOOST_BUILD)

set(_terminal_option)
if("$ENV{THEROCK_INTERACTIVE}")
  set(_terminal_option "USES_TERMINAL")
endif()

set(_cflags "-fPIC")
set(_bootstrap_exec bash "bootstrap.sh")
if(WIN32)
  set(_cflags)
  set(_bootstrap_exec "cmd.exe" "/C" "bootstrap.bat")
endif()

add_custom_target(
  bootstrap_and_build ALL
  ${_terminal_option}
  WORKING_DIRECTORY "${BOOST_SOURCE_DIR}"
  COMMAND
    ${_bootstrap_exec} "--with-libraries=${THEROCK_BOOST_LIBRARIES}"
  COMMAND
    "${BOOST_SOURCE_DIR}/b2" "cflags=${_cflags}" link=static threading=multi
  COMMAND
    "${BOOST_SOURCE_DIR}/b2" headers
  COMMAND
    # Boost is dumb. It assumes that it's "stage" directory is one level up from
    # where the headers are. This is hard-coded in the cmake config. So we take
    # advantage of the fact that our library install location is into our stage/
    # directory, which is one level up from our build directory. There may be
    # a better way to do this... but have I said before that Boost's build is
    # bonkers?
    "${CMAKE_COMMAND}" -E create_symlink "${BOOST_SOURCE_DIR}/boost" "${CMAKE_CURRENT_BINARY_DIR}/../boost"
)

install(DIRECTORY "${BOOST_SOURCE_DIR}/stage/lib" DESTINATION ".")
