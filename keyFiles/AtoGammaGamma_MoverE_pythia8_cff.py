import FWCore.ParameterSet.Config as cms

aMass = 10
aEnergy = 1000

generator = cms.EDFilter("Pythia8EGun",
    PGunParameters = cms.PSet(
        ParticleID = cms.vint32(25),
        AddAntiParticle = cms.bool(False),
        MaxEta = cms.double(5.2),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-5.2),
        MinE = cms.double(aEnergy-0.01),
        MinPhi = cms.double(-3.14159265359), ## in radians
        MaxE = cms.double(aEnergy+0.01)
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('pythia8_mycmd'),
        pythia8_mycmd = cms.vstring('Higgs:useBSM = off',
                                    '25:m0        = {}'.format(aMass),
                                    '25:mMin      = {}'.format(aMass-0.1),
                                    '25:mMax      = {}'.format(aMass+0.1),
                                    '25:mWidth    = 0.01',
                                    '25:onMode    = off',
                                    '25:onIfAny   = 22 22'
                                    )),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts
    psethack = cms.string('A to Gamma Gamma'),
    firstRun = cms.untracked.uint32(1)
)