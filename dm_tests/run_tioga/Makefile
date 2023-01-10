PREFIX=$$GRID_DIR/grid_prefix
CXX = hipcc 

CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g -fopenmp --amdgpu-target=gfx90a -D HAVE_LIME  -I${PREFIX}/include

LDFLAGS=-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa -lamdhip64  -g -ltcmalloc -L${PREFIX}/lib  -L/opt/cray/pe/gcc/mpfr/3.1.4/lib

LIBS = -lhdf5_cpp -lz -lcrypto -llime -lfftw3f -lfftw3 -lmpfr -lgmp -lstdc++ -lm  -lcuda -lz -lhdf5 -lGrid -lomp

SRC=$(wildcard *.cc)
BIN=$(basename $(SRC))

#.PRECIOUS: hmc_SDM.o
.PHONY: clean

all: $(BIN)

%: %.cc
	echo $(PREFIX)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(LIBS) $< -o $@

clean:
	$(RM) -r $(BIN)
