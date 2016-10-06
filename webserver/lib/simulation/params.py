# -*- coding: utf-8 -*-


from lib.simulation.results import SimulationResults


class FakeText(object):
    def __init__(self): self.val = ''
    def insert(self, f, t):
        self.val += "\n{}: {}".format(f, t)
        print ("\nFake Text: {}: {}".format(f, t) )


#actually more of a broker...
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
        self.INITIAL_CELLS_PER_DONOR_AVG = 1.05e6 # in millions
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
        self.HEFF_PLANAR = 1 #harvesting efficiency
        self.HEFF_SUSPENSION = 0

        #demand
        self.CELL_NUMBER_PER_DOSE = 75e6 # in millions
        self.ANNUAL_DEMAND = 1 # doses / year
        self.LOT_SIZE = 1 #doses / lot

        self.types = {
            'TYPE_OF_ET': str,
            'TYPE_OF_MC': str,
            'SOURCE_OF_MSC': str,
            'TYPE_OF_MEDIA' : str,
            'TOTAL_WORKERS': int,
            'MAX_NO_PASSAGES': int,
        }

        #fake text
        self.text = FakeText()

        #simulation results
        self.results = SimulationResults()


    def example_set_simulation_output_x(self, value):
        self.value = value


    def update(self, source):
        for (key, value) in source.items(): #iteritems in python2

            if value: # empty values are considered 0
                vartype = self.types.get(key)
                print (vartype, key, value)
                if vartype == str:
                    tval = value
                elif vartype == int:
                    tval = int(value)
                elif vartype == float:
                    tval = float(value)
                else:
                    tval = float(value)

                self.__dict__[key] = tval
