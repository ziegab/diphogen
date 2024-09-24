#!/bin/sh

#Generates events for a given gridpack
source /cvmfs/cms.cern.ch/cmsset_default.sh 
export SCRAM_ARCH=el9_amd64_gcc11

n_events=250
releasedir=/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tools
tmpdir=/scratch365/gziemyt2/DiphotonGun/condor
outpath=/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_250events1.0Ma10.02000.0pTPileup_MiniAODv2.root
saveAOD=True
aMass=1.0
pileupfile=/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_2500events_PremixSample2018v2.root
eMax=2000.0
eMin=10.0

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
GENSIMfilepath=${wkdir}/GENSIM.root
DIGIHLTfilepath=${wkdir}/DIGIHLTPU.root
RECOfilepath=${wkdir}/RECO.root
MINIfilepath=${wkdir}/MINI.root

GENSIM=$releasedir/CMSSW_13_1_0/src
DIGIHLT=$releasedir/CMSSW_13_1_0/src
RECO=$releasedir/CMSSW_13_1_0/src
MINI=$releasedir/CMSSW_13_1_0/src

echo "Starting GEN to MiniAOD steps"

echo "GENSIM step"
cd $GENSIM
eval `scramv1 runtime -sh`
cmsRun GENSIMstep2018.py $n_events $GENSIMfilepath $aMass $eMax $eMin

# Check exit status
if [ $? -ne 0 ]
then
  echo "GENSIM step failed with exit code $?, exiting."
  exit 1
fi

echo "DIGIHLT step"
cd $DIGIHLT
eval `scramv1 runtime -sh`
cmsRun DIGIHLTPU2018.py $GENSIMfilepath $DIGIHLTfilepath $pileupfile $n_events

echo "RECO step"
cd $RECO
eval `scramv1 runtime -sh`
cmsRun AODstep2018.py $DIGIHLTfilepath $RECOfilepath

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
