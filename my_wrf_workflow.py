from datetime import timedelta, datetime
import os
import create_namelists
import affli
import glob
import ntpath
import logging
import postproc
import path_config
from os import listdir
from os.path import isfile, join
import wrf_model, wrf_da

prog_paths = path_config.load_config('metservice')

affli.create_working_dir(prog_paths)
logging.basicConfig(filename=prog_paths['working_dir'] + '/running_log',level=logging.INFO,filemode='w',format='%(message)s')
global_data_dir, model_starttime, cur_utc = affli.return_initial_para(prog_paths)
wrf_dir, wps_dir, obsnudge_dir, postproc_dir, wrfda_dir, wrfda_verif_dir = affli.create_subdir_for_the_workflow(prog_paths)
m, model_domain = postproc.extract_the_domain(prog_paths['model_domain'])

# plot the map from wps namelist
if prog_paths['run_postproc']:
    logging.info('----------------------')
    logging.info('plotting the model domain from namelist')
    logging.info('----------------------')
    postproc.plot_the_domain(m,postproc_dir)

# run WPS
if prog_paths['run_wps']:
    logging.info('----------------------')
    logging.info('WPS')
    logging.info('----------------------')
    wrf_model.run_wps(prog_paths,
                      model_starttime, 
                      wps_dir, global_data_dir)

# run nudging
if prog_paths['run_obsnudge']:
    logging.info('----------------------')
    logging.info('obs-nudge')
    logging.info('----------------------')
    wrf_da.run_obsnudge(prog_paths,
                        model_starttime,cur_utc,
                        model_domain,
                        obsnudge_dir)

# run WRF
if prog_paths['run_wrf']:
    logging.info('----------------------')
    logging.info('WRF')
    logging.info('----------------------')
    wrf_model.run_wrf(prog_paths, model_starttime, wrf_dir, wps_dir)

# run WRFDA or WRFDA verif
if prog_paths['run_wrfda']:
    logging.info('----------------------')
    logging.info('WRFDA')
    logging.info('----------------------')
    wrf_da.run_wrfda(prog_paths, model_starttime, wrfda_dir)

