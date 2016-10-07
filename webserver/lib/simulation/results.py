# -*- coding: utf-8 -*-

from lib.simulation.donor_results  import SimulationDonorResults
from lib.simulation.cost_structure import SimulationCostStructure
from lib.simulation.event          import SimulationEvent


class SimulationResults(object):

    def __init__(self):
        self.donors = []
        self.costStructure = SimulationCostStructure()
        self.events = []
        self.balance = 0


    def add_donor_results(self, spentDays, totalDoses, totalLots):

        self.donors.append(SimulationDonorResults(spentDays, totalDoses, totalLots))


    def append_event(self, simTime, eventName):

        self.events.append(SimulationEvent(simTime, eventName))


    def set_costs(self, exp_tech, reagent, labor, facility, equipment, qualityControl, total, perDose):
        self.costStructure.expandTechnology = exp_tech
        self.costStructure.reagent          = reagent
        self.costStructure.labor            = labor
        self.costStructure.facility         = facility
        self.costStructure.equipmentUsage   = equipment
        self.costStructure.qualityControl   = qualityControl
        self.costStructure.totalCost        = total
        self.costStructure.costPerDose      = perDose

