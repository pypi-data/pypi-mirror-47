# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#ADD TWO ARRAYS
#add two tvar data arrays, store in new_tvar
def add(tvar1,tvar2,new_tvar=None,interp='linear'):
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and add data
    time = pytplot.data_quants[tv1].data.index.copy()
    data1 = pytplot.data_quants[tv1].data.copy()
    data2 = pytplot.data_quants[tv2].data.copy()
    data = data1+data2
    
    if new_tvar == None:
        new_tvar = tvar1 + '_+_' + tvar2
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar