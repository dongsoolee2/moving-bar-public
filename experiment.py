"""
An Experiment class and functions to deal with retinal physiological data
measured simultaneously from a population of ganglion cells (extracellularly)
and an amacrine cell (or a cell of other types, recorded intracellularly).
"""
import numpy as np
import pandas as pd

class Experiment(object):
    """
    An Experiment stores parameters of an experiment and computes
    characteristics of recorded cells (extracellularly or intracellularly)
    after reading hdf5 file.
    """
    def __init__(self, name, stimlist, rflist):
        """
        Construct a new Experiment class
        """
        self.name = name
        self.list = stimlist
        """
                ['flash', 'line', 'wn_short',
                'mb_lr_con', 'mb_lr_amp', 'mb_lr_dim',
                'mb_lr_2con', 'mb_lr_2amp', 'mb_lr_2dim',
                'mb_lr_4con', 'mb_lr_4amp', 'mb_lr_4dim',
                'mb_rl_con', 'mb_rl_amp', 'mb_rl_dim',
                'mb_rl_2con', 'mb_rl_2amp', 'mb_rl_2dim',
                'mb_rl_4con', 'mb_rl_4amp', 'mb_rl_4dim',
                'wn_long', 'wn_inj']
        """
        self.rflist = rflist

        self.g = dict((k, []) for k in self.list)
        self.i = dict((k, []) for k in self.list)
        self.tbins = dict((k, []) for k in self.list)
        self.stim = dict((k, []) for k in self.list)
        self.rf = {'g': dict((k, []) for k in self.rflist),
            'i': dict((k, []) for k in self.rflist)}
        self.df = pd.DataFrame()

    def addcelldata(self, dic, mode): # i , param
        if mode == 'ganglion':
            for key in [k for k in self.list if k in dic.keys()]:
                self.g[key].append(dic[key])
            for key in [k for k in self.list if k not in dic.keys()]:
                self.g[key].append(np.nan)
        elif mode == 'intracell':
            for key in [k for k in self.list if k in dic.keys()]:
                self.i[key].append(dic[key])
            for key in [k for k in self.list if k not in dic.keys()]:
                self.i[key].append(np.nan)
        elif mode == 'stim':
            for key in [k for k in self.list if k in dic.keys()]:
                self.stim[key].append(dic[key])
            for key in [k for k in self.list if k not in dic.keys()]:
                self.stim[key].append(np.nan)
        elif mode == 'tbins':
            for key in [k for k in self.list if k in dic.keys()]:
                self.tbins[key].append(dic[key])
            for key in [k for k in self.list if k not in dic.keys()]:
                self.tbins[key].append(np.nan)
        elif mode == 'grf':
            for key in [k for k in self.rflist if k in dic.keys()]:
                self.rf['g'][key].append(dic[key])
            for key in [k for k in self.rflist if k not in dic.keys()]:
                self.rf['g'][key].append(np.nan)
        elif mode == 'irf':
            for key in [k for k in self.rflist if k in dic.keys()]:
                self.rf['i'][key].append(dic[key])
            for key in [k for k in self.rflist if k not in dic.keys()]:
                self.rf['i'][key].append(np.nan)
        else:
            print("""mode should be either 'ganglion', 'intracell', 'stim',
                    'tbins', 'grf', 'irf'""")

    def addcellparam(self, table):
        self.table = table
