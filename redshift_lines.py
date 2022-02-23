import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title('Spectral lines: in which S-PLUS band we observe them?')

mycwd = os.path.abspath(os.getcwd())
filters_path = os.path.join(mycwd, 'filters')

ls = {'Ly_alpha': 1215.24, 'C_IV': 1549.48, 'C_III': 1908.734,
        'Mg_II': 2799.117, 'H_gamma': 4341.68, 'H_beta': 4862.68, 'H_alpha': 6564.61}

names = ['uJAVA', 'F0378', 'F0395', 'F0410', 'F0430', 'gSDSS',
            'F0515', 'rSDSS', 'F0660', 'iSDSS', 'F0861', 'zSDSS']

def redshift(l, l_obs):
    return (l_obs - l) / l

def l_obs(l, z):
    return (z*l + l)

def lambdas_obs(z):
    
    d = {}
    for l in ls:
        d[l] = l_obs(ls[l], z)
    
    return d

def loc_lines(z, zline=False, lobs_lines=False):

    fig, ax = plt.subplots(figsize=(12, 7))

    filter_colors = ['#030381', '#a426da', '#0000ff', '#2c97ff', '#09c1c1', '#53e3d5',
            '#33ff33', '#aeff33', '#ffb020', '#ff8c00', '#ff8c00', '#ff0000']
    lines_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for i in range(len(names)):
        
        filter_path = os.path.join(filters_path, f'{names[i]}.dat')
        df = pd.read_csv(filter_path, sep=' ', names=['lambda', names[i]])
        
        if 'F' in names[i]:
            ax.plot(df['lambda'], df[names[i]], c='k', lw=1)
        else:
            ax.plot(df['lambda'], df[names[i]], c='grey', lw=1)
    
    if zline or lobs_lines:
        ax2 = ax.twinx()
        if zline:
            ax2.axhline(z, color='k', lw=1)
        if lobs_lines:
            lobs = np.arange(3000, 10600, 100)
        ax2.set_ylim(0, 8)
        ax2.set_ylabel('Redshift')
         
    i = 0
    lines = lambdas_obs(z)
    for line in lines:
        ax.axvline(lines[line], label=line, c=lines_colors[i])
        if lobs_lines:
            ax2.plot(lobs, redshift(ls[line], lobs), ls='--', lw=1, c=lines_colors[i])
        i += 1

    ax.grid()
    ax.set_ylim(0, 0.8)
    ax.set_xlim(3000, 10500)
    ax.set_xticks(np.arange(3000, 11000, 500))
    ax.set_xlabel('Wavelength (Å)')
    ax.set_ylabel('$R_{\lambda}$ [%]')
    ax.set_title(f'z = {z}', size=16)

    fig.legend(ncol=7, fontsize=12, loc='upper center')
    plt.show()

st.pyplot(loc_lines(st.slider('Redshift', 0, 7, 0, step = 0.01)))

