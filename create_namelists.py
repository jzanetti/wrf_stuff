import datetime
from wrf_domain_config import wrf_domain_config

def verif_obs_wrapper(domain_name,
                      start_date, end_date, analysis_date,
                      verif_obs_wrapper_dir,
                      wrfda_script_dir,
                      wrfda_graphic_dir,
                      wrfda_verif_hour, fcst_hr_at_verif):
    """create the verif_obs_wrapper namelist
    """
    namelist_field = {
        'da_run_suite_verif_obs': {
            'CLEAN': False,
            'INITIAL_DATE': analysis_date.strftime('%Y%m%d%H'),
            'FINAL_DATE': analysis_date.strftime('%Y%m%d%H'),
            'WRFVAR_DIR': '$RUN_DIR',
            'SCRIPTS_DIR': wrfda_script_dir,
            'OB_DIR': '$RUN_DIR/ob',
            'FILTERED_OBS_DIR': '$RUN_DIR/ob',
            'BE_DIR': '$RUN_DIR/data',
            'FC_DIR': '$RUN_DIR/fc',
            'WINDOW_START': -3,
            'WINDOW_END': 3,
            'CYCLE_PERIOD': 3,
            'NUM_PROCS': 1,
            'VERIFY_HOUR': fcst_hr_at_verif, # at analysis hour
            'RUN_CMD': '', 
            'VERIFICATION_FILE_STRING': 'wrfout', 
            'NL_ANALYSIS_TYPE': 'verif',
            'NL_E_WE': wrf_domain_config[domain_name]['common']['e_we'],
            'NL_E_SN': wrf_domain_config[domain_name]['common']['e_sn'],
            'NL_E_VERT': wrf_domain_config[domain_name]['wrf']['e_vert'],
            'NL_DX': wrf_domain_config[domain_name]['common']['dx'],           
            'NL_DY': wrf_domain_config[domain_name]['common']['dy'], 
            'NL_SF_SURFACE_PHYSICS': 2,
            'NL_NUM_LAND_CAT': 21, 
            },
        'da_verif_obs_plot':{
            'START_DATE': analysis_date.strftime('%Y%m%d%H'),
            'END_DATE': analysis_date.strftime('%Y%m%d%H'),
            'NUM_EXPT':1,
            'EXP_NAMES':'\'conv_only\'',
            'EXP_LEGENDS':'\'(/"conv_only"/)\'',
            'INTERVAL':3,
            'NUM_PROCS':1,
            'VERIFY_HOUR': wrfda_verif_hour,
            'GRAPHICS_DIR': '\'' + wrfda_graphic_dir + '\'',
            'WRF_FILE': '\'$RUN_DIR/fc\'',
            'Verify_Date_Range': '\'{} - {} at the hour of {}\''.format(start_date.strftime('%Y%m%d%H'), end_date.strftime('%Y%m%d%H'), wrfda_verif_hour),
            'OBS_TYPES':'\'synop sound\'',
            'NUM_OBS_TYPES':2,
            'PLOT_WKS':'pdf',
            }
    }
    target = open('{}/verif_obs_wrapper.ksh'.format(verif_obs_wrapper_dir), 'w')
    
    
    target.write('#!/bin/ksh -aeu')
    target.write('\n')
    target.write('\n')
    target.write('# if you run the system in serial mode, you need to change the line of 408 in: \n# \
                      ***TOOLS/var/scripts/da_run_wrfvar.ksh/verif_obs_wrapper.ksh*** \n# \
                         -> remove $RUN_CMD from $RUN_CMD ./da_wrfvar.exe')
    target.write('\n')
    target.write('\n')
    
    target.write('export EXP_DIR={}/exp'.format(verif_obs_wrapper_dir) + '\n')
    target.write('export RUN_DIR={}'.format(verif_obs_wrapper_dir) + '\n')

    for r1 in namelist_field['da_run_suite_verif_obs'].keys():
        target.write('export {}={}'.format(r1, namelist_field['da_run_suite_verif_obs'][r1]) + '\n')
    target.write('\n')
    target.write('{}/da_run_suite_verif_obs.ksh \n'.format(wrfda_script_dir))

    target.write('\n')

    for r1 in namelist_field['da_verif_obs_plot'].keys():
        target.write('export {}={}'.format(r1, namelist_field['da_verif_obs_plot'][r1]) + '\n')
    target.write('\n')
    target.write('{}/da_verif_obs_plot.ksh \n'.format(wrfda_script_dir))   
    target.close()
    

