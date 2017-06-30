wrf_domain_config = {
    'debug_domain':
    {
        'common':{
            'e_we': 26,
            'e_sn': 31,
            'dx': 10000,
            'dy': 10000,
            },
        
        'wps': {
                'ref_lat': -39.943,
                'ref_lon': 174.453,
                'truelat1': -39.943,
                'truelat2':  0,
                'stand_lon': 174.453,
                'ref_x': 13.0,
                'ref_y': 15.5,
                'press_pa': [201300 , 200100 , 100000 ,
                                     95000 ,  90000 ,
                                     85000 ,  80000 ,
                                     75000 ,  70000 ,
                                     65000 ,  60000 ,
                                     55000 ,  50000 ,
                                     45000 ,  40000 ,
                                     35000 ,  30000 ,
                                     25000 ,  20000 ,
                                     15000 ,  10000 ,
                                      5000 ,   1000]
            },
     
        'wrf':{
                'e_vert': 28,
                'p_top_requested': 25000,
                'num_metgrid_levels': 32,
                'num_metgrid_soil_levels': 4,
            },
    }   
}