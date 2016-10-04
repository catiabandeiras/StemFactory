#from global_userinput import *

from queue_creator import *

#Imports the generic Python packages

import simpy
import random
import math

import pandas as pd

#IMPORT THE CREATED MODULES

#Create the laboratory class - information about # equipments, total volumes spent, etc, is the parent of "ET" class

class Laboratory(object):
    """A laboratory has a limited number of incubators, BSC, workers and expansion technology units
    """
    def __init__(self,env,gui,int_db):
        #print('Laboratory constructor called')
        self.env = env

        #No need to repeat the fixed things employed in the gui

        #Reagent volumes structure - media, harvest and coating

        self.reagent_volumes = [0,0,0]

        self.mc_mass = 0

        self.planar_used = [0]*len(int_db.names_of_planar_ets)

        self.mc_based_used = [0]*len(int_db.names_of_suspension_ets)

        #Set the numbers of current resources required

        self.occupied_incubators = 0

        self.occupied_workers = 0

        self.occupied_bscs = 0

        self.occupied_bioreactors = 0

        #Set the times of operations (workers, BSC and incubator)

        self.time_of_worker = 0

        self.time_of_bsc = 0

        self.time_of_incubator = 0

        self.time_of_bioreactor = 0

        #Initialize times

        self.seeding_time = 0

        self.feeding_time = 0

        self.harvesting_time = 0

        self.worker_time = int_db.WORKER_GRAB_TIME

        self.incubation_time = 0

        #Start the total doses and lots produced to account for in the lab

        self.total_doses = 0

        self.total_lots = 0

        self.finished_donors = 0

        #Inserts the global queues, initialize to 1

        self.global_worker_queue = simpy.Resource(env,1)

        self.global_incubator_queue = simpy.Resource(env,1)

        self.global_bioreactor_queue = simpy.Resource(env,1)

        self.list_of_workers = create_queue_list(env,gui.TOTAL_WORKERS,1)

        #Insert a CPDs dictionary

        self.final_passage_per_donor = dict()

        self.cpds_per_donor = dict()

    def show_info_lab(self,gui,int_db):

        print('Laboratory construct created.')
        print('The GMP facility has a total area of '+str(gui.AREA_FACILITY)+' sq mt.')
        print('The manufacturing rooms have '+str(gui.TOTAL_INCUBATORS)+' incubators, '+str(gui.TOTAL_BIOREACTORS)+' bioreactors and '+str(gui.TOTAL_BSC)+' biological safety cabins.')
        print('The GMP facility has '+str(gui.TOTAL_WORKERS)+' active workers.')
    
# env = simpy.Environment()

# lab = Laboratory(env)
# lab.show_info_lab()