def wrfda_namelist(start_date, end_date,
                   analysis_datetime,
                   domain_name,
                   working_dir,
                   wrfda_qcobs = None,
                   wrfda_verif = None):
    """create the wrfda namelist
    """
    
    analysis_datetime_min = analysis_datetime - datetime.timedelta(seconds = 3600)
    analysis_datetime_max = analysis_datetime + datetime.timedelta(seconds = 3600)
    namelist_keys_order = ['&wrfvar{}'.format(i) for i in range(1,23)]
    namelist_keys_order.extend(['&time_control','&fdda','&domains','&dfi_control', \
                                '&tc','&physics','&scm','&dynamics','&bdy_control','&grib2', \
                                '&fire','&namelist_quilt','&perturbation'])
    namelist_field = {
        '&wrfvar1': {'var4d': False,
                     'print_detail_grad': False,
                      },
        '&wrfvar2': {},
        '&wrfvar3': {'ob_format': 2,
                     },
        '&wrfvar4': {},
        '&wrfvar5': {},
        '&wrfvar6': {'max_ext_its': 1,
                     'ntmax':50,
                     'orthonorm_gradient': True,
                     },
        '&wrfvar7': {'cv_options': 3,
                    },
        '&wrfvar8': {},
        '&wrfvar9': {},
        '&wrfvar10': {'test_transforms': False,
                      'test_gradient': False
                      },
        '&wrfvar11': {},
        '&wrfvar12': {},     
        '&wrfvar13': {},
        '&wrfvar14': {},
        '&wrfvar15': {},
        '&wrfvar16': {},
        '&wrfvar17': {},
        '&wrfvar18': {'analysis_date':datetime.datetime.strftime(analysis_datetime,'%Y-%m-%d_%H:%M:%S.0000'),
                      },
        '&wrfvar19': {},
        '&wrfvar20': {},    
        '&wrfvar21': {'time_window_min':datetime.datetime.strftime(analysis_datetime_min,'%Y-%m-%d_%H:%M:%S.0000'),
                      },
        '&wrfvar22': {'time_window_max':datetime.datetime.strftime(analysis_datetime_max,'%Y-%m-%d_%H:%M:%S.0000'),
                      },
        '&time_control':{'start_year': start_date.year,
                     'start_month':start_date.month,
                     'start_day': start_date.day,
                     'start_hour': start_date.hour,
                     'end_year': end_date.year,
                     'end_month': end_date.month,
                     'end_day': end_date.day,
                     'end_hour': end_date.hour,
                     },
        '&fdda':{},
        '&domains':{'e_we': wrf_domain_config[domain_name]['common']['e_we'],
                    'e_sn': wrf_domain_config[domain_name]['common']['e_sn'],
                    'e_vert': wrf_domain_config[domain_name]['wrf']['e_vert'],
                    'dx': wrf_domain_config[domain_name]['common']['dx'],
                    'dy': wrf_domain_config[domain_name]['common']['dy'],       
                    },
        '&dfi_control':{},
        '&tc':{},
        '&physics':{
                    'mp_physics': 3,
                    'ra_lw_physics': 1,
                    'ra_sw_physics': 1,
                    'radt': 30,
                    'sf_sfclay_physics': 1,
                    'sf_surface_physics': 2,
                    'bl_pbl_physics': 1,
                    'cu_physics': 1,
                    'cudt': 5,
                    'num_soil_layers': 5,
                    'mp_zero_out': 2,
                    'co2tf': 0,
                    },
        '&scm':{},
        '&dynamics':{},
        '&bdy_control':{},
        '&grib2':{},
        '&fire':{},
        '&namelist_quilt':{},
        '&perturbation':{},
        }

    if wrfda_qcobs:
        namelist_field.update({'&wrfvar17': {'analysis_type': 'QC-OBS'}})
    if wrfda_verif:
        namelist_field.update({'&wrfvar17': {'analysis_type': 'VERIFY'}})


    target = open('{}/namelist.input'.format(working_dir), 'w')
    for r1 in namelist_keys_order:
        target.write(r1 + '\n')
        for r2 in namelist_field[r1].keys():
            if isinstance((namelist_field[r1][r2]), bool):
                target.write(' ' + r2 + '=.' + str(namelist_field[r1][r2]).upper() + '., \n')
            elif isinstance((namelist_field[r1][r2]), list):
                target.write(' ' + r2 + '=')
                for index, v in enumerate(namelist_field[r1][r2]):
                    target.write(str(v) + ', ')
                    if index == len(namelist_field[r1][r2]):
                        target.write('\n')
            else:
                if str(namelist_field[r1][r2])[0] == '-' or str(namelist_field[r1][r2])[0].isdigit() and (r2 != 'start_date') and (r2 != 'end_date'):
                    target.write(' ' + r2 + '=' + str(namelist_field[r1][r2]) + ', \n')
                else:
                    target.write(' ' + r2 + '=\'' + str(namelist_field[r1][r2]) + '\', \n')
        target.write('/')
        target.write('\n')
    target.close()

