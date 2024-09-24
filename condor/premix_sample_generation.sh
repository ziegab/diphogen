#!/bin/sh

#Generates a premix sample with 1000 events
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11

n_events=2500
releasedir=/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tools/CMSSW_13_1_0/src
tmpdir=/scratch365/gziemyt2/DiphotonGun/condor
outpath=/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_2500events_PremixSample2018v3.root

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

#### FILE I/O
MINBIASfilepath=${wkdir}/MinBias.root
PREMIXfilepath=${wkdir}/Premix.root

echo "Starting Premix Generation"

echo "MinBias step"
cd $releasedir
eval `scramv1 runtime -sh`
cmsRun MinBiasSample2018.py $n_events $MINBIASfilepath

# Check exit status
if [ $? -ne 0 ]
then
  echo "MinBias step failed with exit code $?, exiting."
  exit 1
fi

echo "Premix step"
cd $releasedir
eval `scramv1 runtime -sh`
cmsRun PremixSample2018.py $n_events $MINBIASfilepath $PREMIXfilepath

echo "Done generating events for $jobname"
echo "Moving output file to storage"
mv $PREMIXfilepath $outpath

echo "Cleaning up, removing temporary directory"
rm -rf $wkdir
