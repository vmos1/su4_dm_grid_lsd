    /*************************************************************************************

    Grid physics library, www.github.com/paboyle/Grid 

    Derived from: ./tests/Test_rhmc_Wilson1p1.cc

    Copyright (C) 2015

Author: Peter Boyle <paboyle@ph.ed.ac.uk>
Author: paboyle <paboyle@ph.ed.ac.uk>

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

    See the full license in the file "LICENSE" in the top level distribution directory
    *************************************************************************************/
    /*  END LEGAL */
#include <string>
#include <Grid/Grid.h>



int main(int argc, char **argv) {

  using namespace Grid;

  // get Ls, traj_l, md_steps, beta and the fermion mass (last five command line parameters)
  int Ls = atoi(argv[argc - 5]);
  double traj_l = std::stod(argv[argc - 4]);
  int md_steps = std::stod(argv[argc - 3]);
  Real beta = std::stod(argv[argc - 2]);
  Real m_f = std::stod(argv[argc - 1]);

  argc -= 5;
 
  double pv_mass = 1.0;  // pauli-villars mass
  double M5 = 1.8;  // domain wall height
  


  Grid_init(&argc, &argv);
  int threads = GridThread::GetThreads();
  // here make a routine to print all the relevant information on the run
  std::cout << GridLogMessage << "Grid is setup to use " << threads << " threads" << std::endl;

   // Typedefs to simplify notation
  typedef GenericHMCRunner<MinimumNorm2> HMCWrapper;  // Uses the default minimum norm
  typedef WilsonImplR FermionImplPolicy;
  typedef DomainWallFermionD FermionAction;
  typedef typename FermionAction::FermionField FermionField;


  //::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  HMCWrapper TheHMC;

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

  double StoppingCondition = 1e-10;
  double MaxCGIterations = 30000;
  ConjugateGradient<LatticeFermion>  CG(StoppingCondition,MaxCGIterations);

  // Checkpointer definition
  CheckpointerParameters CPparams;  
  CPparams.config_prefix = "ckpoint_lat";
  CPparams.rng_prefix = "ckpoint_rng";
  CPparams.saveInterval = 5;
  CPparams.format = "IEEE64BIG";
  
  TheHMC.Resources.LoadNerscCheckpointer(CPparams);

  RNGModuleParameters RNGpar;
  RNGpar.serial_seeds = "1 2 3 4 5";
  RNGpar.parallel_seeds = "6 7 8 9 10";
  TheHMC.Resources.SetRNGSeeds(RNGpar);

  // Construct observables
  // Plaquette and Polyakov loop
  typedef PlaquetteMod<HMCWrapper::ImplPolicy> PlaqObs;
  TheHMC.Resources.AddObservable<PlaqObs>();
    
  typedef PolyakovMod<HMCWrapper::ImplPolicy> PolyakovObs;
  TheHMC.Resources.AddObservable<PolyakovObs>();
  //////////////////////////////////////////////

  /////////////////////////////////////////////////////////////
  // Collect actions, here use more encapsulation
  // need wrappers of the fermionic classes 
  // that have a complex construction
  // standard
  WilsonGaugeActionR Waction(beta);
    
  auto GridPtr = TheHMC.Resources.GetCartesian();
  auto GridRBPtr = TheHMC.Resources.GetRBCartesian();
  auto FGrid     = SpaceTimeGrid::makeFiveDimGrid(Ls,GridPtr);
  auto FrbGrid   = SpaceTimeGrid::makeFiveDimRedBlackGrid(Ls,GridPtr);

  // temporarily need a gauge field
  LatticeGaugeField U(GridPtr);

  // DJM: setup for EOFA ratio (Shamir)
  DomainWallEOFAFermionD Strange_Op_L(U, *FGrid, *FrbGrid, *GridPtr, *GridRBPtr, m_f,     m_f, pv_mass,  0.0, -1, M5);
  DomainWallEOFAFermionD Strange_Op_R(U, *FGrid, *FrbGrid, *GridPtr, *GridRBPtr, pv_mass, m_f, pv_mass, -1.0,  1, M5);
  ExactOneFlavourRatioPseudoFermionAction<FermionImplPolicy> EOFA(Strange_Op_L, Strange_Op_R, CG, OFRp, true);

    // Collect actions
  ActionLevel<HMCWrapper::Field> Level1(1);
  Level1.push_back(&EOFA);

  ActionLevel<HMCWrapper::Field> Level2(4);
  Level2.push_back(&Waction);

  TheHMC.TheAction.push_back(Level1);
  TheHMC.TheAction.push_back(Level2);
  /////////////////////////////////////////////////////////////

  /*
    double rho = 0.1;  // smearing parameter
    int Nsmear = 2;    // number of smearing levels
    Smear_Stout<HMCWrapper::ImplPolicy> Stout(rho);
    SmearedConfiguration<HMCWrapper::ImplPolicy> SmearingPolicy(
        UGrid, Nsmear, Stout);
  */

  // HMC parameters are serialisable 
  TheHMC.Parameters.MD.MDsteps = md_steps;
  TheHMC.Parameters.MD.trajL   = traj_l;

  TheHMC.ReadCommandLine(argc, argv); // these can be parameters from file
  TheHMC.Run();  // no smearing
  // TheHMC.Run(SmearingPolicy); // for smearing

  Grid_finalize();

} // main



