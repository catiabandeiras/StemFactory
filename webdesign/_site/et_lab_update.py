#Imports the generic Python packages

import simpy
import random
import math
import numpy as np
import pandas as pd

def lab_queue_update(env,lab,donor,et_name,new_seed_vars,gui,int_db):

	'''Function aiming to change the queue capacity according to the chosen ET type'''

	if et_name in int_db.names_of_planar_ets:

		max_units_access(env,lab,donor,et_name,int_db.MAX_UNITS_RESOURCE_PLANAR,new_seed_vars)

		operation_times_access(env,lab,et_name,int_db.ET_OPERATION_TIMES_PLANAR,gui,int_db)

	elif et_name in int_db.names_of_suspension_ets:

		max_units_access(env,lab,donor,et_name,int_db.MAX_UNITS_RESOURCE_SUSPENSION,new_seed_vars)

		operation_times_access(env,lab,et_name,int_db.ET_OPERATION_TIMES_SUSPENSION,gui,int_db)


def max_units_access(env,lab,donor,et_name,max_units_dataframe,new_seed_vars):

	'''Function that looks inside the specific dataframe'''

	donor.required_workers = new_seed_vars[4]

	donor.required_bscs = new_seed_vars[5]

	donor.required_incubators = new_seed_vars[6]

	donor.et_type_per_passage[donor.passage_no-1] = et_name

	donor.no_ets_per_passage[donor.passage_no-1] = new_seed_vars[1]

	#Request space at the lab to update the worker queue capacity only if made possible

	# if lab.global_worker_queue.count + donor.required_workers <= lab.global_worker_queue.capacity:

	# 	donor.worker_queue = simpy.Resource(env,max_units_dataframe.loc[et_name,'worker']*donor.required_workers)

	# if lab.global_incubator_queue.count + donor.required_incubators <= lab.global_incubator_queue.capacity:

	# 	donor.incubator_queue = simpy.Resource(env,max_units_dataframe.loc[et_name,'incubator']*donor.required_incubators)

	donor.worker_queue = simpy.Resource(env,max_units_dataframe.loc[et_name,'worker']*donor.required_workers)

	donor.incubator_queue = simpy.Resource(env,max_units_dataframe.loc[et_name,'incubator']*donor.required_incubators)

	# if len(lab.list_of_workers) < TOTAL_WORKERS:

	# lab.list_of_workers.append(donor.worker_queue)



def operation_times_access(env,lab,et_name,op_times_dataframe,gui,int_db):

	'''Function that looks in the specific operation times dataframe to update the times'''

	lab.seeding_time = op_times_dataframe.loc[et_name,'seeding']

	lab.feeding_time = op_times_dataframe.loc[et_name,'feeding']

	lab.harvesting_time = op_times_dataframe.loc[et_name,'harvesting']

	if et_name in int_db.names_of_planar_ets:

		feeding_period = gui.FP_PLANAR

	elif et_name in int_db.names_of_suspension_ets:

		feeding_period = gui.FP_SUSPENSION

	lab.incubation_time = feeding_period