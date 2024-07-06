#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:17:32 2022

@author: rburcon
"""

import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set(rc={'figure.figsize':(12,6)})
except ImportError:
    pass
    
# built in python modules
import datetime

# python add-ons
import numpy as np
import pandas as pd

import pvlib


angulo_painel=[0,10,20,30,40,50,60,70,80,90]
angulo_azimute=[-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90]
valores=np.zeros((len(angulo_painel),len(angulo_azimute)), dtype=np.float64)
px=0
py=0

for angulo in angulo_painel:
    
    for angulo_eixo in angulo_azimute:

        latitude_id=-20.0
        longitude_id=-52.0
        ang_painel_id=angulo
        azimute_id=angulo_eixo
        fuso='America/Bahia'
        
        
        
        tus = pvlib.location.Location(latitude_id, longitude_id, fuso, 600, 'Maringá')
        times = pd.date_range(start='2017-01-01', end='2018-01-01', freq='60min', tz=tus.tz)
        ephem_data = tus.get_solarposition(times)
        irrad_data = tus.get_clearsky(times)
        
        
        surf_tilt = ang_painel_id
        surf_az = azimute_id # 0 Apontado para o norte 180 apontado para o sul
        
        iso_diffuse = pvlib.irradiance.isotropic(surf_tilt, irrad_data['dhi'])
        
        
        klucher_diffuse = pvlib.irradiance.klucher(surf_tilt, surf_az, 
                                                irrad_data['dhi'], irrad_data['ghi'], 
                                                ephem_data['apparent_zenith'], ephem_data['azimuth'])
        
        
        dni_et = pvlib.irradiance.get_extra_radiation(times.dayofyear)
        reindl_diffuse = pvlib.irradiance.reindl(surf_tilt, surf_az, 
                                              irrad_data['dhi'], irrad_data['dni'], irrad_data['ghi'], dni_et,
                                              ephem_data['apparent_zenith'], ephem_data['azimuth'])
        
        
        sun_zen = ephem_data['apparent_zenith']
        AM = pvlib.atmosphere.get_relative_airmass(sun_zen)
        
        
        
        totals = {}
        model='isotropic'
        
        total = pvlib.irradiance.get_total_irradiance(abs(latitude_id), 0, 
                                               ephem_data['apparent_zenith'], ephem_data['azimuth'],
                                               dni=irrad_data['dni'], ghi=irrad_data['ghi'], dhi=irrad_data['dhi'],
                                               dni_extra=dni_et, airmass=AM,
                                               model='isotropic',
                                               surface_type='urban')
        totals[model] = total
         
        totals_cor = {}      
        total_cor = pvlib.irradiance.get_total_irradiance(ang_painel_id, surf_az, 
                                               ephem_data['apparent_zenith'], ephem_data['azimuth'],
                                               dni=irrad_data['dni'], ghi=irrad_data['ghi'], dhi=irrad_data['dhi'],
                                               dni_extra=dni_et, airmass=AM,
                                               model='isotropic',
                                               surface_type='urban')
        totals_cor[model] = total_cor      
              
              
              
              
        
        
        
        tota=(1-(((total_cor.poa_global.sum())/365)/((total.poa_global.sum())/365)))
        #print("\nFor the panel angle of %.2f° and azimuth of %.2f°, we have a loss of %.2f%%" %(ang_painel_id, surf_az, tota))
        valores[px,py]=tota
        py=py+1
    px=px+1
    py=0
    
