#Imports the generic Python packages

import sys
import simpy
import random
import math
import logging
import time
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

#Import the module with global variables

#start_time = time.time()

#Call the modules

def select_area_seeding(donor,gui,int_db):
    """Function that creates the necessary expansion technology instances from the initial cell density allocated to each passage"""
    cells_to_seed = donor.initial_cells_passage[donor.passage_no-1]

    index_et = -1

    correction_factor_gr = select_correction_factors(gui.SOURCE_OF_MSC)

    if gui.TYPE_OF_ET == 'microcarrier':

        seeding_density_area_mc = (gui.SD_SUSPENSION *1000)/(gui.MC_CONC*int_db.AREA_MC[gui.TYPE_OF_MC])

        #print('The possible area seeding densty of suspension vessels is %d cells/cm2' %seeding_density_area_mc)
		
        base_seeding_density = gui.SD_PLANAR

        base_seeding_density_mc = seeding_density_area_mc

        (index_et,number_seeded_et,new_seeding_density,min_workers,min_bscs,min_inc,min_bioreactors) = search_area_database(cells_to_seed,base_seeding_density,int_db.AREA_SUSPENSION,int_db.MAX_UNITS_RESOURCE_SUSPENSION,gui,int_db)

        if index_et > -1:

            name_of_et = int_db.names_of_suspension_ets[index_et]

            area_et = int_db.AREA_SUSPENSION[index_et]

#            donor.seeding_factor[donor.passage_no-1] = math.exp(-correction_factor_gr*math.log(new_seeding_density*gui.MC_ADH_RATE/base_seeding_density))

            donor.seeding_factor[donor.passage_no-1] = math.exp(-correction_factor_gr*math.log(new_seeding_density*gui.MC_ADH_RATE/base_seeding_density_mc))

    if index_et == -1:

        base_seeding_density = gui.SD_PLANAR

        (index_et,number_seeded_et,new_seeding_density,min_workers,min_bscs,min_inc,min_bioreactors) = search_area_database(cells_to_seed,base_seeding_density,int_db.AREA_PLANAR,int_db.MAX_UNITS_RESOURCE_PLANAR,gui,int_db)

        print((index_et,number_seeded_et,new_seeding_density,min_workers,min_bscs,min_inc,min_bioreactors))

        name_of_et = int_db.names_of_planar_ets[index_et]

        area_et = int_db.AREA_PLANAR[index_et]

        donor.seeding_factor[donor.passage_no-1] = math.exp(-correction_factor_gr*math.log(new_seeding_density/base_seeding_density))

    new_app_gr = donor.seeding_factor[donor.passage_no-1]*int_db.LIST_OF_MAX_GROWTH_RATES[donor.passage_no-1]

    #print('New seeding density is %d' %new_seeding_density)

    #print('New apparent growth rate is %.4f day^-1' % new_app_gr)

    #print('The new growth rate is %.4f of the baseline given for this passage' % donor.seeding_factor[donor.passage_no-1])

	#return the name of et, number of flasks to seed and the new area seeding density

    return (name_of_et,number_seeded_et,new_seeding_density,area_et,min_workers,min_bscs,min_inc,min_bioreactors)

def search_area_database(cells_to_seed,seeding_density,area_series,max_units_db,gui,int_db):
    '''Function that grabs the prescribed seeding density and looks for the best ET area and seeding density according to the type'''

    #Checks how many cells need to be seeded per ET to satisfy the required seeding density

    seed_cells_per_et = seeding_density*area_series

    #print('Base cells to seed per ET')
    #print(seed_cells_per_et)

    #Initializes a loop that starts looking into the largest areas

    number_seeded_et = [int(round(cells_to_seed/seed_cells_per_et[i_seed])) for i_seed in range(len(seed_cells_per_et))]

    #print('Number seeded ETs')
    #print(number_seeded_et)

    #Forces the cells to be seeded in a T25 if the number is too low

    if cells_to_seed < seeding_density*int_db.AREA_PLANAR[0]:

        number_seeded_et[0] = 1


    #Check what are the maximum numbers of ETs per species, putting the limitation of incubators

