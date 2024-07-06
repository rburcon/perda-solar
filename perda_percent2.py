#!/usr/bin/env xdg-open
# coding: utf-8

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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


root = Tk()
root.wm_title("Energy loss - clean sky model")

def compute():
            
    latitude_id=float(latitude.get())
    longitude_id=float(longitude.get())
    ang_painel_id=float(ang_painel.get())
    azimute_id=float(azimute.get())
    fuso=box.get()
   
    
    
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
          
          
          
          
   


    tota=(1-(((total_cor.poa_global.sum())/365)/((total.poa_global.sum())/365)))*100
    print("\nFor the panel angle of %.2f° and azimuth of %.2f°, we have a loss of %.2f%%" %(ang_painel_id, surf_az, tota))
    resp=("\nFor the panel angle of %.2f° and azimuth of %.2f°, we have a loss of %.2f%%" %(ang_painel_id, surf_az, tota))
    #messagebox.showinfo("Loss %", resp)

def sobre():
    from tkinter import messagebox
    var = messagebox.showinfo("Info" , "Solar radiation clear sky model - rburcon@gmail.com")









Label(root, text="Latitude").grid(row=0, sticky=W)
Label(root, text="Longitude").grid(row=1, sticky=W)
Label(root, text="Panel tilt").grid(row=2, sticky=W)
Label(root, text="Azimuth").grid(row=3, sticky=W)
Label(root, text="Timezone").grid(row=4, sticky=W)

latitude=Entry(root)
latitude.grid(row=0, column=1, sticky=E)
latitude.insert(0,"-23.54")
longitude=Entry(root)
longitude.insert(0,"-51.68")
longitude.grid(row=1, column=1, sticky=E)
ang_painel=Entry(root)
ang_painel.grid(row=2, column=1, sticky=E)
ang_painel.insert(0,"23.54")
azimute=Entry(root)
azimute.grid(row=3, column=1, sticky=E)
azimute.insert(0,"0")
value = StringVar()
box = ttk.Combobox(root, textvariable=value,width=18, state='readonly')

box['values'] = ('America/Noronha', 'America/Bahia', 'America/Manaus', 'America/Rio_Branco')
box.current(1)
box.grid(column=1, row=4)




Button(root, text="   Calc ", command=compute).grid(row=3, column=2, sticky=E)

Button(root, text="  About", command=sobre).grid(row=4, column=2, sticky=E)


root.mainloop()





















