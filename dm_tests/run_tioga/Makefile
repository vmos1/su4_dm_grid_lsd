PREFIX=/usr/WS2/lsd/ayyar1/projects/SU4_sdm/Grid_builds/2022_nov15_tioga/grid_prefix
GRID=/usr/WS2/lsd/ayyar1/projects/SU4_sdm/Grid_builds/2022_nov15_tioga

CXX = hipcc 
#LDFLAGS = -L$(PREFIX)/lib/ -L$(GRID)/Grid/build-Nc3/Grid/ -Xcompiler -fopenmp
#CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g -I${GRID}/Grid -I${PWD}/../Grid/ -I/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz/include -I/opt/cray/pe/gcc/mpfr/3.1.4/include -Xpreprocessor -fopenmp

CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g -I${GRID}/Grid -fopenmp --amdgpu-target=gfx90a -I${PREFIX}/include/Grid -I${GRID}/install/build_Nc4/Grid/ -I${GRID}/install/build-Nc4/Grid -D HAVE_LIME -I${PREFIX}/lime-1.3.2/include

LDFLAGS=-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa -lamdhip64  -g -ltcmalloc -L${PREFIX}/lib  -L/opt/cray/pe/gcc/mpfr/3.1.4/lib -L $prefix/lime-1.3.2/lib -L${GRID}/install/build-Nc4/Grid

LIBS = -lhdf5_cpp -lz -lcrypto -llime -lfftw3f -lfftw3 -lmpfr -lgmp -lstdc++ -lm  -lcuda -lz -lhdf5 -lGrid -lomp

SRC=$(wildcard *.cc)
BIN=$(basename $(SRC))

#.PRECIOUS: hmc_SDM.o
.PHONY: clean

all: $(BIN)

%: %.cc
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(LIBS) $< -o $@

clean:
	$(RM) -r $(BIN)
