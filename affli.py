import subprocess
import os, glob
import itertools

def run_executables(cmd, working_dir):
    try:
        subprocess.check_output(cmd, shell=True, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        print e.output
        
def copy_outputs_from_pwd(file_list, working_dir):
    for cf in file_list:
        subprocess.check_output('cp -rf {} {}'.format(cf, working_dir), shell=True)
        
def housekeeping(file_prefix_list, working_dir):
    for i in file_prefix_list:
        for x in list(itertools.chain(*[glob.glob(working_dir + '/' + i)])):
            os.remove(x)
    