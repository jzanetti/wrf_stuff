import subprocess
import os, glob
import itertools
import logging
from datetime import timedelta, datetime

def run_executables(cmd, working_dir):
    try:
        soutput = subprocess.check_output(cmd, shell=True, cwd=working_dir)
        return soutput
    except subprocess.CalledProcessError as e:
        print e.output
        
def copy_outputs_from_pwd(file_list, working_dir):
    for cf in file_list:
        subprocess.check_output('cp -rf {} {}'.format(cf, working_dir), shell=True)
        
def housekeeping(file_prefix_list, working_dir):
    for i in file_prefix_list:
        for x in list(itertools.chain(*[glob.glob(working_dir + '/' + i)])):
            os.remove(x)
            
def return_initial_para(prog_paths):
    # decide the modelling time depending on the weather it is a realtime run or debug run
    if prog_paths['run_mode'] == 'debug':
        cur_utc = datetime.strptime(prog_paths['debug_info']['debug_cur_valid_datetime_str'], '%Y-%m-%dT%H:%M:%S')
        cur_nzt = cur_utc + timedelta(seconds = 12*3600)
    elif prog_paths['run_mode'] == 'realtime':
        cur_nzt = datetime.now()
        cur_utc = cur_nzt - timedelta(seconds = 12*3600)
    logging.info('<><><><><><><><><><><><><><><><><><><>')
    logging.info('current NZT: {} / UTC: {}'.format(cur_nzt.strftime('%Y-%m-%dT%H:%M:%S'), cur_utc.strftime('%Y-%m-%dT%H:%M:%S')))
    if prog_paths['run_obsnudge']: 
        starttime_offset = 6
    else:
        starttime_offset = 3
    
    for hr_offset in range(starttime_offset,12):
        if (cur_utc - timedelta(seconds = hr_offset*3600)).hour % 6 == 0:
            model_starttime = cur_utc - timedelta(seconds = hr_offset*3600)
            break
    logging.info('model start time: {}'.format(model_starttime.strftime('%Y-%m-%dTT-%H:%M:%S')))
    logging.info('offset between model start time and current valid time: {} h'.format((cur_utc-model_starttime).total_seconds()/3600.0))
    logging.info('<><><><><><><><><><><><><><><><><><><>')
    
    # decide the input data location depending on the weather it is a realtime run or debug run
    if prog_paths['run_mode'] == 'debug':
        global_data_dir =  prog_paths['debug_info']['debug_global_analysis_path']
    elif prog_paths['run_mode'] == 'realtime':
        global_data_dir = '/var/lib/nfs/global-data-incoming/gfs-prod/det/' + model_starttime.strftime('%Y%m%d%H') 
    logging.info('global data source: {}'.format(global_data_dir))
    
    return global_data_dir, model_starttime, cur_utc

def create_working_dir(prog_paths):
    if os.path.exists(prog_paths['working_dir']) == False:
        os.makedirs(prog_paths['working_dir'])
        
def create_subdir_for_the_workflow(prog_paths):
    logging.info('----------------------')
    logging.info('Prepare directories etc.')
    logging.info('----------------------')     
    wrf_dir = prog_paths['working_dir'] + '/wrf'
    if os.path.exists(wrf_dir) == False:
        os.makedirs(wrf_dir)

    wps_dir = prog_paths['working_dir'] + '/wps'
    if os.path.exists(wps_dir) == False:
        os.makedirs(wps_dir)
        
    obsnudge_dir = prog_paths['working_dir'] + '/obsnudge'
    if os.path.exists(obsnudge_dir) == False:
        os.makedirs(obsnudge_dir)
        
    postproc_dir = prog_paths['working_dir'] + '/postproc'
    if os.path.exists(postproc_dir) == False:
        os.makedirs(postproc_dir)
    
    obsproc_dir = prog_paths['working_dir'] + '/obsproc'
    if os.path.exists(obsproc_dir) == False:
        os.makedirs(obsproc_dir)
    wrfda_dir = prog_paths['working_dir'] + '/wrfda'
    if os.path.exists(wrfda_dir) == False:
        os.makedirs(wrfda_dir)
        
    wrfda_verif_dir = prog_paths['working_dir'] + '/wrfda_verif'
    if os.path.exists(wrfda_verif_dir) == False:
        os.makedirs(wrfda_verif_dir)
    
    return wrf_dir, wps_dir, obsnudge_dir, postproc_dir, wrfda_dir, wrfda_verif_dir



