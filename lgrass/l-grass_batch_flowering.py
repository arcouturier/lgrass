'''
Created on 11/10/2018

@author: modelisation - SR
'''
# batch pour L-grass with flowering

# import the modules necessary to initiate the L-systems
import time
import math
import re
from openalea.lpy import *
from openalea.plantgl.all import *
from alinea.caribu.CaribuScene import CaribuScene
import multiprocessing
import sys
import os
# from generateScene import *
import numpy as np
from lgrass import flowering_functions
from openalea.lpy import Lsystem
import itertools
import pandas as pd

path_ = r'D:\Simon\Python\lgrass\lgrass'


OUTPUTS_DIRPATH = 'outputs/output_batch_path/comite_these_2'
# date_string = datetime.datetime.now() .strftime('%Y_%m_%d_%Hh%M')
# output_batch_path = open(os.path.join(OUTPUTS_DIRPATH, 'output_batch_path', date_string), "wb")
# output_batch = csv.writer(output_batch_path)
# output_batch.writerow(['vai', 'vbee', 'sldl', 'absolute_max_leaf_number', 'absolute_min_leaf_number'])


# cree la liste de L-systems et liste des noms
testsim = {}
names = []


nb_simul = 0
temp_vern_min_list = np.arange(0, 1, 10)
temp_vern_inter_list = np.arange(8, 9, 10)
temp_vern_max_list = np.arange(17, 18, 10)
daily_vern_rate_list = np.arange(0.001, 0.002, 10)
basic_vern_rate_list = np.arange(0.01, 0.11, 10)
photoperiod_min_list = np.arange(10, 11, 10)
photoperiod_max_list = np.arange(16, 17, 10)
max_photo_ind_rate_list = np.arange(1, 2, 10)
coeff_primordia_emission_vegetative_list = np.arange(1, 2, 10)
coeff_primordia_emission_reproductive_list = np.arange(2, 3, 10)
#conditions = pd.read_csv('D:/Simon/Comites_de_these/Comite_de_these_2/Modelisation/site_sowing_date_bronsyn.csv', sep=';')
#combination_site_sowing_date = np.array([("LUSIGNAN", "2007_10_15")])
combination_site_sowing_date = np.array([("LUSIGNAN", "2012_10_15"),
                                         ("LUSIGNAN", "2017_10_15"),
                                         ("THEIX", "2007_10_15"),
                                         ("THEIX", "2012_10_15"),
                                         ("THEIX", "2017_10_15"),
                                         ("PLOUDANIEL", "2007_10_15"),
                                         ("PLOUDANIEL", "2012_10_15"),
                                         ("PLOUDANIEL", "2017_10_15")])


for x in itertools.product(temp_vern_min_list, temp_vern_inter_list, temp_vern_max_list, daily_vern_rate_list,
                           basic_vern_rate_list, photoperiod_min_list, photoperiod_max_list, max_photo_ind_rate_list,
                           coeff_primordia_emission_vegetative_list, coeff_primordia_emission_reproductive_list,
                           combination_site_sowing_date):
    print(x)
    nb_simul += 1
    flowering_param = flowering_functions.FloweringFunctions()
    flowering_param.param.temp_vern_min = x[0]
    flowering_param.param.temp_vern_inter = x[1]
    flowering_param.param.temp_vern_max = x[2]
    flowering_param.param.daily_vern_rate = x[3]
    flowering_param.param.basic_vern_rate = x[4]
    flowering_param.param.photoperiod_min = x[5]
    flowering_param.param.photoperiod_max = x[6]
    flowering_param.param.max_photo_ind_rate = x[7]
    flowering_param.param.coeff_primordia_emission_vegetative = x[8]
    flowering_param.param.coeff_primordia_emission_reproductive = x[9]

    name = str(x[10][0]) + "_" + str(x[10][1])
    print(name)
    names.append(name)
    lpy_filename = os.path.join('lgrass.lpy')
    testsim[name] = Lsystem(lpy_filename)
    testsim[name].derivationLength = 200
    testsim[name].meteo_path = 'D:/Simon/Comites_de_these/Comite_de_these_2/Modelisation/Meteo_sites_GEVES_daylength.csv'
    testsim[name].sowing_date = x[10][1]
    testsim[name].site = x[10][0]
    testsim[name].flowering_model = flowering_param
    testsim[name].output_induction_file_name = 'induction_' + name
    testsim[name].output_organ_lengths_file_name = 'organ_lengths_' + name

# function to run an L-system from the 'testsim' dictionnary


def runlsystem(n):
    testsim[names[n]].derive()  # permet le declenchement de la fonction "End" du script lpy
    # print(testsim[names[n]].output_dict)
    # with open(os.path.join(OUTPUTS_DIRPATH, 'sortie_test_path', str(n) + '.csv'), 'wb') as sortie_test_path:
    #     sortie_test = csv.writer(sortie_test_path)
    #     sortie_test.writerows(testsim[names[n]].output_dict.items())
    testsim[names[n]].clear()
    print(''.join((names[n], " - done")))

    # print(testsim[names[n]].output_dict)


for i in range(nb_simul):
    runlsystem(i)

# #run the L-systems
# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     CPUnb = multiprocessing.cpu_count()-1 #nombre de processeurs, moins un par prudence. (et pour pouvoir faire d'autres choses en meme temps)
#     print 'nb CPU: ' + str(CPUnb)
#     pool = multiprocessing.Pool(processes=CPUnb)
#     for i in range(int(nb_simul)):
#         pool.apply_async(runlsystem, args=(i,)) #Lance CPUnb simulations en meme temps, lorsqu'une simulation se termine elle est immediatement remplacee par la suivante
#     pool.close()
#     pool.join()
