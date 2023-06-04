CXX = g++
PYTHON = python3
CXXFLAGS = -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -fPIC $(shell python3 -m pybind11 --includes)

TARGET = algorithm.so
SRC = algorithm.cpp
INTERFACE = interface.py
FILE_EAR_CMD = file ear
FILE_OPT_CMD = file opt

.PHONY: all run file_ear file_opt clean 

all:
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
	$(PYTHON) $(INTERFACE)

run:
	$(PYTHON) $(INTERFACE)

file_ear:
	$(PYTHON) $(INTERFACE) $(FILE_EAR_CMD)

file_opt:
	$(PYTHON) $(INTERFACE) $(FILE_OPT_CMD)

clean:
	rm -f $(TARGET)
	rm -rf __pycache__