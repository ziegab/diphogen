To set up the repository:

```
# Clone this repository into your space
git clone https://gitlab.cern.ch/gziemyte/diphogen
# You will need to log into your existing CERN account to access this

# Set up the space so that everything works (VERY IMPORTANT STEP)
python3 diphogen/setup.py
```

Main file to be worked with is newGenerate_diphoSignalPU.py (located in ```diphogen/condor```). This by default generates AOD and MiniAOD files for the DiPhoton Gun. You also need to specify a premixed pileup sample for it - premix_sample_generation.sh can be used to create such a premixed pileup file. 
See ```README.md``` in the condor directory for a list of arguments that can modify the output file you get.

NOTE: The files in this repository are built to work with CMSSW_13_1_0 - other versions of CMSSW can also be used to generate sample files, but it's likely that you'll have to use cmsDriver.py withing a CMSSW environment and generate the necessary files yourself.