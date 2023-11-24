/*************************************************************************************

Grid physics library, www.github.com/paboyle/Grid

Source file: ./tests/Test_hmc_EODWFRatio.cc

Copyright (C) 2015-2016

Author: Peter Boyle <pabobyle@ph.ed.ac.uk>
Author: Guido Cossu <guido.cossu@ed.ac.uk>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

See the full license in the file "LICENSE" in the top level distribution
directory
*************************************************************************************/
/*  END LEGAL */
#include <Grid/Grid.h>

namespace Grid{
  struct FermionParameters: Serializable {
    GRID_SERIALIZABLE_CLASS_MEMBERS(FermionParameters,
				    int, Ls,
				    double, mass,
				    double, M5,
				    double, b,
				    double, c,
				    double, StoppingCondition,
				    int, MaxCGIterations,
				    bool, ApplySmearing);

    //template <class ReaderClass >
    //FermionParameters(Reader<ReaderClass>& Reader){
    //  read(Reader, "Mobius", *this);
    //}

  };

  
  struct MobiusHMCParameters: Serializable {
  GRID_SERIALIZABLE_CLASS_MEMBERS(MobiusHMCParameters,
				  double, gauge_beta,
				  FermionParameters, Mobius)

  template <class ReaderClass >
  MobiusHMCParameters(Reader<ReaderClass>& Reader){
    read(Reader, "Action", *this);
  }

};

  struct SmearingParameters: Serializable {
    GRID_SERIALIZABLE_CLASS_MEMBERS(SmearingParameters,
				    double, rho,
				    Integer, Nsmear)

    template <class ReaderClass >
    SmearingParameters(Reader<ReaderClass>& Reader){
      read(Reader, "StoutSmearing", *this);
    }

  };
  
  
}


