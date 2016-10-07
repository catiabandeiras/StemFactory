#Module that will contain the definition of the internal database class

#So far it's a class that contains every possible variable

import numpy as np

import pandas as pd

class InternalDatabase(object):

	def __init__(self,gui):

		#Start by inputting what is the fraction of the building that is clean rooms

		self.CLEAN_ROOMS_RATIO = 0.2

		#Input the cost per sq mt of clean rooms and non-clean room space in the GMP facility (in €)

		self.COST_SQ_MT_CLEAN_ROOM = 5815

		self.COST_SQ_MT_OTHERS = 3392

		#Input the facility depreciation period (in years)

		self.FACILITY_DEPRECIATION_PERIOD = 15

		#Input the equipment depreciation period (in years)

		self.EQUIPMENT_DEPRECIATION_PERIOD = 5

		#Calculate the daily costs of the building

		self.CLEAN_ROOM_DAILY_COST = round(self.COST_SQ_MT_CLEAN_ROOM*self.CLEAN_ROOMS_RATIO,2)

		self.OTHER_ROOM_DAILY_COST = round(self.COST_SQ_MT_OTHERS*(1-self.CLEAN_ROOMS_RATIO),2)

		print(type(self.CLEAN_ROOM_DAILY_COST))

		print(type(self.OTHER_ROOM_DAILY_COST))

		print(type(gui.AREA_FACILITY))

		print(type(self.FACILITY_DEPRECIATION_PERIOD))

		#Multiplies the daily costs of GMP facility per sq mt per the area facility and divides by the depreciation cost 

		self.FACILITY_DAILY_COST = (self.CLEAN_ROOM_DAILY_COST+self.OTHER_ROOM_DAILY_COST)*gui.AREA_FACILITY/(self.FACILITY_DEPRECIATION_PERIOD*365.25)

		#Input the costs of acquisition of equipment

		self.INCUBATOR_COST = 16000

		self.BSC_COST = 15300

		self.BIOREACTOR_SYSTEM_COST = 56000

		#Calculate the daily equipment acqusition costs

		self.INCUBATORS_DAILY_COST = (self.INCUBATOR_COST*gui.TOTAL_INCUBATORS)/(self.EQUIPMENT_DEPRECIATION_PERIOD*365.25)

		self.BSC_DAILY_COST = (self.BSC_COST*gui.TOTAL_BSC)/(self.EQUIPMENT_DEPRECIATION_PERIOD*365.25)

		self.BIOREACTOR_SYSTEM_DAILY_COST = (self.BIOREACTOR_SYSTEM_COST*gui.TOTAL_BIOREACTORS)/(self.EQUIPMENT_DEPRECIATION_PERIOD*365.25)

		#Input the power of the equipment (in watts)

		self.INCUBATOR_POWER = 1500

		self.BSC_POWER = 1400

		self.BIOREACTOR_POWER = 1700

		#Input the cost of electricity per kWh

		self.PRICE_ELECTRICITY = 0.1641

		#Input the operation costs of the equipment (in days)

		self.OPERATION_COST_INCUBATOR = self.PRICE_ELECTRICITY*(self.INCUBATOR_POWER/1000)*24

		self.OPERATION_COST_BSC = self.PRICE_ELECTRICITY*(self.BSC_POWER/1000)*24

		self.OPERATION_COST_BIOREACTOR = self.PRICE_ELECTRICITY*(self.BIOREACTOR_POWER/1000)*24

		#Labor costs estimated from El Enein PhD thesis (in EUR) - per worker per day!

		self.WORKER_COST = 50

		#Input gases daily costs

		self.C02_SUPPLY_DAILY_COST = 6000/365.25

		self.OTHER_GASES_DAILY_COST = 15600/365.25

		#Input office and non-manufacturing lab supplies:

		self.ADD_SUPPLIES_DAILY_COST = 7900/365.25

		#Input equipment requalification costs:

		self.REQUALIFICATION_DAILY_COSTS = 65400/365.25

		#Input the preventive maintenance costs of the equipment:

		self.MAINTENANCE_DAILY_COSTS = 52800/365.25

		#Input cleaning and disinfection costs of the facility:

		self.CLEANING_COSTS = 28000/365.25

		#Input the daily garment costs

		self.GARMENT_COSTS = 2000/365.25

		#Input the operation costs of energy for lights and air conditioning

		self.OPERATION_COSTS_ENERGY_AIR_LIGHT = 54461/365.25

		#Inputs the costs of quality control per lot

		self.QC_COSTS = 10000

		self.names_of_planar_ets = ['t-flask25',
							   't-flask75',
							   't-flask175',
							   't-flask225',
							   'cellstack1',
							   'cellstack2',
							   'cellstack5',
							   'cellstack10']

		self.names_of_microcarriers = ['cultispher',
								  'cytodex1',
								  'cytodex3',
								  'solohill',
								  'cellbind',
								  'synthemax2']

		self.names_of_suspension_ets = ['spinner125',
								   'spinner500',
								   'spinner1000',
								   'bioreactor1.8',
								   'bioreactor5',
								   'bioreactor14',
								   'bioreactor50']

		self.names_of_resources = ['incubator',
							 'worker']

		#Provide area in cm^2 for planar

		self.AREA_PLANAR = pd.Series(data = [25,75,175,225,636,636*2,636*5,636*10],
								index = self.names_of_planar_ets)


		#Provide area in cm^2/g for microcarriers

		self.AREA_MC = pd.Series(data = [40000,4400,2700,360,360,360],
							index = self.names_of_microcarriers)

		#Volume of the suspension single use vessels in L

		# VOLUME_SUSPENSION = pd.Series(data = [0.125,0.5,1,20,200,500,1000,2000],
		# 							  index = names_of_suspension_ets)

		self.VOLUME_SUSPENSION = pd.Series(data = [0.125,0.5,1,1.8,5,14,50],
		 							  index = self.names_of_suspension_ets)

		#Determine the area of suspension technologies (in cm^2) from the user inputs

		if gui.TYPE_OF_ET == 'microcarrier':

			self.AREA_SUSPENSION = self.VOLUME_SUSPENSION*gui.WORKING_VOLUME_RATIO*gui.MC_CONC*int_db.AREA_MC[gui.TYPE_OF_MC]

		else:

			self.AREA_SUSPENSION = 0

		#Determine the seeding requirements for planar and suspension technologies (in ml)

		self.MEDIA_VOLUME_PLANAR_ETS = pd.Series(data = [5,15,35,45,130,260,650,1300],
											index = self.names_of_planar_ets)

		self.MEDIA_VOLUME_SUSPENSION_ETS = self.VOLUME_SUSPENSION*gui.WORKING_VOLUME_RATIO*1000

		#Determine the feeding requirements for planar and suspension technologies (in ml)

		self.FEEDING_VOLUME_PLANAR_ETS = self.MEDIA_VOLUME_PLANAR_ETS*gui.WV_PLANAR

		self.FEEDING_VOLUME_SUSPENSION_ETS = self.MEDIA_VOLUME_SUSPENSION_ETS*gui.WV_SUSPENSION

		#Determine the harvesting volumes required (in ml)

		self.HARVEST_VOLUME_PLANAR_ETS = pd.Series(data = [1.75,3.5,7,9,25,50,125,250],
												index = self.names_of_planar_ets)

		#assume that the harvesting volume used is 20% of the volume of seeding with culture medium because of the relationship
		#holding for planar technologies

		self.HARVEST_VOLUME_SUSPENSION_ETS = self.VOLUME_SUSPENSION*gui.WORKING_VOLUME_RATIO*1000/5

		#Number of maximum units per resource

		self.MAX_UNITS_RESOURCE_PLANAR = pd.DataFrame(
									data = [[100,1],
											[100,1],
											[100,1],
											[100,1],
											[60,1],
											[60,1],
											[24,1],
											[12,1]],
									index = self.names_of_planar_ets,
									columns = self.names_of_resources
									)

		self.MAX_UNITS_RESOURCE_SUSPENSION = pd.DataFrame(
									data = [[12,2],
											[12,2],
											[6,2],
											[1,1],
											[1,1],
											[1,1],
											[1,1]],
									index = self.names_of_suspension_ets,
									columns = self.names_of_resources
									)

		self.MAX_INCUBATORS_PER_DONOR = 1

		#Input the times per operation - do it later when I can get information from the suppliers.

		#Input the costs of each expansion technology single use unit (in EUR)

		self.UNIT_COST_PLANAR_ETS = pd.Series(data = [1.65,4.85,7.38,8.55,33.89,60.12,131.96,142.72],
												index = self.names_of_planar_ets)

		self.UNIT_COST_SUSPENSION_ETS = pd.Series(data = [67.68,70.40,173.02,250,575,690,1470],
												index = self.names_of_suspension_ets)

		#Input the costs/gram of each microcarrier type in the library

		self.COST_PER_GRAM_MC = pd.Series(data = [18.10,16.34,14.25,3.00,9.66,19.33],
										index=self.names_of_microcarriers)

		#Input if microcarriers need CellBIND coating in xeno free conditions (all uncharged microcarriers)

		self.NEEDS_COATING_MC = pd.Series(data = [0,0,0,1,0,0],
										index=self.names_of_microcarriers)

		#Input the coating volume per area unit required in case the microcarriers need coating

		self.COATING_PER_AREA = 0.02

		#Input the operation times per procedure in the planar operations of handling the maximum number of units - in days

		self.ET_OPERATION_TIMES_PLANAR = pd.DataFrame(
		    data = [[0.38/(24*10),0.38/(24*10),0.5/(24*10)],
		           [0.38/(24*10),0.38/(24*10),0.5/(24*10)],
		           [0.38/(24*10),0.38/(24*10),0.5/(24*10)],
		           [0.38/(24*10),0.38/(24*10),0.5/(24*10)],
		           [0.15/24,0.15/24,0.06/24],
		           [0.15/24,0.15/24,0.06/24],
		           [0.20/24,0.20/24,0.16/24],
		           [0.25/24,0.25/24,0.25/24]],
		    index = self.names_of_planar_ets,
		    columns = ['seeding','feeding','harvesting']
		    )

		#Input the fixed harvesting time (7 min trypsin and 7 min centrifuge). Independent of the number of flasks and the expansion technology.
		self.FIXED_HARVESTING_TIME_PLANAR = 14/(60*24)

		self.FIXED_HARVESTING_TIME = self.FIXED_HARVESTING_TIME_PLANAR

		self.WORKER_GRAB_TIME = 0.0001

		self.ET_OPERATION_TIMES_SUSPENSION = pd.DataFrame(
		    data = [[1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24],
		           [1.5/24,(0.16/24),0.75/24]],
		    index = self.names_of_suspension_ets,
		    columns = ['seeding','feeding','harvesting']
		    )

		#Add a list of the maximum growth rates to the internal database based on the GUI access

		self.LIST_OF_MAX_GROWTH_RATES = [gui.GR_P1,gui.GR_P2,gui.GR_P3,gui.GR_P4,gui.GR_P5]


		#Adds more information about the costs of the reagents

		self.names_of_media = ['fbs','hpl','stempro']

		self.COST_PER_ML_CULTURE_MEDIA = pd.Series(data = [0.15,0.21,0.61],
										index = self.names_of_media)

		self.COST_PER_ML_COATING = 0.94

		self.COST_PER_ML_HARVESTING = 0.04


#int_db = InternalDatabase()