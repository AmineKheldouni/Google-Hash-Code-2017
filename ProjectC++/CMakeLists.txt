cmake_minimum_required(VERSION 3.6)
project(QualifRound)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp Piece.cpp Piece.h inputs.cpp inputs.h)
add_executable(QualifRound ${SOURCE_FILES})