def obsproc_namelist(obsfile_path, obserr_path, domain_name,
                     analysis_datetime,
                     working_dir):
    """create the obsproc namelist
    """
    
    analysis_datetime_min = analysis_datetime - datetime.timedelta(seconds = 3600)
    analysis_datetime_max = analysis_datetime + datetime.timedelta(seconds = 3600)
    namelist_keys_order = ['&record{}'.format(i) for i in range(1,10)]
    namelist_field = {
        '&record1': {'obs_gts_filename': obsfile_path,
                     'obs_err_filename': obserr_path,
                      'gts_from_mmm_archive': False
                      },
        '&record2':{ 'time_window_min': datetime.datetime.strftime(analysis_datetime_min,'%Y-%m-%d_%H:%M:%S'),
                     'time_analysis': datetime.datetime.strftime(analysis_datetime,'%Y-%m-%d_%H:%M:%S'),
                     'time_window_max': datetime.datetime.strftime(analysis_datetime_max,'%Y-%m-%d_%H:%M:%S'),
                     },
        '&record3': { 'max_number_of_obs': 400000, 
                     'fatal_if_exceed_max_obs': True,
                     },
        '&record4': {'qc_test_vert_consistency': True,
                     'qc_test_convective_adj':True,
                     'qc_test_above_lid': True,
                     'remove_above_lid': False,
                     'domain_check_h': True,
                     'Thining_SATOB':False,
                     'Thining_SSMI':False,
                     'Thining_QSCAT':False,
                     'calc_psfc_from_qnh':True,
                     },
        '&record5': {'print_gts_read': True,
                     'print_gpspw_read':True,
                     'print_recoverp': True,
                     'print_duplicate_loc': True,
                     'print_duplicate_time': True,
                     'print_recoverh':True,
                     'print_qc_vert':True,
                     'print_qc_conv':True,
                     'print_qc_lid':True,
                     'print_uncomplete':True,
                     },
        '&record6': {'ptop': 1000.0,
                     'base_pres':100000.0,
                     'base_temp': 290.0,
                     'base_lapse': 50.0,
                     'base_strat_temp': 215.0,
                     'base_tropo_pres':20000.0,
                     },
        '&record7': {'IPROJ': 3,
                     'PHIC':wrf_domain_config[domain_name]['wps']['ref_lat'],
                     'XLONC': wrf_domain_config[domain_name]['wps']['ref_lon'],
                     'TRUELAT1': wrf_domain_config[domain_name]['wps']['truelat1'],
                     'TRUELAT2': wrf_domain_config[domain_name]['wps']['truelat2'],
                     'MOAD_CEN_LAT':wrf_domain_config[domain_name]['wps']['ref_lat'],
                     'STANDARD_LON':wrf_domain_config[domain_name]['wps']['ref_lon'],
                     },
        '&record8': {'IDD': 1,
                     'MAXNES':1,
                     'NESTIX': wrf_domain_config[domain_name]['common']['e_we'],
                     'NESTJX': wrf_domain_config[domain_name]['common']['e_sn'],
                     'DIS':  wrf_domain_config[domain_name]['common']['dx'],
                     'NUMC': 1,
                     'NESTI': 1,
                     'NESTJ': 1,
                     },
        '&record9': {'PREPBUFR_OUTPUT_FILENAME': 'prepbufr_output_filename',
                     'PREPBUFR_TABLE_FILENAME':'prepbufr_table_filename',
                     'OUTPUT_OB_FORMAT': 2,
                     'use_for': '3DVAR',
                     'num_slots_past': 3,
                     'num_slots_ahead': 3,
                     'write_synop': True,
                     'write_ship': True,
                     'write_metar': True,
                     'write_buoy': True,
                     'write_pilot': True,
                     'write_sound': True,
                     'write_amdar': True,
                     'write_satem': True,
                     'write_satob': True,
                     'write_airep': True,
                     'write_gpspw': True,
                     'write_gpsztd': True,
                     'write_gpsref': True,
                     'write_gpseph': True,
                     'write_ssmt1': True,
                     'write_ssmt2': True,
                     'write_ssmi': True,
                     'write_tovs': True,
                     'write_qscat': True,
                     'write_profl': True,
                     'write_bogus': True,
                     'write_airs': True,
                     },
        }
    
    target = open('{}/namelist.obsproc'.format(working_dir), 'w')
    for r1 in namelist_keys_order:
        target.write(r1 + '\n')
        for r2 in namelist_field[r1].keys():
            if isinstance((namelist_field[r1][r2]), bool):
                target.write(' ' + r2 + '=.' + str(namelist_field[r1][r2]).upper() + '., \n')
            elif isinstance((namelist_field[r1][r2]), list):
                target.write(' ' + r2 + '=')
                for index, v in enumerate(namelist_field[r1][r2]):
                    target.write(str(v) + ', ')
                    if index == len(namelist_field[r1][r2]):
                        target.write('\n')
            else:
                if str(namelist_field[r1][r2])[0] == '-' or str(namelist_field[r1][r2])[0].isdigit() and (r2 != 'start_date') and (r2 != 'end_date'):
                    target.write(' ' + r2 + '=' + str(namelist_field[r1][r2]) + ', \n')
                else:
                    target.write(' ' + r2 + '=\'' + str(namelist_field[r1][r2]) + '\', \n')
        target.write('/')
        target.write('\n')
    target.close()


