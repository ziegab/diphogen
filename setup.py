import os
import sys
import subprocess

import textwrap

import json

gen_dir = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.dirname(gen_dir)

# Initialize directories
cache_dir = f"{gen_dir}/cache"
condor_cache = f"{cache_dir}/condor"
tools_dir = f"{gen_dir}/tools"
for d in [tools_dir, condor_cache, tools_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

def try_command(cmd, fail_message=None, exit=True):
    try:
        output = subprocess.check_call(cmd, shell=True)
        return f"Exit code: {output}"
    except:
        if fail_message:
            print(fail_message)
        else:
            print(f"Failed to run command: {cmd}")

        if exit:
            sys.exit(1)
        else:
            return False

def ensure_cmssw(release):
    if not os.path.exists(f"{tools_dir}/{release}"):
        print(f"Setting up {release}")
        try_command(f"""
            cd {tools_dir}
            scram p CMSSW {release}
            cd {release}/src
            eval `scram runtime -sh`
            scram b -j 4"""
        )

def ensure_Config(release):
    if not os.path.exists(f"{tools_dir}/{release}/src/Configuration"):
        print(f"Setting up Configuration")
        try_command(f"""
            cd {tools_dir}/{release}/src
            eval `scram runtime -sh`
            git cms-addpkg Configuration
            scram b -j 4
        """)

def ensure_GeneratorInterface(release):
    if not os.path.exists(f"{tools_dir}/{release}/src/GeneratorInterface"):
        print(f"Setting up Generator Interface")
        try_command(f"""
            cd {tools_dir}/{release}/src
            eval `scram runtime -sh`
            git cms-addpkg GeneratorInterface/Pythia8Interface
            scram b -j 4
        """)

def ensure_files(release):
    if not os.path.exists(f"{tools_dir}/{release}/src/Configuration/Generator/python/AtoGammaGammaFlatMoE_pythia8_cfi.py"):
        print(f"Moving file to the correct directory.")
        try_command(f"""
            cd {tools_dir}
            cp {gen_dir}/keyFiles/AtoGammaGammaFlatMoE_pythia8_cfi.py ./{release}/src/Configuration/Generator/python/
            cd {tools_dir}/{release}/src
            scram b -j 4
        """)
    if not os.path.exists(f"{tools_dir}/{release}/src/GeneratorInterface/Pythia8Interface/plugins/Py8MoEGun.cc"):
        print(f"Moving plugins to the correct directory.")
        try_command(f"""
            cd {tools_dir}
            cp {gen_dir}/keyFiles/Py8MoEGun.cc ./{release}/src/GeneratorInterface/Pythia8Interface/plugins/
            cd {tools_dir}/{release}/src
            scram b -j 4
        """)
    if not os.path.exists(f"{tools_dir}/{release}/src/GENSIMstep2018.py"):
        print(f"Moving generator steps to the correct directory.")
        try_command(f"""
            cd {tools_dir}/{release}/src/
            cp {gen_dir}/keyFiles/GENSIMstep2018.py .
            cp {gen_dir}/keyFiles/DIGIHLTPU2018.py .
            cp {gen_dir}/keyFiles/AODstep2018.py .
            cp {gen_dir}/keyFiles/MiniAODstep2018.py .
            cp {gen_dir}/keyFiles/MinBiasSample2018.py .
            cp {gen_dir}/keyFiles/PremixSample2018.py .
            scram b -j 4
        """)

if __name__ == "__main__":
    # Setting up CMSSW environment for the GEN step
    ensure_cmssw("CMSSW_13_1_0")
    ensure_Config("CMSSW_13_1_0")
    ensure_GeneratorInterface("CMSSW_13_1_0")
    
    # Getting necessary plugins and scripts to generate the signal
    ensure_files("CMSSW_13_1_0")