import sys
import os
import subprocess
import job_manager as jm

## Define paths
preprocessing_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
top_dir = os.path.dirname(preprocessing_dir)
sys.path.append(top_dir)
# USER = os.environ['USER']
# ceph_storage = f'/cms/cephfs/data/store/{USER}/DiphotonGun'
# vast_storage = f'/project01/ndcms/gziemyt2/DiphotonGun'
local_storage = f'{preprocessing_dir}/tempstore'
# defaultpremix = f'/afs/crc.nd.edu/user/g/gziemyt2/glados/diphogen/tempstore/AtoGG_1000events_PremixSample2018.root'

tools_dir = f"{preprocessing_dir}/tools/AtoGG"
scripts_dir = f"{tools_dir}/scripts"

signal_tag = 'AtoGG'
# tmpdir = f"/scratch365/{USER}/DiphotonGun/condor" 
tmpdir = f"/tmp/gziemyt2" # make sure this directory exists since the script branches off from this
# condortmpdir = f"/scratch365/gziemyt2/DiphotonGun/condor"
condortmpdir = f"/tmp/gziemyt2"

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
        aMass,
        releasedir,
        tmpdir,
        outpath,
        file_path,
        Emin,
        Emax,
        aMassErr,
        condor=False,
        saveAOD=True,
    ):

    ## Modify the executable with the specified new information
    lines_to_replace = [7, 8, 9, 10, 11, 12, 13, 14, 15] 
    saveAODstr=str(saveAOD)

    if condor:
        new_lines = ['n_events=' + n_total_events, 
                'releasedir=' + releasedir,
                'tmpdir=' + condortmpdir,
                'outpath=' + outpath,
                'saveAOD=' + saveAODstr,
                'aMass=' + aMass,
                'Emin=' + Emin,
                'Emax=' + Emax,
                'aMassErr=' + aMassErr] 
        execfile = file_path + executable
        replace_lines_in_file(execfile, lines_to_replace, new_lines)
        jm.submit_condor(execfile, job_name)
    else:
        new_lines = ['n_events=' + n_total_events, 
                'releasedir=' + releasedir,
                'tmpdir=' + tmpdir,
                'outpath=' + outpath,
                'saveAOD=' + saveAODstr,
                'aMass=' + aMass,
                'Emin=' + Emin,
                'Emax=' + Emax,
                'aMassErr=' + aMassErr]  
        execfile = file_path + executable
        replace_lines_in_file(execfile, lines_to_replace, new_lines)
        temp = f"{file_path}{executable}"
        # temp = f"./{executable}"
        subprocess.run([temp]) 

# Setting arguments and calling event generation
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate MiniAOD signal events')
    parser.add_argument('--n_total_events', '-n', type=int, default=500, help='Number of events per file.')
    parser.add_argument('--output_base', '-o', type=str, default=local_storage, help='Specify the output base directory. Default is vast.')
    parser.add_argument('--condor', '-c', action='store_true', help='Submit jobs to condor.')
    parser.add_argument('--saveAOD', type=bool, default=True, help='Save AOD as well as MiniAOD')
    parser.add_argument('--saveMiniAODv2', type=bool, default=True, help='Save MiniAOD')
    parser.add_argument('--aMass', '-Ma', type=float, default=999, help="Specify the mass (in GeV) of the orginal object that decays into 2 photons.")
    # parser.add_argument('--premixfile', '-PU', type=str, default=defaultpremix, help='Specify the location and file name of the premixed sample.')
    parser.add_argument('--Emin', type=float, default=10, help="Specify the minimum energy/pt of the original object to decay.")
    parser.add_argument('--Emax', type=float, default=1000, help="Specify the maximum energy/pt of the original object to decay.")
    parser.add_argument('--aMassErr', '-Err', type=float, default=0.1, help="Specify the mass range.")
    parser.add_argument('--validation', '-v', action='store_true', help='Label as validation run.')

    args = parser.parse_args()

    # Generate Events
    print("Generating signal events with configuration: ")
    print("Number of total events: ", args.n_total_events)
    print("Output base: ", args.output_base)
    print("Save AOD: ", args.saveAOD)
    print("Save MAOD: ", args.saveMiniAODv2)

    executable = f"run2_event_generationPU.sh"
    outputbase = args.output_base
    job_name_temp = signal_tag + '_' + str(args.n_total_events) + 'events' + str((args.aMass)) + 'Ma' + str((args.Emin)) + '_' + str((args.Emax)) + 'E' + 'Pileup_MiniAOD'
    if args.validation == True:
        job_name_temp += 'validationSample'
    job_name = job_name_temp.replace(".", "p")
    outpath = f"{outputbase}/{job_name}.root"
    file_path = f'{preprocessing_dir}/condor/'
    # file_path = f'/tmp/{USER}/DiphotonGun/'

    generate_signal_point(
        executable,
        job_name,
        str(args.n_total_events),
        str(args.aMass),
        tools_dir,
        tmpdir,
        outpath,
        file_path,
        str(args.Emin),
        str(args.Emax),
        str(args.aMassErr),
        condor=args.condor,
        saveAOD=args.saveAOD)