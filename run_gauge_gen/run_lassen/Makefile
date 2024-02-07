PREFIX=$$GRID_DIR/grid_prefix

CXX = nvcc 
MPICXX=mpicxx

CXXFLAGS=-O3 -std=c++14 -I${MPICH_DIR}/include  -g -D HAVE_LIME  -I${PREFIX}/include --extended-lambda -Xcompiler -fopenmp

LDFLAGS=-L${MPICH_DIR}/lib -L${CRAY_MPICH_ROOTDIR}/gtl/lib -ltcmalloc -L${PREFIX}/lib -Xcompiler -fopenmp

LIBS = -lhdf5_cpp -lz -lcrypto -llime -lfftw3f -lfftw3 -lmpfr -lgmp -lstdc++ -lm  -lcuda -lz -lhdf5 -lGrid 

SRC=$(wildcard *.cu)
BIN=$(basename $(SRC))

#.PRECIOUS: hmc_SDM.o
.PHONY: clean

all: $(BIN)

%: %.cu
	echo $(PREFIX)
	$(CXX) -ccbin $(MPICXX) -Xcompiler $(CXXFLAGS) $(LDFLAGS) $(LIBS) $< -o $@

clean:
	$(RM) -r $(BIN)
