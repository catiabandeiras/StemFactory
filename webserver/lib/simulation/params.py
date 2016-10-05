# -*- coding: utf-8 -*-


class SimulationParams(object):

    def __init__(self):

        self.AREA_FACILITY = 0
        self.AREA_UNIT = 0
        self.TOTAL_WORKERS = 0
        self.TOTAL_BSC = 0
        self.TOTAL_INCUBATORS = 0
        self.TOTAL_BIOREACTORS = 0
        self.TYPE_OF_ET = ' '
        self.TYPE_OF_MC = ' '
        self.SOURCE_OF_MSC = ' '
        self.TYPE_OF_MEDIA = ' '
        self.INITIAL_CELLS_PER_DONOR = 0
        self.MAXIMUM_NUMBER_CPD = 0
        self.MAX_NO_PASSAGES = ''
        self.LIST_OF_MAX_GROWTH_RATES = [0]*5
        self.GR_P1 = 0
        self.GR_P2 = 0
        self.GR_P3 = 0
        self.GR_P4 = 0
        self.GR_P5 = 0
        self.SD_PLANAR = 0
        self.SD_SUSPENSION = 0
        self.WORKING_VOLUME_RATIO = 0
        self.WV_PLANAR = 0
        self.WV_SUSPENSION = 0
        self.MC_ADH_RATIO = 0
        self.MC_CONC = 0
        self.FP_PLANAR = 0
        self.FP_SUSPENSION = 0
        self.HD_PLANAR = 0
        self.HD_SUSPENSION = 0
        self.HEFF_PLANAR = 0
        self.HEFF_SUSPENSION = 0
        self.CELL_NUMBER_PER_DOSE = 0
        self.ANNUAL_DEMAND = 0
        self.LOT_SIZE = 0


    def update(self, source):
        for (key, value) in source:
            if value:
                self.__dict__[key] = value
