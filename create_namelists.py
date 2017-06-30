import datetime
from wrf_domain_config import wrf_domain_config

def wps_namelist(domain_name,\
                 start_date, end_date, \
                 met_intervals_sec,
                 working_dir):
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
                     'geog_data_path': '/home/szhang/Programs/WRF_sample_data/geog_complete/geog',
                     'opt_geogrid_tbl_path':  '/home/szhang/workspace_wrf/standard_namelist/WPS_TBL/',
                     'ref_x': wrf_domain_config[domain_name]['wps']['ref_x'],
                     'ref_y': wrf_domain_config[domain_name]['wps']['ref_y']},
        '&ungrib': { 'out_format': 'WPS', 'prefix': 'FILE'},
        '&metgrid': {'fg_name': 'FILE',
                     'io_form_metgrid':2,
                     'opt_output_from_metgrid_path': '/home/szhang/workspace_wrf/NZ_test_20170517/',
                     'opt_metgrid_tbl_path':'/home/szhang/workspace_wrf/standard_namelist/WPS_TBL/'},
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
    namelist_field.update(fdda_secontion)

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

