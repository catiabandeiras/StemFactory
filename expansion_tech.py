#Imports the generic Python packages

import simpy
import random
import math

#IMPORT THE ANCILLARY METHODS MODULES

from get_places import *


def expansion_tech_run(env,et,donor,lab,gui,int_db):

    #First, try to find an available worker

    while True:

        if lab.occupied_workers < gui.TOTAL_WORKERS:

            worker_index = 0

            while worker_index < gui.TOTAL_WORKERS:

                #Select a worker

                worker = lab.list_of_workers[worker_index]

                if worker.count < worker.capacity:

                    with worker.request() as request:

                        yield request | env.timeout(0.0001)

                        donor.worker_queue = worker

                        lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])


                        #yield env.timeout(0.0001)

                        #print('Lab workers at %.5f seen by %s in the beginning of seeding are %d' % (env.now,et.full_name,lab.occupied_workers))       

                        #2) If worker is available, calls the seeding block

                        procedure = 'seeding'

                        bsc_procedure = bsc_et(env,et,donor,lab,procedure,gui,int_db)
                        env.process(bsc_procedure)

                        yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.seeding_time))

                        #print('Seeding of %s finished at %.5f' % (et.full_name,env.now))               

                        break

                else:

                    worker_index += 1

            break

        else:

            yield env.timeout(0.0001)

            continue
            
    #If harvesting before the density is favorable, do it

    while et.no_cells < min(et.harvest_density*et.area,gui.CELL_NUMBER_PER_DOSE*(gui.ANNUAL_DEMAND-lab.total_doses)):

        #Chooses if the process goes to a bioreactor system or is in the incubator only

        if et.base_name[0] == 'b':

            incubation = get_place_bioreactor(env,et,donor,lab,gui,int_db)

        else:

            incubation = get_place_incubator(env,et,donor,lab,gui,int_db)
        
        env.process(incubation)

        #print('Incubation of %s started at %.5f' % (et.full_name,env.now)) 

        yield env.timeout(lab.incubation_time)

        #print('Incubation of %s finished at %.5f' % (et.full_name,env.now)) 

        if et.no_cells >= et.harvest_density*et.area:

            '''Sent for harvesting when the number of cells in the flask to harvest is reached'''

            print('%s is sent for harvesting at %.4f' % (et.full_name,env.now))

            break

        else:

            '''Undergoes feeding when the period of incubation is reached'''

            while True:

                if lab.occupied_workers < gui.TOTAL_WORKERS:

                    worker_index = 0

                    while worker_index < gui.TOTAL_WORKERS:

                        #Select a worker

                        worker = lab.list_of_workers[worker_index]

                        if worker.count < worker.capacity:

                            with worker.request() as request:

                                yield request | env.timeout(0.0001)

                                donor.worker_queue = worker

                                lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])

                                #print('Feeding block initialized for %s at %.5f' % (et.full_name,env.now))

                                procedure = 'feeding'

                                #print('Feeding of %s started at %.5f' % (et.full_name,env.now)) 

                                bsc_procedure = bsc_et(env,et,donor,lab,procedure,gui,int_db)
                                env.process(bsc_procedure)

                                yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.feeding_time))

                                #print('Feeding of %s finished at %.5f' % (et.full_name,env.now)) 


                                #print('Feeding block terminated for %s at %.5f' % (et.full_name,env.now))                

                                break

                        else:

                            worker_index += 1

                    break

                else:

                    yield env.timeout(0.0001)

                    continue

#            print(lab.reagent_volumes)

    #4) Check that the bsc and worker are not busy before going to harvesting

    while True:

        '''Launches the harvesting steps'''

        worker_index = 0
        harvested = 0

        while worker_index < gui.TOTAL_WORKERS:

            #Select a worker

            worker = lab.list_of_workers[worker_index]

            #print(lab.list_of_workers)

            if worker.count < worker.capacity:

                # print('Stats before harvesting queue request of %s' % et.full_name)
                # print(donor.donor_index)
                # print(lab.occupied_workers)
                # print(env.now)

                with worker.request() as request:

                    yield request | env.timeout(0.0001)

                    donor.worker_queue = worker

                    lab.occupied_workers = sum([lab.list_of_workers[worker_index].count for worker_index in range(gui.TOTAL_WORKERS)])

                    #yield env.timeout(0.0001)

                    #print('Lab workers at %.5f seen by %s in the beginning of harvesting are %d' % (env.now,et.full_name,lab.occupied_workers))          

                    #print('Harvesting block initialized for %s at %.5f' % (et.full_name,env.now))  

                    procedure = 'harvesting'

                    # print('Harvested flasks per passage at %.5f' % env.now)
                    # print(donor.harvested_per_passage[donor.passage_no-1]) 

                    bsc_procedure = bsc_et(env,et,donor,lab,procedure,gui,int_db)
                    env.process(bsc_procedure)

                    #print('Harvesting of %s started at %.5f' % (et.full_name,env.now)) 

                    yield env.timeout((donor.worker_queue.count/donor.worker_queue.capacity)*(lab.harvesting_time)+int_db.FIXED_HARVESTING_TIME)

                    #print('Harvesting of %s finished at %.5f' % (et.full_name,env.now)) 

                    #print('Harvesting block terminated for %s at %.5f' % (et.full_name,env.now))

                    harvested = 1                    

                    break

            else:

                worker_index += 1

        if harvested == 1:

            break

        else:

            yield env.timeout(0.0001)

            continue

 #       else:

 #           yield env.timeout(0.0001)

 #           continue

    # print('Worker queue right before finishing the processing')
    # print(et.full_name)
    # worker_counts = [lab.list_of_workers[worker_index].count for worker_index in range(TOTAL_WORKERS)]
    # print(worker_counts)
    # print(env.now)

    # print('Harvested flasks per passage at %.5f' % env.now)
    # print(donor.harvested_per_passage[donor.passage_no-1]) 


    env.exit()
