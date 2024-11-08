import sys
import os
import subprocess
import job_manager as jm

## Define paths
preprocessing_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
top_dir = os.path.dirname(preprocessing_dir)
sys.path.append(top_dir)
USER = os.environ['USER']
ceph_storage = f'/cms/cephfs/data/store/{USER}/DiphotonGun'
vast_storage = f'/project01/ndcms/{USER}/DiphotonGun'
local_storage = f'{preprocessing_dir}/tempstore'
# defaultpremix = f'/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tempstore/AtoGG_1000events_PremixSample2018.root'

tools_dir = f"{preprocessing_dir}/tools/CMSSW_13_1_0/src"
scripts_dir = f"{tools_dir}/scripts"

signal_tag = 'AtoGG'
# tmpdir = f"/scratch365/{USER}/DiphotonGun/condor" 
tmpdir = f"/tmp/{USER}/DiphotonGun" # make sure this directory exists since the script branches off from this
condortmpdir = f"/scratch365/{USER}/DiphotonGun/condor"
# condortmpdir = f"/tmp/{USER}/DiphotonGun/condor"

# Definitions to replace lines in executable and to generate the AOD/MiniAOD files
def replace_lines_in_file(file_path, lines_to_replace, new_lines):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i, line_num in enumerate(lines_to_replace):
        lines[line_num - 1] = new_lines[i] + '\n'  
    with open(file_path, 'w') as file:
        file.writelines(lines)

def generate_signal_point(
        executable,
        job_name,
        n_total_events,
        releasedir,
        tmpdir,
        outpath,
        file_path,
        condor=False,
    ):

    ## Modify the executable with the specified new information
    lines_to_replace = [7, 8, 9, 10] 

    if condor:
        new_lines = ['n_events=' + n_total_events, 
                'releasedir=' + releasedir,
                'tmpdir=' + condortmpdir,
                'outpath=' + outpath] 
        execfile = file_path + executable
        replace_lines_in_file(execfile, lines_to_replace, new_lines)
        jm.submit_condor(execfile, job_name)
    else:
        new_lines = ['n_events=' + n_total_events, 
                'releasedir=' + releasedir,
                'tmpdir=' + tmpdir,
                'outpath=' + outpath]  
        execfile = file_path + executable
        replace_lines_in_file(execfile, lines_to_replace, new_lines)
        temp = f"{file_path}/{executable}"
        subprocess.run([temp]) 

# Setting arguments and calling event generation
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate MiniAOD signal events')
    parser.add_argument('--n_total_events', '-n', type=int, default=500, help='Number of events per file.')
    parser.add_argument('--output_base', '-o', type=str, default=vast_storage, help='Specify the output base directory. Default is vast.')
    parser.add_argument('--condor', '-c', action='store_true', help='Submit jobs to condor.')
    parser.add_argument('--version', '-v', type=int, help='Version premix file to be made.')

    args = parser.parse_args()

    # Generate Events
    print("Generating signal events with configuration: ")
    print("Number of total events: ", args.n_total_events)
    print("Output base: ", args.output_base)

    executable = f"premix_sample_generation.sh"
    outputbase = args.output_base
    job_name = signal_tag + '_' + str(args.n_total_events) + 'events_MinBias2018v' + str(args.version)
    outpath = f"{outputbase}/{job_name}.root"
    file_path = f'{preprocessing_dir}/condor/'

    generate_signal_point(
        executable,
        job_name,
        str(args.n_total_events),
        tools_dir,
        tmpdir,
        outpath,
        file_path,
        condor=args.condor)