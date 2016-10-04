#Imports the generic Python packages

import simpy
import random
import math

#IMPORT THE CREATED MODULES

#Create the donor class to store the operations done with each donor in terms of cell number

class Donor(object):
    """A laboratory has a limited number of incubators, BSC, workers and expansion technology units
    """
    def __init__(self,env,donor_index,gui):
        #print('Laboratory constructor called')

 #       Laboratory.__init__(self,env)

        self.initial_cells_passage = [0]*gui.MAX_NO_PASSAGES

        self.initial_cells_passage[0] = abs(int(random.gauss(gui.INITIAL_CELLS_PER_DONOR_AVG,gui.INITIAL_CELLS_PER_DONOR_SD)))

        if self.initial_cells_passage[0] < 0:

            self.initial_cells_passage[0] = -1*self.initial_cells_passage[0]

        self.final_cells_passage = [0]*gui.MAX_NO_PASSAGES

        self.passage_no = 1

        self.cpds = 0

        self.donor_index = donor_index

        self.is_incubated = [0]*gui.MAX_NO_PASSAGES

        self.seeded_per_passage = [0]*gui.MAX_NO_PASSAGES

        self.feeded_per_passage = [0]*gui.MAX_NO_PASSAGES

        self.incubated_per_passage = [0]*gui.MAX_NO_PASSAGES

        self.harvested_per_passage = [0]*gui.MAX_NO_PASSAGES

        self.et_type_per_passage = ['']*gui.MAX_NO_PASSAGES

        self.no_ets_per_passage = [0]*gui.MAX_NO_PASSAGES

        self.doses_per_donor = 0

        #Select what are the corrections to the growth rate operated by different seeding densities

        self.seeding_factor = [1]*gui.MAX_NO_PASSAGES

        #Set the numbers of current resources required to have a donor process

        self.required_workers = 0

        self.required_bscs = 0

        self.required_incubators = 0

        #Initialize queues
        
        self.worker_queue = simpy.Resource(env,1)
        
        self.incubator_queue = simpy.Resource(env,1)
        
        self.bsc_queue = simpy.Resource(env,1)

        self.bioreactor_queue = simpy.Resource(env,1)


    def show_info_donor(self):

        print('Donor construct created.')
        print('The initial number of cells of donor '+str(self.donor_index)+' after isolation is '+str(self.initial_cells_passage[0]))
    
# env = simpy.Environment()

# lab = Laboratory(env)
# lab.show_info_lab()

# donor = Donor(env,0)

#donor.show_info_donor()