#    max_et_capacity = [max_units_db.iloc[j,1]*TOTAL_WORKERS for j in range(len(number_seeded_et))]

    max_et_capacity = [min(max_units_db.iloc[j,1]*gui.TOTAL_WORKERS,max_units_db.iloc[j,0]*int_db.MAX_INCUBATORS_PER_DONOR) for j in range(len(number_seeded_et))]

    #print(max_et_capacity)

    #Calculate the new flasks as the minimum of the maximum capacity and the generated flasks

    limited_ets = [min(number_seeded_et[k],max_et_capacity[k]) for k in range(len(max_et_capacity))]

    #print(limited_ets)

    #Check what are the indexes with flasks seeded larger than 0, if any

    indexes_seeded = [x[0] for x in enumerate(number_seeded_et) if x[1] > 0]

    #print(indexes_seeded)

    # print(indexes_seeded)

    if indexes_seeded == []:

        #Returns that no flasks were seeded

        return (-1,0,0,0,0,0,0)

    else:

        #Check what are the conditions that require a minimum number of workers

        no_workers_condition = [math.ceil(limited_ets[i]/max_units_db.iloc[i,1]) for i in indexes_seeded]

        #print(no_workers_condition)

        min_workers = min(no_workers_condition)

        # print('Minimum workers inside the search area database')
        # print(min_workers)

        condition_min_workers = [y[0] for y in enumerate(no_workers_condition) if y[1] == min_workers]

 #       condition_min_workers = [y for y in enumerate(indexes_seeded,no_workers_condition)]

        #print(condition_min_workers)

        #Return what are the indexes of index_seeded that have the minimum number of workers

        min_workers_index = [y[1] for y in enumerate(indexes_seeded) if y[0] in condition_min_workers]


        #Calculate how many BSCs are necessary simultaneously - assuming that each BSC only has capacity for one worker simultaneously

        min_bscs = min(min_workers,gui.TOTAL_BSC)

        #Returns what are the indexes that have the minimum number of flasks seeded while they require a minimum number of workers

        positive_seeded_flasks = [limited_ets[i] for i in min_workers_index]

        #print(positive_seeded_flasks)

        #Take what are the conditions that allow seeding the minimum number of flasks and return their indexes in the original list

        min_seeded_flasks = min(positive_seeded_flasks)

        #print(min_seeded_flasks)

        conditions_min_seeded = [y[0] for y in enumerate(limited_ets) if y[1] == min_seeded_flasks]

        #print(conditions_min_seeded)

        #Calculate the new seeding densities and the remainder for the minimum seeded conditions

        new_seeding_density = [cells_to_seed/(min_seeded_flasks*area_series[i_seed]) for i_seed in conditions_min_seeded]

        rem_sd = [abs(seeding_density - new_seeding_density[j]) for j in range(len(new_seeding_density))]

        # print(rem_sd)

        #Choose what is the index of minimum remainder from the minimum number of flasks conditions

        min_rem = rem_sd.index(min(rem_sd))

        #Retrieve the index of the global matrix

        final_index = conditions_min_seeded[min_rem]

        #Calculate how many incubators are necessary to hold the number of generated flasks - select for incubators of bioreactors.

        #If the units are planar or below the index for bioreactors, only calculate the number of minimum incubators

        #MAKE A TRYCATCH STRUCTURE:

        try:
            assert_frame_equal(max_units_db, int_db.MAX_UNITS_RESOURCE_PLANAR)
            comp_frames = True
        except:
            comp_frames = False


        if comp_frames == True:

            min_inc = math.ceil(min_seeded_flasks / max_units_db.iloc[final_index,0])

            min_bioreactors = 0

        elif final_index in range(3):

            min_inc = 0

            min_bioreactors = math.ceil(min_seeded_flasks / max_units_db.iloc[final_index,0])

        #Return the results

        return(final_index,min_seeded_flasks,new_seeding_density[min_rem],min_workers,min_bscs,min_inc,min_bioreactors)


    # while i_seed > -1 :

    # 	#Checks how many ET units can be seeded with the prescribed cell density

    #     number_seeded_et = int(round(cells_to_seed/seed_cells_per_et[i_seed]))


    #     #Breaks the cycle if at least one instance of the ET can be seeded.

    #     if number_seeded_et > 0:

    #         current_min = number_seeded_et

    #             if current_min > min_flasks:



    #         new_seeding_density = cells_to_seed/(number_seeded_et*AREA_PLANAR[i_seed])

    #         #Choose what is the maximum and minimum between the proposed and new seeding density

    #         sd_up = max(seeding_density,new_seeding_density)

    #         sd_down = min(seeding_density,new_seeding_density)

    #         rem_sd = sd_up%%sd_down

    #         break

    #     else:

    #         i_seed -= 1

    # #Return the index of ET to seed, the number of seeded ETs and the new seeding density

    # return (i_seed,number_seeded_et,new_seeding_density)

def harvest_selection(name_of_et,gui,int_db):

    if name_of_et in int_db.names_of_planar_ets:

        harvest_density_area = gui.HD_PLANAR

    else:

        harvest_density_area = (gui.HD_SUSPENSION*1000)/(gui.MC_CONC*int_db.AREA_MC[gui.TYPE_OF_MC])

    return harvest_density_area

def select_correction_factors(type_of_msc):

    if type_of_msc == 'asc':

        correction_slope = 0.166

    elif type_of_msc == 'bm':

        correction_slope = 0.147

    else:

        correction_slope = 0

    return correction_slope
