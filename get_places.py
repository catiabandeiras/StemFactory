#Imports the generic Python packages

import sys
##sys.path.append('/Users/svc/anaconda/pkgs/scipy-0.16.0-np110py35_1/lib/python3.5/site-packages')
##sys.path.append('/Users/svc/anaconda/pkgs/numpy-1.10.1-py35_0/lib/python3.5/site-packages')
##sys.path.append('/Users/svc/anaconda/pkgs/matplotlib-1.5.0-np110py35_0/lib/python3.5/site-packages')
##
sys.path.append('/Users/svc/anaconda/lib/python3.5/site-packages')

import simpy
import random
import math

#Import other modules
from scipy.integrate import odeint
import numpy as np
#import matplotlib.pyplot as plt

'''Function that mediates the access to the other particular procedures inside the BSC'''

def bsc_et(env,et,donor,lab,procedure,gui,int_db):

##    print('%s of %s will start at %.4f days.' % (procedure.capitalize(),name,env.now))
##    print('\n')

    if procedure == 'seeding':

        seed = seeding_procedure(env,et,donor,lab,gui,int_db)

        env.process(seed)

        yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time))

    elif procedure == 'feeding':
        
        feed = feeding_procedure(env,et,donor,lab,int_db)

        env.process(feed)

        yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.feeding_time))

    elif procedure == 'harvesting':

        harv = harvesting_procedure(env,et,donor,lab,gui,int_db)

        env.process(harv)

 #       print('Current passage number at %.5f in get_places is %d' %(env.now,donor.passage_no))

        yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.harvesting_time)+int_db.FIXED_HARVESTING_TIME)

        #print('Current passage number at %.5f in get_places is %d' %(env.now,donor.passage_no))

#    print('%s of %s ended at %.4f days.' % (procedure.capitalize(),name,env.now))


def seeding_procedure(env,et,donor,lab,gui,int_db):

    '''Adds volumes of reagents'''

#    lab.occupied_workers += 1

    yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time))

    if et.base_name in int_db.names_of_planar_ets:

        seeding_volume_updates(env,et,lab,int_db.MEDIA_VOLUME_PLANAR_ETS,0)

    elif et.base_name in int_db.names_of_suspension_ets:

        #Update the initial number of cells due to the adhesion rate

#        print(et.initial_cells)

#        print(MC_ADH_RATE)

        et.initial_cells = et.initial_cells*gui.MC_ADH_RATE

        #The lab mc mass is divided per 1000 because the concentration of microcarriers is in g/L and not in ml

        lab.mc_mass = gui.MC_CONC*int_db.MEDIA_VOLUME_SUSPENSION_ETS[et.base_name]/1000

        coating_volume = int_db.NEEDS_COATING_MC[TYPE_OF_MC] * int_db.COATING_PER_AREA * int_db.AREA_MC[gui.TYPE_OF_MC] * lab.mc_mass

        seeding_volume_updates(env,et,lab,int_db.MEDIA_VOLUME_SUSPENSION_ETS,coating_volume)


    #Do the addition to worker and lab times and set bsc as occupied

#    lab.occupied_bscs += 1

    #print('donor worker count inside %d' %donor.worker_queue.count)

    #print('donor worker capacity inside %d' %donor.worker_queue.capacity)

    lab.time_of_worker += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time)

    lab.time_of_bsc += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time)

    #Adds a seeded flask

    donor.seeded_per_passage[donor.passage_no-1] += 1

    #Make the timeouts

    # print('count of worker queue is %d' %donor.worker_queue.count)
    # print('capacity of worker queue is %d' %donor.worker_queue.capacity)
    # print('baseline of seeding time is %d' %lab.seeding_time)

    # print('Reagent volumes spent')
    # print(lab.reagent_volumes)

#    yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time))

def seeding_volume_updates(env,et,lab,media_volume_series,coating_volume):

    '''makes the updates directly in the lab class'''

    name_et = et.base_name

    media_volume = media_volume_series[name_et]

    lab.reagent_volumes[0] += media_volume

    lab.reagent_volumes[2] += coating_volume


def feeding_procedure(env,et,donor,lab,int_db):

    #Set worker and bsc to occupied again

 #   lab.occupied_bscs += 1

    lab.occupied_workers += 1

    '''Adds volumes of reagents'''

    if et.base_name in int_db.names_of_planar_ets:

        feeding_volume_updates(env,et,lab,int_db.FEEDING_VOLUME_PLANAR_ETS)

    elif et.base_name in int_db.names_of_suspension_ets:

        feeding_volume_updates(env,et,lab,int_db.FEEDING_VOLUME_SUSPENSION_ETS)

    #Make the timeouts

    #print(donor.worker_queue.count)
    #print(donor.worker_queue.capacity)

    yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.feeding_time))

    #The number of hours of the worker in operation increases

    lab.time_of_worker += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.feeding_time)
    lab.time_of_bsc += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.feeding_time)

    #print('Reagent volumes spent')
    #print(lab.reagent_volumes)

def feeding_volume_updates(env,et,lab,feeding_volume_series):

    '''makes the updates directly in the lab class'''

    name_et = et.base_name

    media_volume = feeding_volume_series[name_et]

    lab.reagent_volumes[0] += media_volume

def harvesting_procedure(env,et,donor,lab,gui,int_db):

    '''Adds volumes of reagents'''

