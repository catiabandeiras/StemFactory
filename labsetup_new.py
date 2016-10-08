'''labsetup_msc.py - Method that coordinates the execution of the simulations'''

#Imports the generic Python packages

import sys
import simpy
import random
import math
import logging
import time
#from tkinter import *
#from tkinter import ttk
#import numpy as np
import pandas as pd

#Import the module with global variables

start_time = time.time()

#Call the modules
from lab_class import *
from donor_class import *
from seeding_selection import *
from et_lab_update import *
from et_class import *
from expansion_tech import *
from final_cost_info import *



#Create the laboratory by initializing the internal database when the simulation starts running
#passes both the GUI and database parameters

def labsetup(env,gui,int_db):

    '''Function that defines how the laboratory is set up and how '''

    #Initialize the GMP facility

    #gui.text.insert('2.0','Entered simulation\n')

    lab = Laboratory(env,gui,int_db)

    #lab.show_info_lab(gui,int_db)

    #yield env.timeout(1)

#    print(env.now)

    #Initialize the donors (assume infinite, so it's a while True statement)

    donor_index = 0

    while lab.total_doses < gui.ANNUAL_DEMAND:

        '''Launch the donor'''

        donor = Donor(env,donor_index,gui)

        donor.show_info_donor()

        print('Donor number %d starts running at %.5f days' % (donor_index,env.now))

        donor_proc = env.process(donor_launch(env,lab,gui,donor,donor_index,int_db))

        yield env.timeout(0.0001)

        # print('required workers for donor %d'%donor_index)
        # print(donor.required_workers)

        while True:

            #Launches a new donor if there are avalable workers and incubators to put cells at

            if lab.occupied_workers < min(gui.TOTAL_WORKERS,gui.TOTAL_BSC) and lab.occupied_workers+donor.required_workers <= gui.TOTAL_WORKERS and lab.occupied_incubators < gui.TOTAL_INCUBATORS:

                donor_index += 1

                break

            else:

                yield env.timeout(0.0001)

                continue

        if lab.total_doses >= gui.ANNUAL_DEMAND:

            #Prints how many doses and lots produced

            print('Annual demand reached!')

            dose_lot_print(env,lab,gui)

            #Print the costs

            final_cost_info(env,lab,gui,int_db)

            break

        #else:
        #     print('Did not meet the demand in the allotted time!')
        #     final_cost_info(env,lab,gui,int_db)
        #     break

    # while True:

    #     if lab.finished_donors >= donor_index:

    #         #Only puts the print to the final doses and lot when all donors were processed.

    #         dose_lot_print(env,lab,gui)

    #         #Print the costs

    #         final_cost_info(env,lab,gui,int_db)

    #         break

    #     else:

    #         yield env.timeout(0.0001)

    #         continue




def dose_lot_print(env,lab,gui):

    '''Function that prints the current time, doses and lots'''

    print('The total doses produced within the run at %.5f days are %d' % (env.now,lab.total_doses))

    gui.text.insert('1.0','The total doses produced within the run at %.5f days are %d \n' % (env.now,lab.total_doses))

    lab.total_lots = math.ceil(lab.total_doses/gui.LOT_SIZE)

    #AC MOD - set simulation results
    gui.results.add_donor_results(env.now, lab.total_doses, lab.total_lots)


    print('The total lots produced within the run at %.5f days are %d' % (env.now,lab.total_lots))

    gui.text.insert('2.0','The total lots produced within the run at %.5f days are %d \n' % (env.now,lab.total_lots))



