GRID=${GRID_DIR}
PREFIX=${GRID_DIR}/grid_prefix

CXX = hipcc 

CXXFLAGS=-O3 -fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -I/${PREFIX}/include -g -I${GRID}/Grid -I/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/ -I${OLCF_GMP_ROOT}/include -I/opt/cray/pe/gcc/mpfr/3.1.4/include -fopenmp --amdgpu-target=gfx90a -I${PREFIX}/include/Grid  -I/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/fftw-3.3.9-3hxcnpeqmrvidsb3erk36wi75kexaznd/include

LDFLAGS=-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lmpi_gtl_hsa -lamdhip64  -g -L/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/gperftools-2.9.1-72ubwtuc5wcz2meqltbfdb76epufgzo2//lib -ltcmalloc -L${PREFIX}/lib  -L${OLCF_GMP_ROOT}/lib -L/opt/cray/pe/gcc/mpfr/3.1.4/lib -L /autofs/nccs-svm1_home1/ckelly/install/LIME/lib -L${OLCF_HDF5_ROOT}/lib -L/opt/cray/pe/fftw/3.3.10.1/x86_trento/lib

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
