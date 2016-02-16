CXX=c++
CXXFLAGS=-Wall -O3

all: eigen.o

clean:
	rm -f *.o

.cpp.o:
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

.SUFFIXES: .cpp .o

.PHONY: all clean
