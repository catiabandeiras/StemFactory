import sys
import simpy
import random
import math
import logging
import time
import numpy as np
import csv


def final_cost_info(env,lab,gui,int_db):

    #First, retrieve the costs with ETs

    final_et_costs = costs_ET(env,lab,gui,int_db)

    print('The final total costs of ET are %.2f EUR.' % final_et_costs)

    #text_widget = gui.text_widget

    gui.text.insert('3.0','The final total costs of ET are %.2f EUR. \n' % final_et_costs)

    #Afterwards, define the costs of reagents

    final_reagent_costs = costs_reagents(env,lab,gui,int_db)

    print('The final total costs of reagents are %.2f EUR.' % final_reagent_costs)

    gui.text.insert('4.0','The final total costs of reagents are %.2f EUR. \n' % final_reagent_costs)

    final_labor_costs = costs_labor(env,lab,gui,int_db)

    print('The final total labor costs are %.2f EUR.' % final_labor_costs)

    gui.text.insert('5.0','The final total labor costs are %.2f EUR. \n' % final_labor_costs)

    final_facility_costs = costs_facility(env,lab,int_db)

    print('The final total costs of the facility are %.2f EUR.' % final_facility_costs)

    gui.text.insert('6.0','The final total costs of the facility are %.2f EUR. \n' % final_facility_costs)

    final_equip_util_costs = costs_equip_util(env,lab,int_db)

    print('The final total costs with equipment utilization are %.2f EUR.' % final_equip_util_costs)

    gui.text.insert('7.0','The final total costs with equipment utilization are %.2f EUR. \n' % final_equip_util_costs)

    final_qc_costs = costs_qc(env,lab,int_db)

    print('The final total costs of quality control are %.2f EUR.' % final_qc_costs)

    gui.text.insert('8.0','The final total costs of quality control are %.2f EUR. \n' % final_qc_costs)

    final_total_costs = (final_et_costs + final_reagent_costs + final_labor_costs + final_facility_costs + final_equip_util_costs + final_qc_costs)

    array_final_costs = np.array([final_et_costs, final_reagent_costs, final_labor_costs, final_facility_costs, final_equip_util_costs, final_qc_costs])*100/final_total_costs

    print(np.round(array_final_costs,2))

    final_costs_per_dose = final_total_costs / lab.total_doses

    print('The total costs per dose are %.2f EUR.' % final_costs_per_dose)

    print(final_costs_per_dose)
    print(gui.SALES_PRICE)

    gui.NET_PROFIT += (gui.SALES_PRICE - final_costs_per_dose)*gui.ANNUAL_DEMAND

    print(gui.NET_PROFIT)

    gui.text.insert('9.0','The total costs per dose are %.2f EUR. \n' % final_costs_per_dose)

    if gui.NET_PROFIT > 0:

        gui.text.insert('10.0','Congrats! You have now a profit of %.2f EUR! \n' %gui.NET_PROFIT)
        gui.results.appendEvent(env.now, 'loss')

    else:

        gui.text.insert('10.0','Tragedy! You are broke!\n')
        gui.results.appendEvent(env.now, 'profit')

    # AC MOD - track costs
    gui.results.set_costs(
        final_et_costs, final_reagent_costs, final_labor_costs, final_facility_costs,
        final_equip_util_costs, final_qc_costs, final_total_costs, final_costs_per_dose
    )

    #Add a test to write the values to a file

    f = open("simdata_test.txt",'w')
    f.write("Total costs per dose "+str(final_costs_per_dose))
    f.close()

    #Write the CPDs to a file

    cpds_dict = lab.cpds_per_donor
    #print(cpds_dict)

    output_file = open('CPDs.csv', 'w',newline = '')

    writer = csv.writer(output_file)

    for key, value in cpds_dict.items():
        #print(key,value)
        writer.writerow([key, value])

    output_file.close()

    #Write the passage numbers to a file

    passages_dict = lab.final_passage_per_donor

    output_file = open('Passages.csv', 'w',newline = '')

    writer = csv.writer(output_file)

    for key, value in passages_dict.items():
        writer.writerow([key, value])

    output_file.close()

def costs_ET(env,lab,gui,int_db):

    #Multiply the total number of ETs used per their costs - also input the mass of MC used because it makes part of the ET

    if gui.TYPE_OF_ET == 'microcarrier':

        final_et_costs = sum(lab.planar_used*int_db.UNIT_COST_PLANAR_ETS) + sum(lab.mc_based_used*int_db.UNIT_COST_SUSPENSION_ETS) + lab.mc_mass * int_db.COST_PER_GRAM_MC[gui.TYPE_OF_MC]

    else:

        final_et_costs = sum(lab.planar_used*int_db.UNIT_COST_PLANAR_ETS)

    return final_et_costs

def costs_reagents(env,lab,gui,int_db):

    #Check the volumes of culture media, harvesting material and coating material used.

    final_reagent_costs = sum(np.array(lab.reagent_volumes) * np.array([int_db.COST_PER_ML_CULTURE_MEDIA[gui.TYPE_OF_MEDIA],int_db.COST_PER_ML_COATING,int_db.COST_PER_ML_HARVESTING]))

    return final_reagent_costs

def costs_labor(env,lab,gui,int_db):

    #Calcualte the workers. Assume that all workers are always hired and perfoming other tasks, like cleaning and recalibration, if they are not manufacturing.

    final_labor_costs = math.ceil(env.now)*gui.TOTAL_WORKERS*int_db.WORKER_COST

    return final_labor_costs

def costs_facility(env,lab,int_db):

    #Accounts for the time involved in the simulation and how the costs of facility per day are accounted for.

    final_facility_costs = math.ceil(env.now) * (int_db.FACILITY_DAILY_COST + int_db.INCUBATORS_DAILY_COST + int_db.BSC_DAILY_COST + int_db.C02_SUPPLY_DAILY_COST + int_db.OTHER_GASES_DAILY_COST + int_db.ADD_SUPPLIES_DAILY_COST + int_db.REQUALIFICATION_DAILY_COSTS + int_db.MAINTENANCE_DAILY_COSTS + int_db.CLEANING_COSTS + int_db.GARMENT_COSTS + int_db.OPERATION_COSTS_ENERGY_AIR_LIGHT)

    return final_facility_costs

def costs_equip_util(env,lab,int_db):

    #Accounts for the number of equipments used in each passage and donor - structure also needs to be retaught

    #print('final time of bsc is %.4f' % lab.time_of_bsc)
    #print('final time of incubators is %.4f' % lab.time_of_incubator)

    final_equip_util_costs = lab.time_of_bsc * int_db.OPERATION_COST_BSC + lab.time_of_incubator * int_db.OPERATION_COST_INCUBATOR + lab.time_of_bioreactor * int_db.OPERATION_COST_BIOREACTOR

    return final_equip_util_costs

def costs_qc(env,lab,int_db):

    #Accounts for the costs of quality control

    final_qc_costs = int_db.QC_COSTS*lab.total_lots

    return final_qc_costs