def wps_namelist(domain_name,\
                 start_date, end_date, \
                 met_intervals_sec,
                 working_dir,
                 geog_data_path, tbl_path):
    """create the wps namelist
    """
    namelist_keys_order = ['&share','&geogrid','&ungrib','&metgrid','&mod_levs']
    namelist_field = {
        '&share': {'wrf_core': 'ARW', 'max_dom':1,
                     'start_date':'2017-05-01_00:00:00','end_date':'2017-05-01_06:00:00',
                      'interval_seconds': 10800,
                      'io_form_geogrid': 2,
                      'opt_output_from_geogrid_path': '/home/szhang/workspace_wrf/NZ_test_20170517/',
                      'debug_level': 0,},
        '&geogrid':{ 'parent_id': 1,
                     'parent_grid_ratio': 1,
                     'i_parent_start': 1,
                     'j_parent_start': 1,
                     'e_we': wrf_domain_config[domain_name]['common']['e_we'],
                     'e_sn': wrf_domain_config[domain_name]['common']['e_sn'],
                     'geog_data_res': '10m',
                     'dx': wrf_domain_config[domain_name]['common']['dx'],
                     'dy': wrf_domain_config[domain_name]['common']['dy'],
                     'map_proj': 'mercator',
                     'ref_lat': wrf_domain_config[domain_name]['wps']['ref_lat'],
                     'ref_lon': wrf_domain_config[domain_name]['wps']['ref_lon'],
                     'truelat1': wrf_domain_config[domain_name]['wps']['truelat1'],
                     'truelat2':  wrf_domain_config[domain_name]['wps']['truelat2'],
                     'stand_lon': wrf_domain_config[domain_name]['wps']['stand_lon'],
                     'geog_data_path': geog_data_path,
                     #'geog_data_path': '/home/szhang/Programs/WRF_sample_data/geog_complete/geog',
                     'opt_geogrid_tbl_path':  tbl_path,
                     'ref_x': wrf_domain_config[domain_name]['wps']['ref_x'],
                     'ref_y': wrf_domain_config[domain_name]['wps']['ref_y']},
        '&ungrib': { 'out_format': 'WPS', 'prefix': 'FILE'},
        '&metgrid': {'fg_name': 'FILE',
                     'io_form_metgrid':2,
                     'opt_output_from_metgrid_path': working_dir,
                     'opt_metgrid_tbl_path':tbl_path},
        '&mod_levs': {'press_pa': wrf_domain_config[domain_name]['wps']['press_pa']},   
        }
    
    namelist_field['&share']['start_date'] =  start_date.strftime('%Y-%m-%d_%H:00:00')
    namelist_field['&share']['end_date'] =  end_date.strftime('%Y-%m-%d_%H:00:00')
    namelist_field['&share']['opt_output_from_geogrid_path'] =  working_dir
    namelist_field['&share']['interval_seconds'] =  met_intervals_sec
    namelist_field['&metgrid']['opt_output_from_metgrid_path'] =  working_dir
    
    target = open('{}/namelist.wps'.format(working_dir), 'w')
    for r1 in namelist_keys_order:
        target.write(r1 + '\n')
        for r2 in namelist_field[r1].keys():
            if isinstance((namelist_field[r1][r2]), bool):
                target.write(' ' + r2 + '=.' + str(namelist_field[r1][r2]).upper() + '., \n')
            if isinstance((namelist_field[r1][r2]), list):
                target.write(' ' + r2 + '=')
                for index, v in enumerate(namelist_field[r1][r2]):
                    target.write(str(v) + ', ')
                    if index == len(namelist_field[r1][r2]):
                        target.write('\n')
            else:
                if str(namelist_field[r1][r2])[0] == '-' or str(namelist_field[r1][r2])[0].isdigit() and (r2 != 'start_date') and (r2 != 'end_date'):
                    target.write(' ' + r2 + '=' + str(namelist_field[r1][r2]) + ', \n')
                else:
                    target.write(' ' + r2 + '=\'' + str(namelist_field[r1][r2]) + '\', \n')
        target.write('/')
        target.write('\n')
    target.close()


