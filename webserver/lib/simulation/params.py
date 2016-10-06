# -*- coding: utf-8 -*-


class SimulationParams(object):

    def __init__(self):

        #Net profit and sales price

        self.NET_PROFIT = 0
        self.SALES_PRICE = 25000

        #Facility
        self.AREA_FACILITY = 400
        self.AREA_UNIT = 1
        self.TOTAL_WORKERS = 1
        self.TOTAL_BSC = 1
        self.TOTAL_INCUBATORS = 1
        self.TOTAL_BIOREACTORS = 0

        #Culture Conditions
        self.TYPE_OF_ET = 'planar'
        self.TYPE_OF_MC = 'solohill'
        self.SOURCE_OF_MSC = 'bm'
        self.TYPE_OF_MEDIA = 'fbs'

        #Growth characteristics
        self.INITIAL_CELLS_PER_DONOR_AVG = 1.05 # in millions
        self.INITIAL_CELLS_PER_DONOR_SD  = 0 # in millions
        self.MAXIMUM_NUMBER_CPD = 0 #
        self.MAX_NO_PASSAGES = 3 # between 1 and 5

        #    weirdness (are these the same? array vs several scalar)
        self.LIST_OF_MAX_GROWTH_RATES = [0]*5
        self.GR_P1 = 0.21
        self.GR_P2 = 0.20
        self.GR_P3 = 0.18
        self.GR_P4 = 0
        self.GR_P5 = 0

        # manual
        self.SD_PLANAR = 3000 #seeding density
        self.SD_SUSPENSION = 0 #in suspension
        self.WORKING_VOLUME_RATIO = 0 #working volume suspension ratio
        self.WV_PLANAR = 1     #fraction replaced (planar)
        self.WV_SUSPENSION = 0 #fraction replaced (suspension)
        self.MC_ADH_RATIO = 0 #adhesion
        self.MC_CONC = 0 #microcarrier concentration

        self.FP_PLANAR = 3 #feeding period
        self.FP_SUSPENSION = 0
        self.HD_PLANAR = 25000 #harvesting density
        self.HD_SUSPENSION = 0
        self.HEFF_PLANAR = 0.75 #harvesting efficiency
        self.HEFF_SUSPENSION = 0

        #demand
        self.CELL_NUMBER_PER_DOSE = 75 # in millions
        self.ANNUAL_DEMAND = 1 # doses / year
        self.LOT_SIZE = 1 #doses / lot


    def update(self, source):
        for (key, value) in source.items(): #iteritems in python2
            if key not in ('TYPE_OF_ET','TYPE_OF_MC','SOURCE_OF_MSC','TYPE_OF_MEDIA'):
                if value:
                    print(key,value)
                    self.__dict__[key] = round(float(value),2)
            else:
                if value:
                    self.__dict__[key] = value                    
