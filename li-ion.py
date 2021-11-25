#!/usr/bin/env python
import sys
import toml
import PySimpleGUI as sg
#import PySimpleGUIQt as sg
import numpy as np
from appdirs import AppDirs
from os import path, makedirs
from pathlib import Path
from version import NAME, APPNAME, GUI, VERSION, AUTHOR

"""
"""
tension = {}
charge = {}
type = {}

type['13S2P'] = 'WILPA 2210'
type['12S2P'] = 'WILPA 2554'
type['12S2Pxlr'] = 'WILPA 3017'
type['10S3P'] = 'WILPA 2475'

tension['10S3P'] = np.array([32, 33.76, 34.61, 35.43, 36.04, 36.47, 36.67, 36.74, 36.77, 36.80, 36.82,
                             36.84, 36.85, 36.87, 36.89, 36.95, 37.06, 37.43, 37.75, 37.90, 38.19,
                             38.89, 39.45, 40.12, 40.94, 41.90, 42])
charge['10S3P'] = np.array([0, 1.6, 2.5, 3.5, 4.5, 5.5, 6.5, 7.4, 8.4, 9.4, 10.4, 11.4, 12.3, 13.3, 14.3,
                            15.3, 16.3, 21.1, 30.9, 40.6, 50.4, 60.2, 70.0, 79.7, 89.5, 99.3, 100])

tension['12S2P'] = np.array([
    50.40,
    50.28,
    49.13,
    48.14,
    47.34,
    46.67,
    45.83,
    45.48,
    45.30,
    44.92,
    44.47,
    44.34,
    44.27,
    44.24,
    44.22,
    44.21,
    44.18,
    44.16,
    44.12,
    44.09,
    44.00,
    43.76,
    43.25,
    42.52,
    41.53,
    40.51,
    38.40])

charge['12S2P'] = np.array([
    100.0,
    99.3,
    89.5,
    79.7,
    70.0,
    60.2,
    50.4,
    40.6,
    30.9,
    21.1,
    16.3,
    15.3,
    14.3,
    13.3,
    12.3,
    11.4,
    10.4,
    9.4,
    8.4,
    7.4,
    6.5,
    5.5,
    4.5,
    3.5,
    2.5,
    1.6,
    0.0])

tension['12S2Pxlr'] = np.array([
 
    50.40,
    48.68,
    47.39,
    46.28,
    45.34,
    44.21,
    43.66,
    42.58,
    41.39,
    41.28,
    41.21,
    41.12,
    41.04,
    40.93,
    40.81,
    40.66,
    40.93,
    40.43,
    40.01,
    39.38,
    38.63])

charge['12S2Pxlr'] = np.array([
    100.0,
    90.1,
    80.2,
    70.4,
    60.5,
    50.6,
    40.7,
    30.9,
    21.0,
    11.1,
    10.1,
    9.1,
    8.1,
    7.1,
    6.2,
    5.2,
    4.2,
    3.2,
    2.2,
    1.2,
    0])

tension['13S2P'] = np.array([
    54.60,
    54.47,
    53.22,
    52.16,
    51.29,
    50.56,
    49.65,
    49.27,
    49.08,
    48.66,
    48.18,
    48.04,
    47.96,
    47.93,
    47.91,
    47.89,
    47.87,
    47.84,
    47.80,
    47.76,
    47.67,
    47.41,
    46.85,
    46.06,
    44.99,
    43.89,
    41.60])
    
charge['13S2P'] = np.array([
    100.0,
    99.3,
    89.5,
    79.7,
    70.0,
    60.2,
    50.4,
    40.6,
    30.9,
    21.1,
    16.3,
    15.3,
    14.3,
    13.3,
    12.3,
    11.4,
    10.4,
    9.4,
    8.4,
    7.4,
    6.5,
    5.5,
    4.5,
    3.5,
    2.5,
    1.6,
    0.0])

def getDefaultConfig():
        toml_string = """
        type = '10S3P'
        """
        return toml.loads(toml_string)

def saveDefaultConfig():
    with open(cfg_file, 'w') as fid:
        cfg = getDefaultConfig()
        cfg['version'] = VERSION
        toml.dump(cfg, fid)

# Save current config
def saveConfig():
    with open(cfg_file, 'w') as fid:
        toml.dump(cfg, fid)

# start main program
cfg_dir = AppDirs(APPNAME, AUTHOR).user_config_dir
print(cfg_dir)
if not path.exists(cfg_dir):
    makedirs(cfg_dir)
cfg_file = Path(path.expandvars(
    f"{cfg_dir}/{APPNAME}")).with_suffix('.toml')
if not path.isfile(cfg_file):
    saveDefaultConfig()
cfg = toml.load(cfg_file)
if "version" not in cfg or \
    cfg["version"] != VERSION:
    saveDefaultConfig()
    cfg = toml.load(cfg_file)

# default value
V = tension['10S3P']

layout = [[sg.T(type['10S3P'], key='_MODEL_', visible=None), sg.Text('Select the batterie'),
           sg.InputCombo(['10S3P', '13S2P', '12S2P', '12S2Pxlr'], key='_TYPE_', default_value = cfg['type'], 
                                        change_submits=True, size=(8, 1))],
          [sg.T('Enter voltage'), sg.In(key='_INPUT_',
                                        size=(8, 1), change_submits=True)],
          #        [sg.T('', key='_TENSION_', visible=False), sg.T('Capacity'), sg.In(key='_RESULT_', size=(8,1))],
          [sg.T('Capacity'), sg.In(key='_RESULT_', size=(8, 1))],
          [sg.CloseButton('Quit')]]

window = sg.Window('Li-Ion capacity calculator',
                   auto_size_text=False,
                   default_element_size=(22, 1),
                   text_justification='right',
                   ).Layout(layout)

while True:     # Event Loop
    event, values = window.Read()
    #print(event, values)
    if event is None:
        break
    if event == 'Quit' or event == None:
        # print(cfg['type'])
        saveConfig()
        raise SystemExit("Cancelling: user exit")
    if event == '_TYPE_':
        cfg['type'] = values['_TYPE_']
        window.Element('_MODEL_').Update(value=type[values['_TYPE_']])
        window.Element('_INPUT_').Update(value='')
        window.Element('_RESULT_').Update(value='')
    if event == '_INPUT_':
        if values['_INPUT_'] == '':
            continue
        if values['_TYPE_'] == '10S3P':
            V = tension['10S3P']
            C = charge['10S3P']
        if values['_TYPE_'] == '12S2P':
            V = tension['12S2P']
            C = charge['12S2P']
        if values['_TYPE_'] == '12S2Pxlr':
            V = tension['12S2Pxlr']
            C = charge['12S2Pxlr']
        if values['_TYPE_'] == '13S2P':
            V = tension['13S2P']
            C = charge['13S2P']
        U = values['_INPUT_']
        U = U.replace(',','.')
        u = float(U)
        ind = (np.abs(V - u)).argmin()
        if u >= np.max(V):
            str = '{:4.1f} %'.format(100.0)
        elif u <= np.min(V):
            str = '{:4.1f} %'.format(0)
        else:
            try:
                p = (V[ind+1] - V[ind]) / (u - V[ind])
                res = (C[ind+1] - C[ind]) / p
                res = C[ind] + res
                str = '{:4.1f} %'.format(res)
            except:
                if ind >= len(U) -1:
                    str = '{:4.1f} %'.format(100)
                else:
                    str = '{:4.1f} %'.format(0)
        input = 'Input: {:05.2f} V'.format(u)
        window.Element('_RESULT_').Update(value=str)


# print(cfg['type'])
saveConfig()
