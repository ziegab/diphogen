#!/bin/bash

#Generates events for a given gridpack
source /cvmfs/cms.cern.ch/cmsset_default.sh 
export SCRAM_ARCH=slc7_amd64_gcc700

n_events=10
releasedir=/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tools/AtoGG
tmpdir=/tmp/gziemyt2/DiphotonGun
outpath=/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tempstore/1krun2events/AtoGG_10events0p05Ma0p01_51p0EPileup_MiniAOD.root
saveAOD=True
aMass=0.05
Emin=0.01
Emax=51.0
aMassErr=0.001

outputdir=$(dirname "$outpath")
echo "$outputdir"
if [ ! -d "$outputdir" ]
then
  echo "Output directory does not exist, exiting."
  exit 1
fi

outfilename=$(basename "$outpath")
jobname=${outfilename%.*}

echo "Running event generation for $jobname"
echo "Output file name: $outfilename"

wkdir=$tmpdir/$jobname
echo "Working directory: $wkdir"
cd $tmpdir
if [ -d $wkdir ]
then
  echo "Removing existing temporary directory."
  rm -rf $wkdir
  mkdir $wkdir
else
  echo "Creating temporary directory"
  mkdir $wkdir
fi

#### File I/O
DIGI2RAWfilepath=${wkdir}/DIGI2RAW.root
HLTfilepath=${wkdir}/HLTPU.root
RECOfilepath=${wkdir}/RECO.root
MINIfilepath=${wkdir}/MINI.root

DIGI2RAW=$releasedir/CMSSW_10_6_17_patch1/src
HLT=$releasedir/CMSSW_10_2_16_UL/src
RECO=$releasedir/CMSSW_10_6_17_patch1/src
MINI=$releasedir/CMSSW_10_6_27/src

echo "Starting Gen to MiniAOD steps"

echo "DIGI2RAW step"
cd $DIGI2RAW
eval `scramv1 runtime -sh`
cmsRun AtoGammaGamma_MoverE_pythia8_DIGI2RAWv2.py $n_events $DIGI2RAWfilepath $aMass $Emin $Emax $aMassErr

# Check exit status
if [ $? -ne 0 ]
then
  echo "GEN step failed with exit code $?, exiting."
  exit 1
fi

echo "HLT step"
cd $HLT
eval `scramv1 runtime -sh`
cmsRun AtoGammaGamma_MoverE_pythia8_HLT.py $DIGI2RAWfilepath $HLTfilepath

echo "RECO step"
cd $RECO
eval `scramv1 runtime -sh`
cmsRun AtoGammaGamma_MoverE_pythia8_AOD.py $HLTfilepath $RECOfilepath

if [ $saveAOD == "True" ]
then
  # Replace MiniAOD in outpath with AOD
  outMinifilepath=${outpath//MiniAOD/AOD}
  cp $RECOfilepath $outMinifilepath
fi

echo "MiniAOD step"
cd $MINI
eval `scramv1 runtime -sh` 
cmsRun AtoGammaGamma_MoverE_pythia8_MiniAODv2.py $RECOfilepath $MINIfilepath


echo "Done generating events for $jobname"
echo "Moving output file to hadoop"
mv $MINIfilepath $outpath

echo "Cleaning up, removing temporary directory"
rm -rf $wkdir
