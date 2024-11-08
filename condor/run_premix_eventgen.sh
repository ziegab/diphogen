#!/bin/sh

#Generates events for a given gridpack
source /cvmfs/cms.cern.ch/cmsset_default.sh 
export SCRAM_ARCH=el9_amd64_gcc11

n_events=500
releasedir=/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tools
tmpdir=/scratch365/gziemyt2/DiphotonGun/condor
outpath=/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_500events1p5Ma1p0_1501p0EPileup_MiniAODvalidationSample.root
saveAOD=True
aMass=1.5
minbiasfile=/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_5000events_MinBias2018v1.root
Emin=1.0
Emax=1501.0
aMassErr=0.1

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
PREMIXfilepath=${wkdir}/Premix.root
GENSIMfilepath=${wkdir}/GENSIM.root
DIGIHLTfilepath=${wkdir}/DIGIHLTPU.root
RECOfilepath=${wkdir}/RECO.root
MINIfilepath=${wkdir}/MINI.root

PREMIX=$releasedir/CMSSW_13_1_0/src
GENSIM=$releasedir/CMSSW_13_1_0/src
DIGIHLT=$releasedir/CMSSW_13_1_0/src
RECO=$releasedir/CMSSW_13_1_0/src
MINI=$releasedir/CMSSW_13_1_0/src

echo "Starting PreMix Generation"

echo "Premix step"
cd $PREMIX
eval `scramv1 runtime -sh`
cmsRun PremixSample2018.py $n_events $minbiasfile $PREMIXfilepath

# Check exit status
if [ $? -ne 0 ]
then
  echo "Premix step failed with exit code $?, exiting."
  exit 1
fi

echo "Starting GEN to MiniAOD steps"

echo "GENSIMDIGIHLTAOD step"
cd $GENSIM
eval `scramv1 runtime -sh`
cmsRun GENSIMDIGIHLTAODPU20182.py $n_events $RECOfilepath $aMass $Emin $Emax $aMassErr $PREMIXfilepath

if [ $saveAOD == "True" ]
then
  # Replace MiniAOD in outpath with AOD
  outMinifilepath=${outpath//MiniAOD/AOD}
  cp $RECOfilepath $outMinifilepath
fi

echo "MiniAOD step"
cd $MINI
eval `scramv1 runtime -sh` 
cmsRun MiniAODstep2018.py $RECOfilepath $MINIfilepath


echo "Done generating events for $jobname"
echo "Moving output file to hadoop"
mv $MINIfilepath $outpath

echo "Cleaning up, removing temporary directory"
rm -rf $wkdir
