# -*- coding: utf-8 -*-

import math

from lib.simulation.donor_results  import SimulationDonorResults
from lib.simulation.cost_structure import SimulationCostStructure
from lib.simulation.event          import SimulationEvent


class SimulationResults(object):

    def __init__(self):
        self.donors = []
        self.events = []
        self.costStructure = SimulationCostStructure()
        self.events = []
        self.doses_manufactured = 0
        self.balance = 0
        self.days_to_meet_demand = 0
        self.days_bf_deadline = 0
        self.deadline_met = False


    def add_donor_results(self, spentDays, totalDoses, totalLots):

        self.donors.append(SimulationDonorResults(
            math.ceil(spentDays), totalDoses, totalLots
        ))


    def append_event(self, simTime, eventName):

        self.events.append(SimulationEvent(simTime, eventName))


    def set_costs(self, exp_tech, reagent, labor, facility, equipment, qualityControl, total, perDose):
        self.costStructure.expandTechnology = round(exp_tech, 2)
        self.costStructure.reagent          = round(reagent, 2)
        self.costStructure.labor            = round(labor, 2)
        self.costStructure.facility         = round(facility, 2)
        self.costStructure.equipmentUsage   = round(equipment, 2)
        self.costStructure.qualityControl   = round(qualityControl, 2)
        self.costStructure.totalCost        = round(total, 2)
        self.costStructure.costPerDose      = round(perDose, 2)

    def set_balance(self, balance):
        self.balance = round(balance, 2)