'''
# run WRFDA or WRFDA verif
if prog_paths['run_wrfda'] or prog_paths['run_wrfda_verif']:
    logging.info('----------------------')
    logging.info('WRFDA - OBSPROC')
    logging.info('----------------------')
    logging.info('OBSPROC: Create namelist.obsproc')
    
    analysis_datetime = datetime.strptime(prog_paths['debug_info']['debug_analysis_datetime_str'], '%Y-%m-%dT%H:%M:%S')
    obsfile_path = prog_paths['debug_info']['debug_little_r_path'] + '/all.little_r:' + analysis_datetime.strftime('%Y-%m-%d_%H')
    obserr_path = prog_paths['debug_info']['debug_obs_err_for_var']
    create_namelists.obsproc_namelist(obsfile_path, obserr_path, prog_paths['model_domain'], analysis_datetime, obsproc_dir)
    
    logging.info('OBSPROC: running obsproc.exe')
    obsproc_log = affli.run_executables(prog_paths['exe']['wrfda']['obsproc'], obsproc_dir)
    obsproc_file = open(obsproc_dir + '/run_obsproc_log', "w")
    obsproc_file.write(obsproc_log)
    obsproc_file.close()
    logging.info('WRFDA - OBSPROC: completed !')
    
    if prog_paths['run_wrfda']:
        wrfda_working_dir = wrfda_dir
    elif prog_paths['run_wrfda_verif']:
        wrfda_working_dir = wrfda_verif_dir

    logging.info('3DVAR: Copy background data, TBL, observation and background error')
    # link background data
    affli.run_executables('cp -rf {}/wrfout_d01_{} {}/{}'.format(wrf_dir, analysis_datetime.strftime('%Y-%m-%d_%H:%M:%S'), wrfda_working_dir, 'fg'), wrfda_working_dir)
    # link landuse.TBL
    affli.run_executables('cp -rf {}/{} {}'.format(prog_paths['scripts']['wrf']['tbl'], 'LANDUSE.TBL', wrfda_working_dir), wrfda_working_dir)
    
    # link obs at analysis
    affli.run_executables('cp -rf {}/obs_gts_{}.3DVAR {}/{}'.format(obsproc_dir, analysis_datetime.strftime('%Y-%m-%d_%H:%M:%S'), wrfda_working_dir, 'ob.ascii'), wrfda_working_dir)   
        
    # link background error
    affli.run_executables('cp -rf {} {}/{}'.format(prog_paths['scripts']['wrfda']['be'], wrfda_working_dir, 'be.dat'), wrfda_working_dir)

    if prog_paths['run_wrfda']:
        logging.info('----------------------')
        logging.info('WRFDA - 3DVAR')
        logging.info('----------------------')
        logging.info('3DVAR: Create namelist.input')
        create_namelists.wrfda_namelist(model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600),
                                          analysis_datetime,
                                          prog_paths['model_domain'],wrfda_working_dir)
    
        logging.info('3DVAR: running da_wrfvar.exe')
        wrfda_log = affli.run_executables(prog_paths['exe']['wrfda']['wrfda'], wrfda_working_dir)
        wrfda_file = open(wrfda_working_dir + '/run_3dvar_log', "w")
        wrfda_file.write(wrfda_log)
        wrfda_file.close()
        
        logging.info('3DVAR: completed !')
    if prog_paths['run_wrfda_verif']:
        logging.info('----------------------')
        logging.info('WRFDA - verification')
        logging.info('----------------------')
        logging.info('3DVAR - verification: Create namelist.input')
        wrfda_verif_hour = 9
        fcst_hr_at_verif = wrfda_verif_hour - model_starttime.hour
        
        # 1. run wrfda to produce the filtered obs
        create_namelists.wrfda_namelist(model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600),
                                          analysis_datetime,
                                          prog_paths['model_domain'], wrfda_working_dir,
                                          wrfda_qcobs = True)
        logging.info('3DVAR: running da_wrfvar.exe')
        wrfda_verif_log = affli.run_executables(prog_paths['exe']['wrfda']['wrfda'], wrfda_working_dir)
        wrfda_file = open(wrfda_working_dir + '/run_verif_obsqc_log', "w")
        wrfda_file.write(wrfda_verif_log)
        wrfda_file.close()
        
        # 1.1 remove unnecessary files
        datalist  = [f for f in listdir(wrfda_working_dir) if isfile(join(wrfda_working_dir, f))]
        for dfilename in datalist:
            if dfilename != 'filtered_obs_01':
                os.remove(wrfda_working_dir + '/' + dfilename)

        # 2. running verif_obs_wrapper.ksh
        verif_obs_wrapper_dir = '{}/{}/data'.format(wrfda_working_dir, 'verif_obs_wrapper_dir')
        if os.path.exists(verif_obs_wrapper_dir) == False:
            os.makedirs(verif_obs_wrapper_dir)

        # 2.1 link be.dat
        if os.path.exists(verif_obs_wrapper_dir + '/data') == False:
            os.makedirs(verif_obs_wrapper_dir + '/data')
        affli.run_executables('cp -rf {} {}/{}/be.dat'.format(prog_paths['scripts']['wrfda']['be'], verif_obs_wrapper_dir, 'data'),wrfda_working_dir)

        # 2.2 link forecasts
        fc_dir = verif_obs_wrapper_dir + '/fc/' + model_starttime.strftime('%Y%m%d%H')
        if os.path.exists(fc_dir) == False:
            os.makedirs(fc_dir)
        affli.run_executables('ln -sf {}/wrfout_d01_* {}'.format(wrf_dir, fc_dir), wrfda_working_dir)

        # 2.3 link inc
        if os.path.exists(verif_obs_wrapper_dir + '/inc') == False:
            os.makedirs(verif_obs_wrapper_dir + '/inc')
        affli.run_executables('ln -sf {}/inc/namelist_script.inc {}/inc'.format(prog_paths['scripts']['wrfda']['wrfda_build_dir'], verif_obs_wrapper_dir), wrfda_working_dir)

        # 2.4 link obs
        ob_dir = '{}/ob/{}/wrfvar/'.format(verif_obs_wrapper_dir, analysis_datetime.strftime('%Y%m%d%H'))
        if os.path.exists(ob_dir) == False:
            os.makedirs(ob_dir)
        affli.run_executables('cp -rf filtered_obs_01 {}/filtered_obs'.format(ob_dir), wrfda_working_dir)

        # 2.5 link LANDUSE.TBL
        if os.path.exists(verif_obs_wrapper_dir + '/run') == False:
            os.makedirs(verif_obs_wrapper_dir + '/run')
        affli.run_executables('cp -rf {}/run/LANDUSE.TBL {}/run'.format(prog_paths['scripts']['wrfda']['wrfda_build_dir'], verif_obs_wrapper_dir), wrfda_working_dir)
     
        # 2.6 link exe
        if os.path.exists(verif_obs_wrapper_dir + '/var/da') == False:
            os.makedirs(verif_obs_wrapper_dir + '/var/da')
        affli.run_executables('ln -sf {}/var/da/*.exe {}/var/da'.format(prog_paths['scripts']['wrfda']['wrfda_build_dir'], verif_obs_wrapper_dir), wrfda_working_dir)
       
        # 2.7 link satellite info
        if os.path.exists(verif_obs_wrapper_dir + '/var/run') == False:
            os.makedirs(verif_obs_wrapper_dir + '/var/run')
        affli.run_executables('cp -rf {}/var/run/radiance_info {}/var/run'.format(prog_paths['scripts']['wrfda']['wrfda_build_dir'], verif_obs_wrapper_dir), wrfda_working_dir)
        affli.run_executables('cp -rf {}/var/run/gmao_airs_bufr.tbl {}/var/run/gmao_airs_bufr.tbl_new'.format(prog_paths['scripts']['wrfda']['wrfda_build_dir'], verif_obs_wrapper_dir), wrfda_working_dir)     
        
        create_namelists.verif_obs_wrapper(prog_paths['model_domain'], 
                                           model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600), analysis_datetime,
                                           verif_obs_wrapper_dir,
                                           prog_paths['scripts']['wrfda']['wrfda_script_dir'],
                                           prog_paths['scripts']['wrfda']['wrfda_graphic_dir'],
                                           wrfda_verif_hour, fcst_hr_at_verif)
        
        affli.run_executables('chmod 755 {}/verif_obs_wrapper.ksh'.format(verif_obs_wrapper_dir), wrfda_working_dir)
        print '{}/verif_obs_wrapper.ksh'.format(verif_obs_wrapper_dir)
        affli.run_executables('{}/verif_obs_wrapper.ksh'.format(verif_obs_wrapper_dir), verif_obs_wrapper_dir)
'''