from pytplot import options

def mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=''):
    """
    This function updates the metadata for FPI data products
    
    Parameters:
        probe : str or list of str
            probe or list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FPI include 'brst' and 'fast'. The
            default is 'fast'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

    """
    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]
    if not isinstance(level, list): level = [level]

    probe = [str(p) for p in probe]
    
    for this_probe in probe:
        for this_dr in data_rate:
            for this_lvl in level:
                for this_dtype in datatype:
                    if this_dtype == 'des-moms':
                        options('mms'+this_probe+'_des_energyspectr_par_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (eV)')
                        options('mms'+this_probe+'_des_energyspectr_anti_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (eV)')
                        options('mms'+this_probe+'_des_energyspectr_perp_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (eV)')
                        options('mms'+this_probe+'_des_energyspectr_omni_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (eV)')

                        options('mms'+this_probe+'_des_energyspectr_par_'+this_dr+suffix, 'ylog', True)
                        options('mms'+this_probe+'_des_energyspectr_par_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_energyspectr_par_'+this_dr+suffix, 'Colormap', 'jet')
                        
                        options('mms'+this_probe+'_des_energyspectr_anti_'+this_dr+suffix, 'ylog', True)
                        options('mms'+this_probe+'_des_energyspectr_anti_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_energyspectr_anti_'+this_dr+suffix, 'Colormap', 'jet')
                        
                        options('mms'+this_probe+'_des_energyspectr_perp_'+this_dr+suffix, 'ylog', True)
                        options('mms'+this_probe+'_des_energyspectr_perp_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_energyspectr_perp_'+this_dr+suffix, 'Colormap', 'jet')
                        
                        options('mms'+this_probe+'_des_energyspectr_omni_'+this_dr+suffix, 'ylog', True)
                        options('mms'+this_probe+'_des_energyspectr_omni_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_energyspectr_omni_'+this_dr+suffix, 'Colormap', 'jet')
                        
                        options('mms'+this_probe+'_des_pitchangdist_lowen_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_pitchangdist_lowen_'+this_dr+suffix, 'Colormap', 'jet')

                        options('mms'+this_probe+'_des_pitchangdist_miden_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_pitchangdist_miden_'+this_dr+suffix, 'Colormap', 'jet')

                        options('mms'+this_probe+'_des_pitchangdist_highen_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_des_pitchangdist_highen_'+this_dr+suffix, 'Colormap', 'jet')

                        options('mms'+this_probe+'_des_pitchangdist_lowen_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (deg)')
                        options('mms'+this_probe+'_des_pitchangdist_miden_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (deg)')
                        options('mms'+this_probe+'_des_pitchangdist_highen_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES (deg)')

                        options('mms'+this_probe+'_des_energyspectr_par_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')
                        options('mms'+this_probe+'_des_energyspectr_anti_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')
                        options('mms'+this_probe+'_des_energyspectr_perp_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')
                        options('mms'+this_probe+'_des_energyspectr_omni_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')

                        options('mms'+this_probe+'_des_pitchangdist_lowen_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')
                        options('mms'+this_probe+'_des_pitchangdist_miden_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')
                        options('mms'+this_probe+'_des_pitchangdist_highen_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')


                        options('mms'+this_probe+'_des_bulkv_dbcs_'+this_dr+suffix, 'color', ['b', 'g', 'r'])
                        options('mms'+this_probe+'_des_bulkv_gse_'+this_dr+suffix, 'color', ['b', 'g', 'r'])

                        options('mms'+this_probe+'_des_bulkv_gse_'+this_dr+suffix, 'legend_names', ['Vx GSE', 'Vy GSE', 'Vz GSE'])
                        options('mms'+this_probe+'_des_bulkv_dbcs_'+this_dr+suffix, 'legend_names', ['Vx DBCS', 'Vy DBCS', 'Vz DBCS'])
                        options('mms'+this_probe+'_des_bulkv_gse_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES velocity (km/s)')
                        options('mms'+this_probe+'_des_bulkv_dbcs_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES velocity (km/s)')
                        options('mms'+this_probe+'_des_numberdensity_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DES density (cm^-3)')
                    elif this_dtype == 'dis-moms':
                        options('mms'+this_probe+'_dis_energyspectr_omni_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DIS (eV)')
                        options('mms'+this_probe+'_dis_energyspectr_omni_'+this_dr+suffix, 'ylog', True)
                        options('mms'+this_probe+'_dis_energyspectr_omni_'+this_dr+suffix, 'zlog', True)
                        options('mms'+this_probe+'_dis_energyspectr_omni_'+this_dr+suffix, 'Colormap', 'jet')
                        options('mms'+this_probe+'_dis_energyspectr_omni_'+this_dr+suffix, 'ztitle', '[keV/(cm^2 s sr keV)]')

                        options('mms'+this_probe+'_dis_bulkv_dbcs_'+this_dr+suffix, 'color', ['b', 'g', 'r'])
                        options('mms'+this_probe+'_dis_bulkv_gse_'+this_dr+suffix, 'color', ['b', 'g', 'r'])

                        options('mms'+this_probe+'_dis_bulkv_gse_'+this_dr+suffix, 'legend_names', ['Vx GSE', 'Vy GSE', 'Vz GSE'])

                        options('mms'+this_probe+'_dis_bulkv_dbcs_'+this_dr+suffix, 'legend_names', ['Vx DBCS', 'Vy DBCS', 'Vz DBCS'])

                        options('mms'+this_probe+'_dis_bulkv_gse_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DIS velocity (km/s)')
                        options('mms'+this_probe+'_dis_bulkv_dbcs_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DIS velocity (km/s)')

                        options('mms'+this_probe+'_dis_numberdensity_'+this_dr+suffix, 'ytitle', 'MMS'+this_probe+' DIS density (cm^-3)')




