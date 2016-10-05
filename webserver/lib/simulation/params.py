# -*- coding: utf-8 -*-


class SimulationParams(object):

    def __init__(self):

        #Facility
        self.AREA_FACILITY = 0
        self.AREA_UNIT = 0
        self.TOTAL_WORKERS = 0
        self.TOTAL_BSC = 0
        self.TOTAL_INCUBATORS = 0
        self.TOTAL_BIOREACTORS = 0

        #Culture Conditions
        self.TYPE_OF_ET = ' '
        self.TYPE_OF_MC = ' '
        self.SOURCE_OF_MSC = ' '
        self.TYPE_OF_MEDIA = ' '

        #Growth characteristics
        self.INITIAL_CELLS_PER_DONOR_AVG = 1 # in millions
        self.INITIAL_CELLS_PER_DONOR_SD  = 0 # in millions
        self.MAXIMUM_NUMBER_CPD = 0 #
        self.MAX_NO_PASSAGES = 1 # between 1 and 5

        #    weirdness (are these the same? array vs several scalar)
        self.LIST_OF_MAX_GROWTH_RATES = [0]*5
        self.GR_P1 = 0
        self.GR_P2 = 0
        self.GR_P3 = 0
        self.GR_P4 = 0
        self.GR_P5 = 0

        # manual
        self.SD_PLANAR = 0 #seeding density
        self.SD_SUSPENSION = 0 #in suspension
        self.WORKING_VOLUME_RATIO = 0 #working volume suspension ratio
        self.WV_PLANAR = 0     #fraction replaced (planar)
        self.WV_SUSPENSION = 0 #fraction replaced (suspension)
        self.MC_ADH_RATIO = 0 #adhesion
        self.MC_CONC = 0 #microcarrier concentration

        self.FP_PLANAR = 0 #feeding period
        self.FP_SUSPENSION = 0
        self.HD_PLANAR = 0 #harvesting density
        self.HD_SUSPENSION = 0
        self.HEFF_PLANAR = 0 #harvesting efficiency
        self.HEFF_SUSPENSION = 0

        #demand
        self.CELL_NUMBER_PER_DOSE = 0 # in millions
        self.ANNUAL_DEMAND = 0 # doses / year
        self.LOT_SIZE = 0 #doses / lot


    def update(self, source):
        for (key, value) in source.iteritems():
            if value:
                self.__dict__[key] = value