def finish_simulation(env,lab,gui,donor,donor_index,clause):

    '''Function that prints the outcomes'''

    if clause == 'maxcap':

        print('No need for more passages, maximum capacity reached. Break simulation')

        gui.results.append_event(env.now, "Max_Capacity_Reached")

        number_doses_per_donor = math.floor(donor.final_cells_passage[donor.passage_no-2]/gui.CELL_NUMBER_PER_DOSE)

        final_passage_no = donor.passage_no - 1

    elif clause == 'maxpass':

        print('Final passage allowed reached')

        gui.results.append_event(env.now, "Max_Passages_reached")

        number_doses_per_donor = math.floor(donor.final_cells_passage[donor.passage_no-1]/gui.CELL_NUMBER_PER_DOSE)

        final_passage_no = donor.passage_no

    elif clause == 'maxcpd':

        print('Maximum number of CPDs reached. Break simulation.')

        gui.results.append_event(env.now, "Max_CPD_reached")

        number_doses_per_donor = math.floor(donor.final_cells_passage[donor.passage_no-1]/gui.CELL_NUMBER_PER_DOSE)

        final_passage_no = donor.passage_no

    elif clause == 'maxtime':

        print('Maximum simulation time allowed reached. Break simulation')

        gui.results.append_event(env.now, "Max_Time_Reached")

        number_doses_per_donor = math.floor(donor.final_cells_passage[donor.passage_no-1]/gui.CELL_NUMBER_PER_DOSE)

        final_passage_no = donor.passage_no


    donor.doses_per_donor += number_doses_per_donor

    print('%d doses were produced from donor %d with %.2f CPDs at passage %d' % (donor.doses_per_donor,donor_index,donor.cpds,final_passage_no))

    #Append the donor CPDs to the lab database

    lab.cpds_per_donor[donor.donor_index] = round(donor.cpds,2)

    lab.final_passage_per_donor[donor.donor_index] = int(final_passage_no)


    # print('Current state of dictionary of CPDs per donor')
    # print(lab.cpds_per_donor)

    # print('Current state of final passsages per donor')
    # print(lab.final_passage_per_donor)

    #Add the produced doses to the annual demand

    lab.total_doses += donor.doses_per_donor

    #print(lab.total_doses)

    #Release the occupied incubator

    lab.occupied_incubators -= donor.required_incubators

    #print('Occupied incubators after passage %d of donor %d in finish_simulation' %(donor.passage_no,donor_index))
    #print(lab.occupied_incubators)


    #print('Occupied incubators after end of donor processing')
    #print(lab.occupied_incubators)

    #Print the current dose information

    dose_lot_print(env,lab,gui)

    lab.finished_donors += 1



def donor_launch(env,lab,gui,donor,donor_index,int_db):
    '''Function that coordinates the launch of new donors so that they can run simultaneously'''

    '''Create the donor'''

#    donor = Donor(env,donor_index)

    while donor.passage_no <= gui.MAX_NO_PASSAGES and donor.cpds <= gui.MAXIMUM_NUMBER_CPD:

        #Select what is the best expansion technology type and create an appropriate number of instances of the ET class

        new_seed_vars = select_area_seeding(donor,gui,int_db)

        print('All new seed vars')
        print(new_seed_vars)

        #Select an area harvesting density

        name_of_et = new_seed_vars[0]

        number_seeded_et = new_seed_vars[1]

        new_seed_dens = new_seed_vars[2]

        prev_et_name = donor.et_type_per_passage[donor.passage_no-2]

        prev_no_et = donor.no_ets_per_passage[donor.passage_no-2]

        # print(name_of_et)
        # print(number_seeded_et)
        # print(prev_et_name)
        # print(prev_no_et)

        # print('New seeding density is %d' %new_seed_dens)

        # print('The new growth rate is %.4f of the baseline given for this passage' % donor.seeding_factor[donor.passage_no-1])

        harvest_density_area = harvest_selection(name_of_et,gui,int_db)

        # print('harvest density area')

        # print(harvest_density_area)

        #break

    #yield env.timeout(1)

#        print(harvest_density_area)

        if (name_of_et == prev_et_name and number_seeded_et == prev_no_et) or new_seed_dens > harvest_density_area:

            #Send simulation to finish if maximum capacity was reached

            clause = 'maxcap'

            finish_simulation(env,lab,gui,donor,donor_index,clause)

            break


#         # print('Number of seeded %s ETs is %d' % (name_of_et,number_seeded_et))

#         #Update the queues

#         # print('Worker queues before lab updates')

#         # print(donor.donor_index)
#         # worker_counts = [lab.list_of_workers[worker_index].count for worker_index in range(TOTAL_WORKERS)]
#         # print(worker_counts)
#         # print(lab.occupied_workers)
#         # print(env.now)

        lab_queue_update(env,lab,donor,name_of_et,new_seed_vars,gui,int_db)

#         print('feeding time is %.5f' %lab.feeding_time)


        #Gets what are the occupied workers

        worker_counts = [lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)]

        print('Lab worker queue count is %d' % lab.occupied_workers)
        print('Donor worker queue capacity is %d' % donor.worker_queue.capacity)
        print('Required workers for passage %d of donor %d are %d' % (donor.passage_no,donor_index,donor.required_workers))
        print('Required incubators for passage %d of donor %d are %d' % (donor.passage_no,donor_index,donor.required_incubators))

#  #       lab.occupied_workers += donor.required_workers

        if donor.passage_no == 1:

            lab.occupied_incubators += donor.required_incubators

        print('Occupied workers in the beginning of passage %d of donor %d in the outside loop' %(donor.passage_no,donor_index))
        print(lab.occupied_workers)