def wrf_namelist(domain_name, \
                 start_date, end_date, \
                 fdda_index,\
                 working_dir):
    """create the wps namelist
    """
    run_hours = int((end_date - start_date).total_seconds()/3600.0)
    namelist_keys_order = ['&time_control','&domains','&physics','&fdda','&dynamics','&bdy_control','&grib2','&namelist_quilt']
    namelist_field = {
        '&time_control': {
                            'run_days':0,
                            'run_hours': run_hours,
                            'run_minutes': 0,
                            'run_seconds': 0,
                            'start_year': 2017,
                            'start_month': 5,
                            'start_day': 17,
                            'start_hour': 0,
                            'start_minute': 0,
                            'start_second': 0,
                            'end_year': 2017,
                            'end_month': 5,
                            'end_day': 17,
                            'end_hour': 6,
                            'end_minute': 0,
                            'end_second': 0,
                            'interval_seconds': 10800,
                            'input_from_file': True,
                            'history_interval': 60,
                            'frames_per_outfile': 1,
                            'restart': False,
                            'restart_interval': 5000,
                            'io_form_history': 2,
                            'io_form_restart': 2,
                            'io_form_input': 2,
                            'io_form_boundary': 2,
                            'debug_level': 0,
                            },
        '&domains':{
                    'time_step': 60,
                    'time_step_fract_num': 0,
                    'time_step_fract_den': 1,
                    'max_dom': 1,
                    'e_we': wrf_domain_config[domain_name]['common']['e_we'],
                    'e_sn': wrf_domain_config[domain_name]['common']['e_sn'],
                    'e_vert': wrf_domain_config[domain_name]['wrf']['e_vert'],
                    'p_top_requested': wrf_domain_config[domain_name]['wrf']['p_top_requested'],
                    'num_metgrid_levels': 32,
                    'num_metgrid_soil_levels': 4,
                    'dx': wrf_domain_config[domain_name]['common']['dx'],
                    'dy': wrf_domain_config[domain_name]['common']['dy'],
                    'grid_id': 1,
                    'parent_id': 1,
                    'i_parent_start': 1,
                    'j_parent_start': 1,
                    'parent_grid_ratio': 1,
                    'parent_time_step_ratio': 1,
                    'feedback': 1,
                    'smooth_option': 0,
                    },
        '&physics': {
                    'mp_physics': 3,
                    'ra_lw_physics': 1,
                    'ra_sw_physics': 1,
                    'radt': 30,
                    'sf_sfclay_physics': 1,
                    'sf_surface_physics': 2,
                    'bl_pbl_physics': 1,
                    'bldt': 0,
                    'cu_physics': 1,
                    'cudt': 5,
                    'isfflx': 1,
                    'ifsnow': 0,
                    'icloud': 1,
                    'surface_input_source': 1,
                    'num_soil_layers': 4,
                    'sf_urban_physics': 0,
                    'maxiens': 1,
                    'maxens': 3,
                    'maxens2': 3,
                    'maxens3': 16,
                    'ensdim': 144,
                    },
        '&dynamics': {'w_damping': 0,
                      'diff_opt': 1,
                      'km_opt': 4,
                      'diff_6th_opt': 0,
                      'diff_6th_factor': 0.12,
                      'base_temp': 290.,
                      'damp_opt': 0,
                      'zdamp': 5000.,
                      'dampcoef': 0.2,
                      'khdif': 0,
                      'kvdif': 0,
                      'non_hydrostatic': True,
                      'moist_adv_opt': 1,
                      'scalar_adv_opt': 1
                      },
        '&bdy_control': {
                    'spec_bdy_width': 5,
                    'spec_zone': 1,
                    'relax_zone': 4,
                    'specified': True,
                    'nested': False
                    },
        '&grib2': {},
        '&namelist_quilt': {
                    'nio_tasks_per_group': 0,
                    'nio_groups': 1
                    },
        }

    fdda_secontion = {
        '&fdda': {
                 'grid_fdda': 1,
                 'gfdda_inname': 'wrffdda_d<domain>',
                 'gfdda_interval_m': 180,
                 'gfdda_end_h': 60,
                 'grid_sfdda': 0,
                 'sgfdda_inname': 'wrfsfdda_d<domain>',
                 'sgfdda_interval_m': 60,
                 'sgfdda_interval_s': 3600,
                 'sgfdda_end_h': 0,
                 'io_form_gfdda': 2,
                 'fgdt':0,
                 'if_no_pbl_nudging_uv': 0,
                 'if_no_pbl_nudging_t': 1,
                 'if_no_pbl_nudging_q': 1,
                 'if_zfac_uv': 0,
                 'k_zfac_uv': 10,
                 'if_zfac_t': 1,
                 'k_zfac_t': 10,
                 'if_zfac_q': 1,
                 'k_zfac_q': 10,
                 'guv': 0.000300,
                 'gt': 0.000300,
                 'gq': 0.000300,
                 'if_ramping': 0,
                 'dtramp_min': 0.000000,
                 'obs_nudge_opt': 1,
                 'max_obs': 150000,
                 'fdda_start': 0.000000, 
                 'fdda_end': 600,
                 'obs_nudge_wind': 1,
                 'obs_coef_wind': 0.000600,
                 'obs_nudge_temp': 1,
                 'obs_coef_temp': 0.000600,
                 'obs_nudge_mois': 1,
                 'obs_coef_mois': 0.000600,
                 'obs_rinxy': 120.000000,
                 'obs_rinsig': 0.100000,
                 'obs_twindo': 0.666666,
                 'obs_npfi': 10,
                 'obs_ionf': 2,
                 'obs_idynin': 0,
                 'obs_dtramp': 40.000000,
                 'obs_prt_freq': 10,
                 'obs_ipf_errob': True,
                 'obs_ipf_nudob': True,
                 'obs_ipf_in4dob': True,
            }
        }
    if fdda_index:
        namelist_field.update(fdda_secontion)
    else:
        namelist_field.update({'&fdda':{}})

    for j in ['year','month','day','hour']:
        namelist_field['&time_control']['start_'+j] = getattr(start_date,j)
        namelist_field['&time_control']['end_'+j] = getattr(end_date,j)
    
    target = open('{}/namelist.input'.format(working_dir), 'w')
    for r1 in namelist_keys_order:
        target.write(r1 + '\n')
        for r2 in namelist_field[r1].keys():
            if isinstance((namelist_field[r1][r2]), bool):
                target.write(' ' + r2 + '=.' + str(namelist_field[r1][r2]).upper() + '., \n')
            elif isinstance((namelist_field[r1][r2]), list):
                target.write(' ' + r2 + '=')
                for index, v in enumerate(namelist_field[r1][r2]):
                    target.write(str(v) + ', ')
                    if index == len(namelist_field[r1][r2]):
                        target.write('\n')
            else:
                if str(namelist_field[r1][r2])[0] == '-' or str(namelist_field[r1][r2])[0].isdigit() and (r2 != 'start_date') and (r2 != 'end_date'):
                    target.write(' ' + r2 + '=' + str(namelist_field[r1][r2]) + ', \n')
                else:
                    target.write(' ' + r2 + '=\'' + str(namelist_field[r1][r2]) + '\', \n')
        target.write('/')
        target.write('\n')
    target.close()