int main(int argc, char **argv) {
  using namespace Grid;
   ;

  Grid_init(&argc, &argv);
  int threads = GridThread::GetThreads();
  // here make a routine to print all the relevant information on the run
  std::cout << GridLogMessage << "Grid is setup to use " << threads << " threads" << std::endl;

   // Typedefs to simplify notation
  typedef GenericHMCRunner<MinimumNorm2> HMCWrapper;  // Uses the default minimum norm
  typedef WilsonImplR FermionImplPolicy;
  typedef MobiusFermionD FermionAction;
  typedef typename FermionAction::FermionField FermionField;
  // Serialiser
  typedef Grid::XmlReader       Serialiser;
  
  //::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  HMCWrapper TheHMC;
  TheHMC.ReadCommandLine(argc, argv); // these can be parameters from file
 
  // Reader, file should come from command line
  if (TheHMC.ParameterFile.empty()){
    std::cout << "Input file not specified."
              << "Use --ParameterFile option in the command line.\nAborting" 
              << std::endl;
    exit(1);
  }
  Serialiser Reader(TheHMC.ParameterFile);

  MobiusHMCParameters MyParams(Reader);  
  // Apply smearing to the fermionic action
  bool ApplySmearing = MyParams.Mobius.ApplySmearing;
  
  

  // Grid from the command line
  TheHMC.Resources.AddFourDimGrid("gauge");
  // Possibile to create the module by hand 
  // hardcoding parameters or using a Reader

  // EOFA parameters
  OneFlavourRationalParams OFRp;
  OFRp.lo       = 0.98;
  OFRp.hi       = 25.0;
  OFRp.MaxIter  = 10000;
  OFRp.tolerance= 1.0e-7;
  OFRp.degree   = 10;
  OFRp.precision= 40;
  
  // Checkpointer definition (Name: Checkpointer)
  CheckpointerParameters CPparams(Reader);
  
  TheHMC.Resources.LoadNerscCheckpointer(CPparams);
  //  TheHMC.Resources.LoadBinaryCheckpointer(CPparams);

  // RNG definition (Name: RandomNumberGenerator)
  RNGModuleParameters RNGpar(Reader);
  TheHMC.Resources.SetRNGSeeds(RNGpar);

  // Construct observables
  // Plaquette and Polyakov loop
  typedef PlaquetteMod<HMCWrapper::ImplPolicy> PlaqObs;
  TheHMC.Resources.AddObservable<PlaqObs>();
    
  typedef PolyakovMod<HMCWrapper::ImplPolicy> PolyakovObs;
  TheHMC.Resources.AddObservable<PolyakovObs>();

  /////////////////////////////////////////////////////////////
  // Collect actions, here use more encapsulation
  // need wrappers of the fermionic classes 
  // that have a complex construction
  // standard

  WilsonGaugeActionR Waction(MyParams.gauge_beta);
//   SymanzikGaugeActionR Syzaction(MyParams.gauge_beta);
    
  const int Ls   = MyParams.Mobius.Ls;
  auto GridPtr   = TheHMC.Resources.GetCartesian();
  auto GridRBPtr = TheHMC.Resources.GetRBCartesian();
  auto FGrid     = SpaceTimeGrid::makeFiveDimGrid(Ls,GridPtr);
  auto FrbGrid   = SpaceTimeGrid::makeFiveDimRedBlackGrid(Ls,GridPtr);

  // temporarily need a gauge field
  LatticeGaugeField U(GridPtr);

  Real mass = MyParams.Mobius.mass; //0.04;
  Real pv   = 1.0;
  RealD M5  = MyParams.Mobius.M5; //1.5;
  RealD b   = MyParams.Mobius.b; //  3./2.;
  RealD c   = MyParams.Mobius.c; //  1./2.;

  // These lines are unecessary if BC are all periodic
  //std::vector<Complex> boundary = {1,1,1,-1};
  //FermionAction::ImplParams Params(boundary);
  

  ConjugateGradient<FermionField>  CG(MyParams.Mobius.StoppingCondition,MyParams.Mobius.MaxCGIterations);
  // DJM: setup for EOFA ratio (Mobius)
  MobiusEOFAFermionD Strange_Op_L(U, *FGrid, *FrbGrid, *GridPtr, *GridRBPtr, mass,     mass, pv,  0.0, -1, M5, b, c);
  MobiusEOFAFermionD Strange_Op_R(U, *FGrid, *FrbGrid, *GridPtr, *GridRBPtr, pv, mass, pv, -1.0,  1, M5, b, c);
  ExactOneFlavourRatioPseudoFermionAction<FermionImplPolicy> EOFA(Strange_Op_L, Strange_Op_R, CG, OFRp, true);
    
//   FermionAction DenOp(U,*FGrid,*FrbGrid,*GridPtr,*GridRBPtr,mass,M5,b,c, Params);
//   FermionAction NumOp(U,*FGrid,*FrbGrid,*GridPtr,*GridRBPtr,pv,  M5,b,c, Params);
//   TwoFlavourEvenOddRatioPseudoFermionAction<FermionImplPolicy> Nf2a(NumOp, DenOp,CG,CG);

  // Set smearing (true/false), default: false
  EOFA.is_smeared = ApplySmearing;
  
  // Collect actions
  ActionLevel<HMCWrapper::Field> Level1(1);
  Level1.push_back(&EOFA);


  ActionLevel<HMCWrapper::Field> Level2(4);
  Level2.push_back(&Waction);
//   Level2.push_back(&Syzaction);

  TheHMC.TheAction.push_back(Level1);
  TheHMC.TheAction.push_back(Level2);

  /////////////////////////////////////////////////////////////
  // HMC parameters are serialisable
  TheHMC.Parameters.initialize(Reader);

  // Reset performance counters 

  if (ApplySmearing){
    SmearingParameters SmPar(Reader);
    //double rho = 0.1;  // smearing parameter
    //int Nsmear = 3;    // number of smearing levels
    Smear_Stout<HMCWrapper::ImplPolicy> Stout(SmPar.rho);
    SmearedConfiguration<HMCWrapper::ImplPolicy> SmearingPolicy(GridPtr, SmPar.Nsmear, Stout);
    TheHMC.Run(SmearingPolicy); // for smearing
  } else {
    TheHMC.Run();  // no smearing
  }


  Grid_finalize();
} 

