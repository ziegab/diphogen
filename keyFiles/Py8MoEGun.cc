#include "GeneratorInterface/Core/interface/GeneratorFilter.h"
#include "GeneratorInterface/ExternalDecays/interface/ExternalDecayDriver.h"

#include "GeneratorInterface/Pythia8Interface/interface/Py8GunBase.h"

// EvtGen plugin
//
#include "Pythia8Plugins/EvtGen.h"

namespace gen {

class Py8MoEGun : public Py8GunBase {
   
   public:
      
      Py8MoEGun( edm::ParameterSet const& );
      ~Py8MoEGun() {}
	 
      bool generatePartonsAndHadronize() override;
      const char* classname() const override;
	 
   private:
      
      // EGun particle(s) characteristics
      double  fMinEta;
      double  fMaxEta;
      double  fMinE ;
      double  fMaxE ;
      double  fMinMoE ;
      double  fMaxMoE ;
      bool    fAddAntiParticle;

};

// implementation 
//
Py8MoEGun::Py8MoEGun( edm::ParameterSet const& ps )
   : Py8GunBase(ps) 
{

   // ParameterSet defpset ;
   edm::ParameterSet pgun_params = 
      ps.getParameter<edm::ParameterSet>("PGunParameters"); // , defpset ) ;
   fMinEta     = pgun_params.getParameter<double>("MinEta"); // ,-2.2);
   fMaxEta     = pgun_params.getParameter<double>("MaxEta"); // , 2.2);
   fMinE       = pgun_params.getParameter<double>("MinE"); // ,  0.);
   fMaxE       = pgun_params.getParameter<double>("MaxE"); // ,  0.);
   fMinMoE     = pgun_params.getParameter<double>("MinMoE"); // ,  0.);
   fMaxMoE     = pgun_params.getParameter<double>("MaxMoE"); // ,  0.);
   fAddAntiParticle = pgun_params.getParameter<bool>("AddAntiParticle"); //, false) ;  

}

bool Py8MoEGun::generatePartonsAndHadronize()
{

   fMasterGen->event.reset();
   
   for ( size_t i=0; i<fPartIDs.size(); i++ )
   {

      int particleID = fPartIDs[i]; // this is PDG - need to convert to Py8 ???

      double phi = (fMaxPhi-fMinPhi) * randomEngine().flat() + fMinPhi;
      double ee   = (fMaxE-fMinE) * randomEngine().flat() + fMinE;
      double MoE   = (fMaxMoE-fMinMoE) * randomEngine().flat() + fMinMoE;
      double eta  = (fMaxEta-fMinEta) * randomEngine().flat() + fMinEta;
      double the  = 2.*atan(exp(-eta));

      // double mass = (fMasterGen->particleData).m0( particleID );
      // double MoE = mass / ee;
      double mass = MoE * ee;

      double pp = sqrt( ee*ee - mass*mass );
      double px = pp * sin(the) * cos(phi);
      double py = pp * sin(the) * sin(phi);
      double pz = pp * cos(the);

      if ( !((fMasterGen->particleData).isParticle( particleID )) )
      {
         particleID = std::fabs(particleID) ;
      }
      (fMasterGen->event).append( particleID, 1, 0, 0, px, py, pz, ee, mass ); 

// Here also need to add anti-particle (if any)
// otherwise just add a 2nd particle of the same type 
// (for example, gamma)
//
      if ( fAddAntiParticle )
      {
         if ( (fMasterGen->particleData).isParticle( -particleID ) )
	 {
	    (fMasterGen->event).append( -particleID, 1, 0, 0, -px, -py, -pz, ee, mass );
	 }
	 else
	 {
	    (fMasterGen->event).append( particleID, 1, 0, 0, -px, -py, -pz, ee, mass );
	 }
      }

   }
   
   if ( !fMasterGen->next() ) return false;
   
   if (evtgenDecays.get()) evtgenDecays->decay();

   event().reset(new HepMC::GenEvent);
   return toHepMC.fill_next_event( fMasterGen->event, event().get() );
  
}

const char* Py8MoEGun::classname() const
{
   return "Py8MoEGun"; 
}

typedef edm::GeneratorFilter<gen::Py8MoEGun, gen::ExternalDecayDriver> Pythia8MoEGun;

} // end namespace

using gen::Pythia8MoEGun;
DEFINE_FWK_MODULE(Pythia8MoEGun);
