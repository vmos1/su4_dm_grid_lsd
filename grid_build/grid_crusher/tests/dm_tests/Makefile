#PREFIX=$(HOME)/GridSU4/prefix
#GRID=$(HOME)/GridSU4/GridCompile
PREFIX=/autofs/nccs-svm1_home1/ckelly/install/Grid_develop_crusher
GRID=/gpfs/alpine/lgt104/proj-shared/ayyar/LSD_projects/build_LSD_grid/install_oct7_2022

#CXX = nvcc -x cu
CXX = hipcc 
#CXXFLAGS = -O3 -ccbin mpicxx -gencode arch=compute_70,code=sm_70 -I$(PREFIX)/include/ -I$(GRID)/Grid/ -I$(GRID)/install/build-Nc4/Grid/ -std=c++11 -Xcompiler -fno-strict-aliasing --expt-extended-lambda --expt-relaxed-constexpr
#LDFLAGS = -L$(PREFIX)/lib/ -L$(GRID)/Grid/build-Nc3/Grid/ -Xcompiler -fopenmp


#CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g -I${GRID}/Grid -I${PWD}/../Grid/ -I/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz/include -I/opt/cray/pe/gcc/mpfr/3.1.4/include -Xpreprocessor -fopenmp

CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g -I${GRID}/Grid -I/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz/include -I/opt/cray/pe/gcc/mpfr/3.1.4/include -fopenmp --amdgpu-target=gfx90a -I${PREFIX}/include/Grid -I${PWD}/../../Grid/

LDFLAGS=-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa -lamdhip64  -g -L/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/gperftools-2.9.1-72ubwtuc5wcz2meqltbfdb76epufgzo2//lib -ltcmalloc -L${PREFIX}/lib  -L/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz/lib -L/opt/cray/pe/gcc/mpfr/3.1.4/lib -L /autofs/nccs-svm1_home1/ckelly/install/LIME/lib -L/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/hdf5-1.12.1-duogocgjuszctn4kw6he2vgus5kcedxl/lib -L/opt/cray/pe/fftw/3.3.10.1/x86_trento/lib -I${PWD}/../../Grid/

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