#        break

#        yield env.timeout(1)

        #Make the launch of the new process wait until all required workers are free

        while True:

            if donor.required_workers + lab.occupied_workers > gui.TOTAL_WORKERS:

                yield env.timeout(0.0001)

            else:

                print('Passage %d of donor %d is ready to start at %.4f' % (donor.passage_no,donor_index,env.now))
                #print('Lab worker queue count is %d' % lab.occupied_workers)

                # print('Worker queues outside before entering the cycle')

                # print(donor.donor_index)
                # worker_counts = [lab.list_of_workers[worker_index].count for worker_index in range(TOTAL_WORKERS)]
                # print(worker_counts)
                # print(lab.occupied_workers)
                # print(env.now)

                break

        #break

        #yield env.timeout(1)

        #Create a list with the instances of ET class

        list_et_class = [ExpansionTechnology(env,gui,int_db,donor,donor_index,new_seed_vars,harvest_density_area,no_et) for no_et in range(number_seeded_et)]

        # for et in list_et_class:

        #     et.show_info_et()

        # break

        # yield env.timeout(1)

        #Create a list of processes and run them simultaneously when possible.

        list_of_processes = [expansion_tech_run(env,et,donor,lab,gui,int_db) for et in list_et_class]

        for proc in list_of_processes:

            print('Process due to start at %.4f' % env.now)

            env.process(proc)

            yield env.timeout(0)


        #Update the timeouts only when all the flasks are harvested

        while donor.harvested_per_passage[donor.passage_no-1] < number_seeded_et:

            yield env.timeout(0.00001)

            if donor.harvested_per_passage[donor.passage_no-1] == number_seeded_et:

                #print('passage %d of donor %d finished at %.5f' % (donor.passage_no,donor_index,env.now))

                #Release the occupied resources to allow for new cultures

                #lab.occupied_incubators -= donor.required_incubators

 #               lab.occupied_workers -= donor.required_workers

 #               lab.occupied_bscs -= donor.required_bscs

                # print('Occupied workers after passage %d of donor %d finished in the outside loop' %(donor.passage_no,donor_index))
                # print(lab.occupied_workers)

                # print('Occupied bscs after passage %d of donor %d finished in the outside loop' %(donor.passage_no,donor_index))
                # print(lab.occupied_bscs)

                #print('Occupied incubators after passage %d of donor %d finished in the outside loop' %(donor.passage_no,donor_index))
                #print(lab.occupied_incubators)

                print('Final number of cells of passage %d are %d' % (donor.passage_no,donor.final_cells_passage[donor.passage_no-1]))

                #Put a structure to loop over and put the next passage of the donor on hold until workers are available.

                break

        #Update the total CPD of the passage

        donor.cpds = math.log(donor.final_cells_passage[donor.passage_no-1]/donor.initial_cells_passage[0])/math.log(2)

        #Check if the number of cells is above the end goal. Break if that's the case, otherwise increase the number of passages

#        if donor.final_cells_passage[donor.passage_no-1] > CELL_NUMBER_PER_DOSE:

        if donor.passage_no == gui.MAX_NO_PASSAGES:

            #Send simulation to finish if maximum passage was reached

            clause = 'maxpass'

            #AC - uncommented
            print('Maximum passages reached! End of simulation!')

            finish_simulation(env,lab,gui,donor,donor_index,clause)

            break

        elif round(donor.cpds,0) >= gui.MAXIMUM_NUMBER_CPD:

            #Send simulation to finish if maximum passage was reached

            clause = 'maxcpd'

            #AC - uncommented
            print('Maximum CPDs reached! End of simulation!')

            finish_simulation(env,lab,gui,donor,donor_index,clause)

            break

        else:

            #Increase the passage number

            donor.passage_no += 1
            #AC - debug
            print ("Donor {} - Passage No increased to {}".format( donor, donor.passage_no))
        yield env.timeout(0.0001)

    # if donor.passage_no > gui.MAX_NO_PASSAGES:
    #     gui.results.append_event(env.now, "Max_Passages_reached")

    # if donor.cpds > gui.MAXIMUM_NUMBER_CPD:
    #     gui.results.append_event(env.now, "Max_CPD_reached")

    print ("exited cycle cond 1 - donor passage {} <= max passage {}".format(donor.passage_no, gui.MAX_NO_PASSAGES))
    print ("exited cycle cond 2 - donor CPDS    {} <= MAX CPDS    {}".format(donor.cpds,       gui.MAXIMUM_NUMBER_CPD))

