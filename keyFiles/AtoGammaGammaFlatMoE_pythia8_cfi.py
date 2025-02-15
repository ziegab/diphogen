import FWCore.ParameterSet.Config as cms

aMass = 999

eMin = 250
eMax = 2500
moeMin = 0.01
moeMax = 0.1

generator = cms.EDFilter("Pythia8MoEGun",
    PGunParameters = cms.PSet(
        AddAntiParticle = cms.bool(False),
        
        ParticleID = cms.vint32(25),

        MinE = cms.double(eMin),
        MaxE = cms.double(eMax),

        MinMoE = cms.double(moeMin),
        MaxMoE = cms.double(moeMax),

        MinEta = cms.double(-1.4),
        MaxEta = cms.double(1.4),

        MinPhi = cms.double(-3.14159265359),
        MaxPhi = cms.double(3.14159265359)
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('pythia8_mycmd'),
        pythia8_mycmd = cms.vstring('Higgs:useBSM = off', 
            'HiggsBSM:allH2 = offHiggsBSM:gg2H2 = off', 
            'HiggsBSM:ffbar2H2 =off', 
            'HiggsBSM:gmgm2H2=off', 
            'HiggsBSM:ffbar2H2Z=off', 
            'HiggsBSM:ffbar2H2W=off', 
            'HiggsBSM:ff2H2ff(t:ZZ)=off', 
            'HiggsBSM:ff2H2ff(t:WW)=off', 
            'HiggsBSM:gg2H2ttbar=off', 
            'HiggsBSM:qqbar2H2ttbar=off', 
            '25:m0        = {}'.format(aMass), 
            '25:mMin      = {}'.format(aMass-0.1), 
            '25:mMax      = {}'.format(aMass+0.1),
            '25:mWidth    = 0.01', 
            '25:tau0      = 025:0:bRatio  = 0.0', 
            '25:1:bRatio  = 0.0', 
            '25:2:bRatio  = 0.000', 
            '25:3:bRatio  = 0.00', 
            '25:4:bRatio  = 0.0', 
            '25:5:bRatio  = 0.0', 
            '25:6:bRatio  = 0.0', 
            '25:7:bRatio  = 0.000', 
            '25:8:bRatio  = 0.0', 
            '25:9:bRatio  = 0.0', 
            '25:10:bRatio = 1.00', 
            '25:11:bRatio = 0.00', 
            '25:12:bRatio = 0.0', 
            '25:13:bRatio = 0.0', 
            '25:0:meMode  = 100', 
            '25:1:meMode  = 100', 
            '25:2:meMode  = 100', 
            '25:3:meMode  = 100', 
            '25:4:meMode  = 100', 
            '25:5:meMode  = 100', 
            '25:6:meMode  = 100', 
            '25:7:meMode  = 100', 
            '25:8:meMode  = 100', 
            '25:9:meMode  = 100', 
            '25:10:meMode = 100', 
            '25:11:meMode = 100', 
            '25:12:meMode = 100', 
            '25:13:meMode = 100', 
            '35:m0        = 100', 
            '35:mWidth    = 0.00403', 
            '35:0:bRatio  = 0.0', 
            '35:1:bRatio  = 0.0', 
            '35:2:bRatio  = 0.0', 
            '35:3:bRatio  = 0.0', 
            '35:4:bRatio  = 0.0', 
            '35:5:bRatio  = 0.0', 
            '35:6:bRatio  = 0.0', 
            '35:7:bRatio  = 0.0', 
            '35:8:bRatio  = 0.0', 
            '35:9:bRatio  = 0.0', 
            '35:10:bRatio  = 0.0', 
            '35:11:bRatio  = 0.0', 
            '35:12:bRatio  = 0.0', 
            '35:13:bRatio  = 0.0', 
            '35:14:bRatio  = 0.0', 
            '35:15:bRatio  = 1.0', 
            '35:16:bRatio  = 0.0', 
            '35:17:bRatio  = 0.0', 
            '35:18:bRatio  = 0.0', 
            '35:19:bRatio  = 0.0', 
            '35:20:bRatio  = 0.0', 
            '35:0:meMode  = 100', 
            '35:1:meMode  = 100', 
            '35:2:meMode  = 100', 
            '35:3:meMode  = 100', 
            '35:4:meMode  = 100', 
            '35:5:meMode  = 100', 
            '35:6:meMode  = 100', 
            '35:7:meMode  = 100', 
            '35:8:meMode  = 100', 
            '35:9:meMode  = 100', 
            '35:10:meMode = 100', 
            '35:11:meMode  = 100', 
            '35:12:meMode  = 100', 
            '35:13:meMode  = 100', 
            '35:14:meMode  = 100', 
            '35:15:meMode  = 100', 
            '35:16:meMode  = 100', 
            '35:17:meMode  = 100', 
            '35:18:meMode  = 100', 
            '35:19:meMode  = 100', 
            '35:20:meMode = 100')
    ),
    Verbosity = cms.untracked.int32(0),
    firstRun = cms.untracked.uint32(1),
    psethack = cms.string('a to gamma gamma basic')
)