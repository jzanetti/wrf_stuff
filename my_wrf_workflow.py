from datetime import timedelta, datetime
import os
import create_namelists
import affli
import glob
import ntpath
import logging
import postproc

prog_paths = {
    'run_mode': 'debug', # you can choose debug or realtime
    'working_dir': '/home/szhang/workspace_wrf/var_test_20160630_no_nudging',
    'model_domain': 'debug_domain',
    'global_data_type': 'fnl', # you can choose gfs/FNL etc.
    'fcst_hrs': 12,
    'met_intervals_sec': 10800,
    'run_wps': True,
    'run_wrf': True,
    'run_obsnudge': False,
    'run_postproc': False,
    'scripts':{'wps':{
                    'vtable': '/home/szhang/workspace_wrf/standard_namelist/Vtable/Vtable.GFS',
                    'link_grib': '/home/szhang/workspace_wrf/standard_namelist/scripts/link_grib.csh',  
                    },
               'wrf':{
                   'tbl': '/home/szhang/workspace_wrf/standard_namelist/WRF_LIB'
                   },
               'obsnudge':{
                   'obs2little_r': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/obs2little_r',
                   'fdda_prep': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/fdda_prep',
                   }
               },
    'exe': {'wps': {
                'geogrid': '/home/szhang/Programs/anaconda2/envs/wrf/wps/bin/geogrid.exe',
                'ungrib': '/home/szhang/Programs/anaconda2/envs/wrf/wps/bin/ungrib.exe',
                'metgrid': '/home/szhang/Programs/anaconda2/envs/wrf/wps/bin/metgrid.exe',
                },
            'wrf': {
                'real': '/home/szhang/Programs/anaconda2/envs/wrf/wrf/main/real.exe',
                'wrf': '/home/szhang/Programs/anaconda2/envs/wrf/wrf/main/wrf.exe'
                }
        },
    'debug_info': {
        'debug_datetime_str': '2017-05-31T16:00:00',
        'debug_little_r_path': '/home/szhang/Programs/WRFDA_sample_data/wrf_workflow_little_r',
        }
    }

# create working directory and the main log file
if os.path.exists(prog_paths['working_dir']) == False:
    os.makedirs(prog_paths['working_dir'])
logging.basicConfig(filename=prog_paths['working_dir'] + '/running_log',level=logging.INFO,filemode='w',format='%(message)s')

# decide the modelling time depending on the weather it is a realtime run or debug run
if prog_paths['run_mode'] == 'debug':
    cur_utc = datetime.strptime(prog_paths['debug_info']['debug_datetime_str'], '%Y-%m-%dT%H:%M:%S')
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
    global_data_dir =  '/home/szhang/Programs/WRF_sample_data/FNL/20170531'
elif prog_paths['run_mode'] == 'realtime':
    global_data_dir = '/var/lib/nfs/global-data-incoming/gfs-prod/det/' + model_starttime.strftime('%Y%m%d%H') 
logging.info('global data source: {}'.format(global_data_dir))


# create the necessary directory for wrf, wps and obsnudge
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

# plot the map from wps namelist
if prog_paths['run_postproc']:
    logging.info('----------------------')
    logging.info('plotting the model domain from namelist')
    logging.info('----------------------')
    postproc.plot_the_domain(prog_paths['model_domain'],postproc_dir)

# run WPS
if prog_paths['run_wps']:
    logging.info('----------------------')
    logging.info('WPS')
    logging.info('----------------------')
    
    logging.info('WPS: Create namelist.wps')
    create_namelists.wps_namelist(prog_paths['model_domain'],model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600), prog_paths['met_intervals_sec'], wps_dir)
    
    logging.info('WPS: run geogrod.exe')
    affli.run_executables(prog_paths['exe']['wps']['geogrid'], wps_dir)
    
    logging.info('WPS: link GFS Vtable and link_grib.csh')
    affli.run_executables('ln -sf {} Vtable'.format(prog_paths['scripts']['wps']['vtable']), wps_dir)
    affli.run_executables('ln -sf {} .'.format(prog_paths['scripts']['wps']['link_grib']), wps_dir)
    
    logging.info('WPS: link global data')
    affli.run_executables('{}/link_grib.csh {}/{}*'.format(wps_dir, global_data_dir, prog_paths['global_data_type']), wps_dir)
    
    logging.info('WPS: run ungrib.exe')
    affli.run_executables(prog_paths['exe']['wps']['ungrib'], wps_dir)
    
    logging.info('WPS: run metgrid.exe')
    affli.run_executables(prog_paths['exe']['wps']['metgrid'], wps_dir)
    
    logging.info('WPS: housekeep')
    affli.housekeeping(['FILE*','GRIB*','link_grib.csh','Vtable'], wps_dir)
    
    logging.info('WPS task completed')

