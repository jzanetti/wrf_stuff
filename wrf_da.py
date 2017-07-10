import logging
from datetime import timedelta, datetime
import affli

def run_obsnudge(prog_paths,model_starttime,cur_utc,model_domain,obsnudge_dir):
    logging.info('obs-nudge: copy obsconfig.ini and fix the permission issue')
    logging.info('obsnudge: run obs2little_r')
    obs_time_buffer_sec = 3600
    if prog_paths['debug_info']['download_obs_from_s3']:
        obs2little_r_cmd = '{} {} {} --{} {} {} {} {} {} {} {} {} {} {} {} {}'.format(prog_paths['scripts']['obsnudge']['obs2little_r'],
                                    'research', 'us-west-2',
                                    'archive', 
                                    model_starttime.strftime('%Y%m%d%H%M'), 
                                    #-30.0, -50.0, 160.0, 190.0,
                                    model_domain[2], model_domain[0], model_domain[1], model_domain[3],
                                    3,
                                   '--to', (cur_utc + timedelta(seconds = obs_time_buffer_sec)).strftime('%Y%m%d%H%M'),
                                   '--cutoff-time', (cur_utc + + timedelta(seconds = obs_time_buffer_sec)).strftime('%Y%m%d%H%M'),
                                   '--num_threads', 64)
        logging.info('   start downloading obs ... ')
        affli.run_executables(obs2little_r_cmd, obsnudge_dir)
    else:
        affli.run_executables('cp -rf {}/* {}'.format(prog_paths['debug_info']['debug_little_r_path'],obsnudge_dir),obsnudge_dir)
    logging.info('   end downloading obs ... ')

    logging.info('obsnudge: run fdda_prep')
    fdda_prep_cmd = '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(prog_paths['scripts']['obsnudge']['fdda_prep'],
                                'research', 'archive',
                                model_starttime.strftime('%Y%m%d%H%M'), cur_utc.strftime('%Y%m%d%H%M'), 
                                prog_paths['met_intervals_sec'],
                                model_domain[2], model_domain[0], model_domain[1], model_domain[3],
                                #-42.0, -38.0, 173.0, 176.0,
                                prog_paths['working_dir'],
                                obsnudge_dir,
                                1, 
                                'all.little_r',
                                '/home/szhang/Programs/CHAMP-4.2.30','adl6kmN','GFS')
    affli.run_executables(fdda_prep_cmd, obsnudge_dir)
    logging.info('fdda_prep finished')
    
    
    if prog_paths['run_postproc']:
        extract_domain_obs_data = postproc.extract_domain_obs('/home/szhang/workspace_wrf/var_test_20170629/obsnudge/OBS_DOMAIN101')
        for obs_type in ['temperature','pressure','height','u','rh']:
            for obs_platform in ['FM-42', 'FM-12','FM-88']:
                postproc.plot_domain_obs(prog_paths['model_domain'], extract_domain_obs_data,\
                                         obs_type, obs_platform, model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600),
                                         postproc_dir)


def run_wrfda(prog_paths, model_starttime, wrfda_dir):
    logging.info('OBSPROC: Create namelist.obsproc')
    analysis_datetime = datetime.strptime(prog_paths['debug_info']['debug_analysis_datetime_str'], '%Y-%m-%dT%H:%M:%S')
    
    # 1. link observation and observation error
    obsfile_path = prog_paths['debug_info']['debug_little_r_path'] + '/all.little_r:' + analysis_datetime.strftime('%Y-%m-%d_%H')
    obserr_path = prog_paths['debug_info']['debug_obs_err_for_var']
    
    # 2. create obsproc namelist
    create_namelists.obsproc_namelist(obsfile_path, obserr_path, prog_paths['model_domain'], analysis_datetime, obsproc_dir)
    
    # 3. run OBSPROC
    logging.info('OBSPROC: running obsproc.exe')
    obsproc_log = affli.run_executables(prog_paths['exe']['wrfda']['obsproc'], obsproc_dir)
    obsproc_file = open(obsproc_dir + '/run_obsproc_log', "w")
    obsproc_file.write(obsproc_log)
    obsproc_file.close()
    logging.info('WRFDA - OBSPROC: completed !')
    
    # 4. run WRFDA
    wrfda_working_dir = wrfda_dir

    logging.info('3DVAR: Copy background data, TBL, observation and background error')
    # 4.1 link background data
    affli.run_executables('cp -rf {}/wrfout_d01_{} {}/{}'.format(wrf_dir, analysis_datetime.strftime('%Y-%m-%d_%H:%M:%S'), wrfda_working_dir, 'fg'), wrfda_working_dir)
    # 4.2 link landuse.TBL
    affli.run_executables('cp -rf {}/{} {}'.format(prog_paths['scripts']['wrf']['tbl'], 'LANDUSE.TBL', wrfda_working_dir), wrfda_working_dir)
    # 4.3 link obs at analysis
    affli.run_executables('cp -rf {}/obs_gts_{}.3DVAR {}/{}'.format(obsproc_dir, analysis_datetime.strftime('%Y-%m-%d_%H:%M:%S'), wrfda_working_dir, 'ob.ascii'), wrfda_working_dir)   
    # 4.4 link background error
    affli.run_executables('cp -rf {} {}/{}'.format(prog_paths['scripts']['wrfda']['be'], wrfda_working_dir, 'be.dat'), wrfda_working_dir)

    # 4.5 create wrfda namelist
    create_namelists.wrfda_namelist(model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600),
                                          analysis_datetime,
                                          prog_paths['model_domain'],wrfda_working_dir)
    
    # 4.6 run wrfda
    logging.info('3DVAR: running da_wrfvar.exe')
    wrfda_log = affli.run_executables(prog_paths['exe']['wrfda']['wrfda'], wrfda_working_dir)
    wrfda_file = open(wrfda_working_dir + '/run_3dvar_log', "w")
    wrfda_file.write(wrfda_log)
    wrfda_file.close()

    