#    lab.occupied_workers += 1

    yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.harvesting_time)+int_db.FIXED_HARVESTING_TIME)

    if et.base_name in int_db.names_of_planar_ets:

        harvesting_volume_updates(env,et,lab,int_db.HARVEST_VOLUME_PLANAR_ETS)

        index_of_et = int_db.names_of_planar_ets.index(et.base_name)

        lab.planar_used[index_of_et] += 1

        final_cells_et = int(math.floor(et.no_cells)*gui.HEFF_PLANAR)


        #add a new harvested flask accounting for the harvest efficiency of the current technology

#        print('Total number of planar technologies of type %s used is %d' %(et.base_name,lab.planar_used[index_of_et]))

    elif et.base_name in int_db.names_of_suspension_ets:

        harvesting_volume_updates(env,et,lab,int_db.HARVEST_VOLUME_SUSPENSION_ETS)

        index_of_et = int_db.names_of_suspension_ets.index(et.base_name)

        lab.mc_based_used[index_of_et] += 1

        final_cells_et = int(math.floor(et.no_cells)*gui.HEFF_SUSPENSION)

 #   print(donor.final_cells_passage)

    #Add to initial cells of next passage

    #print('Final cells of %s are %d' % (et.full_name,final_cells_et))

    donor.final_cells_passage[donor.passage_no-1] += final_cells_et

    if donor.passage_no < len(donor.initial_cells_passage):

        donor.initial_cells_passage[donor.passage_no] = donor.final_cells_passage[donor.passage_no-1]

    donor.harvested_per_passage[donor.passage_no-1] += 1

    #print('Harvested flasks at %.4f are %d' % (env.now,donor.harvested_per_passage[donor.passage_no-1]))

    #print(donor.harvested_per_passage)

    #Make the timeouts

    lab.time_of_worker += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.harvesting_time)+int_db.FIXED_HARVESTING_TIME

    lab.time_of_bsc += (donor.worker_queue.count/donor.worker_queue.capacity)*(lab.harvesting_time)+int_db.FIXED_HARVESTING_TIME

    lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])

#    yield env.timeout((lab.worker_queue.count/lab.worker_queue.capacity)*(lab.harvesting_time)+FIXED_HARVESTING_TIME)

def harvesting_volume_updates(env,et,lab,harvesting_volume_series):

    '''makes the updates directly in the lab class'''

    name_et = et.base_name

    harvest_volume = harvesting_volume_series[name_et]

    lab.reagent_volumes[1] += harvest_volume

    
def get_place_incubator(env,et,donor,lab,gui,int_db):

    '''Function that mediates access to incubator'''
    
    with donor.incubator_queue.request() as request:

        yield request

        lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])

        #Add the time of use of incubators

        feeding_period = lab.incubation_time

        #Run the cell growth ODE

        cell_growth = cellgrowth(env,et,donor,lab,feeding_period,int_db)
        
        env.process(cell_growth)        

        #Update the global incubation times and the times of incubation per ET

        lab.time_of_incubator += feeding_period/donor.incubator_queue.count

        et.days_incubated += feeding_period

        #print('Number of days in incubation of %s is %d' % (et.full_name,et.days_incubated))

        yield env.timeout(feeding_period)

#        et.days_incubated += feeding_period


def get_place_bioreactor(env,et,donor,lab,gui,int_db):

    '''Method that mediates access to bioreactor'''
    
    with donor.bioreactor_queue.request() as request:

        yield request

        lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])

        #Add the time of use of incubators

        feeding_period = lab.incubation_time

        #Run the cell growth ODE

        cell_growth = cellgrowth(env,et,donor,lab,feeding_period,int_db)
        
        env.process(cell_growth)        

        #Update the global incubation times and the times of incubation per ET

        lab.time_of_bioreactor += feeding_period/donor.bioreactor_queue.count

        et.days_incubated += feeding_period

        yield env.timeout(feeding_period)


def cellgrowth(env,et,donor,lab,feeding_period,int_db):

    '''Method resposible for predicting what is the cell growth'''

    #Initialize the number of cells

    Xv0 = et.initial_cells

#    yield env.timeout(feeding_period)

    #Get the current incubation time

    inc_time = et.days_incubated

#    print(inc_time)
#    print(env.now)

    #Select what is the current growth rate

    miu_max = int_db.LIST_OF_MAX_GROWTH_RATES[donor.passage_no-1]*donor.seeding_factor[donor.passage_no-1]

    #Insert the time indexes for simulation - index needs to be corrected due to numerical approximation

    t = np.linspace(0,100,num=100/0.0001+1)

    t_round = np.around(t,4)

    time_index = np.where(t_round==inc_time)

    time_index_1 = time_index[0]

    time_index_2 = time_index_1[0]

    #Pass the handles for odeint

    cellgrowth_int_handle = lambda Xv,t: cellgrowth_ode(Xv,t,miu_max)

    cell_per_time = odeint(cellgrowth_int_handle,Xv0,t)

    #Select the right index from times of integration and update cell number

    et.no_cells = cell_per_time[time_index_2]

    #print('The number of cells after %.5f  of incubation is %d' % (et.days_incubated,et.no_cells))

    #Advance the simulation to the day where feeding is done and density checked

    yield env.timeout(feeding_period)
    

def cellgrowth_ode(Xv,t,k):

    '''A very simple method to predict the growth curve of cells'''

    #Put the apparent growth rate equation for simplicity for now

    return k*Xv
