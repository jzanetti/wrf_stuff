import datetime

def load_config(config_name):
    if config_name == 'home':
        prog_paths = {
            'run_mode': 'debug', # you can choose debug or realtime
            'working_dir': '/home/jzanetti/wrf_directory/wrf_exp_20170704',
            'model_domain': 'debug_domain',
            'global_data_type': 'fnl', # you can choose gfs/FNL etc.
            'fcst_hrs': 6,
            'met_intervals_sec': 10800,
            'run_wps': True,
            'run_wrf': True,
            'run_obsnudge': False,
            'run_wrfda': False,
            'run_wrfda_verif': False,
            'run_postproc': True,
            'scripts':{'wps':{
                            'vtable': '/home/jzanetti/wrf_directory/standard_namelists/Vtable.GFS',
                            'link_grib': '/home/jzanetti/wrf_directory/standard_namelists/link_grib.csh',  
                            'geog_data_path': '/home/jzanetti/programs/WRF_geog/geog',
                            'tbl': '/home/jzanetti/wrf_directory/standard_namelists/WPS_TBL',
                            },
                       'wrf':{
                           'tbl': '/home/jzanetti/wrf_directory/standard_namelists/WRF_TBL'
                           },
                       'obsnudge':{
                           'obs2little_r': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/obs2little_r',
                           'fdda_prep': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/fdda_prep',
                           },
                       'wrfda':{
                           'be': '/home/jzanetti/programs/WRFDA-3.9/WRFDA/var/run/be.dat.cv3',
                           'wrfda_script_dir': '/home/jzanetti/programs/WRFDA_V3.8_TOOLS/TOOLS/var/scripts',
                           'wrfda_graphic_dir': '/home/szhang/Programs/WRFDA-Tools-3.8.1/TOOLS/var/graphics/ncl',
                           'wrfda_build_dir': '/home/jzanetti/programs/WRFDA-3.9/WRFDA'
                           }
                       },
            'exe': {'wps': {
                        'geogrid': '/home/jzanetti/programs/WPS/geogrid.exe',
                        'ungrib': '/home/jzanetti/programs/WPS/ungrib.exe',
                        'metgrid': '/home/jzanetti/programs/WPS/metgrid.exe',
                        },
                    'wrf': {
                        'real': '/home/jzanetti/programs/WRFV3/main/real.exe',
                        'wrf': '/home/jzanetti/programs/WRFV3/main/wrf.exe'
                        },
                    'wrfda':{
                        'obsproc': '/home/jzanetti/programs/WRFDA-3.9/WRFDA/var/obsproc/obsproc.exe',
                        'wrfda': '/home/jzanetti/programs/WRFDA-3.9/WRFDA/var/build/da_wrfvar.exe',
                        'da_verif_obs': '/home/jzanetti/programs/WRFDA-3.9/WRFDA/var/build/da_verif_obs.exe',
                        }
                },
            'debug_info': {
                'debug_cur_valid_datetime_str': '2017-01-01T12:00:00',
                'debug_analysis_datetime_str': '2017-01-01T09:00:00',
                'download_obs_from_s3': False,
                'debug_little_r_path': '/home/jzanetti/wrf_directory/little_r',
                'debug_obs_err_for_var': '/home/jzanetti/programs/WRFDA-3.9/WRFDA/var/obsproc/obserr.txt',
                'debug_global_analysis_path': '/home/jzanetti/wrf_directory/fnl/20170101',
                }
            }
        


    if config_name == 'metservice':
        wrf_stuff_script_path = '/home/szhang/GitHub_branches/wrf_stuff'
        prog_paths = {
            'run_mode': 'debug', # you can choose debug or realtime
            'working_dir': '/home/szhang/workspace_wrf/wrf_cycling_test/debug_run4',
            #'working_dir': '/home/szhang/workspace_wrf/wrf_cycling_test/test_' + datetime.datetime.now().strftime('%Y%m%d%H%M'),
            'model_domain': 'debug_domain',
            'global_data_type': 'fnl', # you can choose gfs/FNL etc.
            'fcst_hrs': 6,
            'met_intervals_sec': 10800,
            'run_wps': False,
            'run_wrf': True,
            'run_obsnudge': False,
            'run_wrfda': False,
            'run_wrfda_verif': False,
            'run_postproc': False,
            'scripts':{'wps':{
                            'vtable': wrf_stuff_script_path + '/test/WRF_build/Vtable/Vtable.GFS',
                            'link_grib': wrf_stuff_script_path + '/test/WRF_build/others/link_grib.csh',  
                            'geog_data_path': '/home/szhang/Programs/WRF_sample_data/geog_complete/geog',
                            'tbl': wrf_stuff_script_path + '/test/WRF_build/TBL/WPS_TBL',
                            },
                       'wrf':{
                           'tbl': wrf_stuff_script_path + '/test/WRF_build/TBL/WRF_TBL'
                           },
                       'obsnudge':{
                           'obs2little_r': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/obs2little_r',
                           'fdda_prep': '/home/szhang/Programs/anaconda2/envs/obs2r_20160629/bin/fdda_prep',
                           },
                       'wrfda':{
                           'be': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA/var/run/be.dat.cv3',
                           'wrfda_script_dir': '/home/szhang/Programs/WRFDA-Tools-3.8.1/TOOLS/var/scripts',
                           'wrfda_graphic_dir': '/home/szhang/Programs/WRFDA-Tools-3.8.1/TOOLS/var/graphics/ncl',
                           'wrfda_build_dir': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA'
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
                        },
                    'wrfda':{
                        'obsproc': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA/var/obsproc/obsproc.exe',
                        'wrfda': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA/var/build/da_wrfvar.exe',
                        'da_verif_obs': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA/var/build/da_verif_obs.exe',
                        }
                },
            'debug_info': {
                'debug_cur_valid_datetime_str': '2017-06-01T12:00:00',
                'debug_analysis_datetime_str': '2017-06-01T09:00:00',
                'download_obs_from_s3': False,
                'debug_little_r_path': wrf_stuff_script_path + '/test_data/little_r_debug/2017-06-01',
                'debug_obs_err_for_var': '/home/szhang/Programs/WRFDA-3.9.0/WRFDA/var/obsproc/obserr.txt',
                'debug_global_analysis_path': wrf_stuff_script_path + '/test_data/fnl/20170601',
                }
            }
        

   
        
    return prog_paths
