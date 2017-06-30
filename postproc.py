from mpl_toolkits.basemap import Basemap
from wrf_domain_config import wrf_domain_config
import matplotlib.pyplot as plt
import numpy
import os
from datetime import datetime,timedelta


def plot_the_domain(domain_name, plot_dir):
    # setup Lambert Conformal basemap.
    m = Basemap(width=wrf_domain_config[domain_name]['common']['e_we']*wrf_domain_config[domain_name]['common']['dx'],
                height=wrf_domain_config[domain_name]['common']['e_sn']*wrf_domain_config[domain_name]['common']['dy'],
                projection='lcc',
                resolution='c',
                lat_1=wrf_domain_config[domain_name]['wps']['truelat1'],
                lat_2=wrf_domain_config[domain_name]['wps']['truelat2'],
                lat_0=wrf_domain_config[domain_name]['wps']['ref_lat'],
                lon_0=wrf_domain_config[domain_name]['wps']['ref_lon'])
    # draw coastlines.
    m.drawcoastlines()
    # draw a boundary around the map, fill the background.
    # this background will end up being the ocean color, since
    # the continents will be drawn on top.
    m.drawmapboundary(fill_color='aqua')
    # fill continents, set lake color same as ocean color.
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawparallels(numpy.arange(-90.,91.,0.75),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(numpy.arange(-180.,181.,0.75),labels=[0,0,0,1],fontsize=10)
    plt.title('Domain extracted from the namelist \n projection: lcc')
    plt.savefig(plot_dir + '/' + "wrf_domain_from_namelist.png", bbox_inches='tight')
    plt.close()

def plot_domain_obs_fun(domain_name,lat_list, lon_list, data_list, fm_list,\
                        obs_type, fm_code,\
                        cur_datetime,
                        postproc_dir):
    m = Basemap(width=wrf_domain_config[domain_name]['common']['e_we']*wrf_domain_config[domain_name]['common']['dx'],
                height=wrf_domain_config[domain_name]['common']['e_sn']*wrf_domain_config[domain_name]['common']['dy'],
                projection='lcc',
                resolution='c',
                lat_1=wrf_domain_config[domain_name]['wps']['truelat1'],
                lat_2=wrf_domain_config[domain_name]['wps']['truelat2'],
                lat_0=wrf_domain_config[domain_name]['wps']['ref_lat'],
                lon_0=wrf_domain_config[domain_name]['wps']['ref_lon'])
    m.drawcoastlines()
    m.drawparallels(numpy.arange(-90.,91.,0.75),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(numpy.arange(-180.,181.,0.75),labels=[0,0,0,1],fontsize=10)
    x, y = m(lon_list,lat_list)
    m.scatter(x,y,c=data_list,s=20,marker='o')
    title_str = '{}, {} \n {}'.format(obs_type, fm_code, cur_datetime.strftime('%Y-%m-%d_%H:%M:%S'))
    plt.title(title_str)
    plt.colorbar()
    cpostproc_dir = postproc_dir + '/obsnudge/' + fm_code
    if os.path.exists(cpostproc_dir) == False:
        os.makedirs(cpostproc_dir)
    plt.savefig('{}/{}_{}_{}.png'.format(cpostproc_dir, obs_type, fm_code, cur_datetime.strftime('%Y%m%d_%H%M%S')));
    plt.close()

def plot_domain_obs(domain_name,domain_obs_dict, obs_type, fm_code, start_datetime, end_datetime, postproc_dir):
    cur_datetime = start_datetime
    while cur_datetime <= end_datetime:
        data_list = []
        data_lat_list = []
        data_lon_list = []
        data_fm_list = []
        for i_data in domain_obs_dict:
            if len(i_data[obs_type]) == 1:
                if i_data[obs_type][0] != -888888.0 and i_data['fm_info'] == fm_code and \
                        (i_data['obs_datetime'] < cur_datetime + timedelta(seconds = 1800) and i_data['obs_datetime'] > cur_datetime - timedelta(seconds = 1800)):
                    data_list.append(i_data[obs_type][0])
                    data_lat_list.append(i_data['latitude'])
                    data_lon_list.append(i_data['longitude'])
        if len(data_list) > 0:
            plot_domain_obs_fun(domain_name,data_lat_list, data_lon_list, data_list, data_fm_list, \
                                obs_type, fm_code,
                                cur_datetime,
                                postproc_dir)
        
        cur_datetime = cur_datetime + timedelta(seconds = 3600)
    

def extract_domain_obs(obs_domain_path):
    data_dict = []
    the_first_report = True
    with open(obs_domain_path, "r") as ins:
        for line in ins:
            try:
                cur_data_time = datetime.strptime(line.strip(),'%Y%m%d%H%M%S')
                if the_first_report == False:
                    if new_dict['is_sound'] == 'T':
                        new_dict.update({'pressure': p_data})
                        new_dict.update({'height': h_data})
                        new_dict.update({'temperature': t_data})
                        new_dict.update({'u': u_data})
                        new_dict.update({'v': v_data})
                        new_dict.update({'rh': rh_data})
                    else:
                        raise Exception('sound data is not implemented')
                    data_dict.append(new_dict)
                new_dict = {}
                p_data = []
                h_data = []
                t_data = []
                u_data = []
                v_data = []
                rh_data = []
                line_index = 0
                new_dict.update({'obs_datetime': cur_data_time})
                the_first_report = False
                line_index = line_index + 1
            except:
                if line_index == 1:
                    latlon = [float(cline) for cline in line.split()]
                    new_dict.update({'latitude': latlon[0]})
                    new_dict.update({'longitude': latlon[1]})
                    line_index = line_index + 1
                elif line_index == 2:
                    stn_info = [str(cline) for cline in line.split()]
                    new_dict.update({'station_number': stn_info[0]})
                    new_dict.update({'station_type': stn_info[1]})
                    new_dict.update({'station_geo_hash': stn_info[2]})
                    line_index = line_index + 1
                elif line_index == 3:
                    stn_info2 = [str(cline) for cline in line.split()]
                    new_dict.update({'fm_info': stn_info2[0]})
                    new_dict.update({'terrain_height': stn_info2[1]})
                    new_dict.update({'is_sound': stn_info2[2]})
                    new_dict.update({'is_bogus': stn_info2[3]})
                    new_dict.update({'levels': float(stn_info2[4])})
                    line_index = line_index + 1
                elif line_index > 3:
                    if new_dict['is_sound'] == 'T':
                        sonde_info = [float(cline) for cline in line.split()]
                        p_data.append(sonde_info[0])
                        h_data.append(sonde_info[2])
                        t_data.append(sonde_info[4])
                        u_data.append(sonde_info[6])
                        v_data.append(sonde_info[8])
                        rh_data.append(sonde_info[10])
                        line_index = line_index + 1
                    else:
                        raise Exception('sound data is not implemented')
    return data_dict
                
    