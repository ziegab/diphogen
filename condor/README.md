To generate files according to the defaults listed in the code, cd to the diphogen/condor directory and enter:

```python3 newGenerate_diphoSignalPU.py```

Arguments can be listed with:
```python3 newGenerate_diphoSignalPU.py -n 500```

Arguments:
- ```-n``` to specify number of events. Must be followed by an integer argument. (Default=500)
- ```-o``` to specify the output base directory. Must be followed by a string argument. (Default=/project01/ndcms/{USER}/DiphotonGun)
- ```-c``` to submit to condor. (Default=False)
- ```-Ma``` to specify the aMass (GeV). Must be followed by an integer argument. (Default=999)
-  ```-PU``` to specify the PileUp file. Must be followed by path to premix file.
- ```--eMax``` to specify maximum energy. Must be followed by a float argument. (Default=1000)
- ```--eMin``` to specify minimum energy. Must be followed by a float argument. (Default=10)

NOTE: You can also modify the directories in the newGenerate_diphoSignalPU.py script directly, if you want to change the names of the directories or if you want to direct to a different temporary directory (default is to /scratch365/ because /tmp/ sometimes has problems working with condor).