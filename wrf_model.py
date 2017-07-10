import logging
import create_namelists
from datetime import timedelta, datetime
import affli

def run_wps(prog_paths, model_starttime, wps_dir, global_data_dir):    
    logging.info('WPS: Create namelist.wps')
    create_namelists.wps_namelist(prog_paths['model_domain'],model_starttime, model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600), prog_paths['met_intervals_sec'], wps_dir, prog_paths['scripts']['wps']['geog_data_path'], prog_paths['scripts']['wps']['tbl'])
    
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
    
def run_wrf(prog_paths, model_starttime, wrf_dir, wps_dir):
    logging.info('WRF: Create namelist.input')
    create_namelists.wrf_namelist(prog_paths['model_domain'], model_starttime,model_starttime + timedelta(seconds = prog_paths['fcst_hrs']*3600), prog_paths['run_obsnudge'], wrf_dir)
    
    logging.info('WRF: Link TBL')
    affli.run_executables('ln -sf {}/* {}'.format(prog_paths['scripts']['wrf']['tbl'],wrf_dir), wrf_dir)

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