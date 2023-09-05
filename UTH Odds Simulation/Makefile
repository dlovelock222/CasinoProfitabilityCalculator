uth: uthSim.o helperFunctions.o
	g++ uthSim.o helperFunctions.o -o uth

uthSim.o: uthSim.cpp
	g++ -c uthSim.cpp

helperFunctions.o: helperFunctions.cpp helperFunctions.h
	g++ -c helperFunctions.cpp

clean:
	rm -f uth