# run nudging
if prog_paths['run_obsnudge']:
    logging.info('----------------------')
    logging.info('obs-nudge')
    logging.info('----------------------')
    logging.info('obs-nudge: copy obsconfig.ini and fix the premission issue')
    #affli.run_executables('cp -rf {} {}'.format(prog_paths['scripts']['obsnudge']['obsconfig'], obsnudge_dir), obsnudge_dir)
    #affli.run_executables('chmod 755 {}'.format(prog_paths['scripts']['obsnudge']['obs2little_r']), obsnudge_dir)
    
    logging.info('obsnudge: run obs2little_r')
    obs_time_buffer_sec = 3600
    obs2little_r_cmd = '{} {} {} --{} {} {} {} {} {} {} {} {} {} {} {} {}'.format(prog_paths['scripts']['obsnudge']['obs2little_r'],
                                'research', 'us-west-2',
                                'archive', 
                                model_starttime.strftime('%Y%m%d%H%M'), 
                                #-30.0, -50.0, 160.0, 190.0,
                                -38.0, -42.0, 173.0, 176.0,
                                3,
                               '--to', (cur_utc + timedelta(seconds = obs_time_buffer_sec)).strftime('%Y%m%d%H%M'),
                               '--cutoff-time', (cur_utc + + timedelta(seconds = obs_time_buffer_sec)).strftime('%Y%m%d%H%M'),
                               '--num_threads', 64)
    logging.info('   start downloading obs ... ')
    if prog_paths['run_mode'] == 'debug':
        affli.run_executables('cp -rf {}/* {}'.format(prog_paths['debug_info']['debug_little_r_path'],obsnudge_dir),obsnudge_dir)
    else:
        affli.run_executables(obs2little_r_cmd, obsnudge_dir)
    logging.info('   end downloading obs ... ')

    logging.info('obsnudge: run fdda_prep')
    fdda_prep_cmd = '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(prog_paths['scripts']['obsnudge']['fdda_prep'],
                                'research', 'archive',
                                model_starttime.strftime('%Y%m%d%H%M'), cur_utc.strftime('%Y%m%d%H%M'), 
                                prog_paths['met_intervals_sec'],
                                -30.0, -50.0, 160.0, 190.0,
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
    
# run WRF
if prog_paths['run_wrf']:
    logging.info('----------------------')
    logging.info('WRF')
    logging.info('----------------------')
    logging.info('WRF: Create namelist.input')
    create_namelists.wrf_namelist(prog_paths['model_domain'], model_starttime,model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600), prog_paths['run_obsnudge'], wrf_dir)
    
    logging.info('WRF: Link TBL')
    affli.run_executables('ln -sf {}/* {}*'.format(prog_paths['scripts']['wrf']['tbl'],wrf_dir), wrf_dir)

    logging.info('WRF: Link metdata from WPS')
    affli.run_executables('ln -sf {}/met_em* {}'.format(wps_dir,wrf_dir), wrf_dir)

    if prog_paths['run_obsnudge']:
        logging.info('WRF: Link metoa* and OBSDOMAIN* from obsnudge')
        metoa_list = glob.glob('{}/metoa*'.format(obsnudge_dir))
        for cmetoa in metoa_list:
            os.remove('{}/{}'.format(wrf_dir,ntpath.basename(cmetoa).replace('metoa','met')))
            logging.info(' --- ln -sf {} {}'.format(cmetoa, wrf_dir + '/' + ntpath.basename(cmetoa).replace('metoa','met')))
            affli.run_executables('ln -sf {} {}'.format(cmetoa, wrf_dir + '/' + ntpath.basename(cmetoa).replace('metoa','met')),wrf_dir)
        
        affli.run_executables('ln -sf {} {}'.format(obsnudge_dir + '/OBS_DOMAIN*', wrf_dir), wrf_dir)
    
    logging.info('WRF: run real.exe')
    affli.run_executables(prog_paths['exe']['wrf']['real'], wrf_dir)

    logging.info('WRF: run wrf.exe')
    wrf_log = affli.run_executables(prog_paths['exe']['wrf']['wrf'], wrf_dir)
    wrf_log_file = open(wrf_dir + '/run_wrf_log', "w")
    wrf_log_file.write(wrf_log)
    wrf_log_file.close()

    logging.info('WRF: wrf.exe completed !')
    print 'job done, check the log at {}'.format(prog_paths['working_dir'] + '/running_log')

