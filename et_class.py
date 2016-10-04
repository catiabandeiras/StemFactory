#Imports the generic Python packages

import simpy
import random
import math

class ExpansionTechnology(object):

	def __init__(self,env,gui,int_db,donor,donor_index,new_seed_tuple,harvest_density,no_instance):
		#print('Laboratory constructor called')

#		Donor.__init__(self,env,donor_index)

		#Inputs the name to make the variables easier to find in either planar or suspension areas

		name = new_seed_tuple[0]

		self.base_name = name

		self.full_name = name+'-D'+str(donor_index)+'-P'+str(donor.passage_no)+'-N'+str(no_instance)

		#Inputs the seeding density to know how many cells are the starting point

		seeding_density = new_seed_tuple[2]

		self.seeding_density = seeding_density

		self.harvest_density = harvest_density

		#Initialize the number of cells

		area = new_seed_tuple[3]

		self.area = area

		self.no_cells = seeding_density*area

		self.initial_cells = self.no_cells

		#Searches for the right apparent growth rate according to the passage number

		self.growth_rate = int_db.LIST_OF_MAX_GROWTH_RATES[donor.passage_no-1]

		self.no_instance = no_instance

		#Initialize the number of days in incubation

		self.days_incubated = 0


	def show_info_et(self):

		print('expansion technology unit constructor created')
		print('expansion technology is of type '+self.base_name)
		print('full name of expansion technology is '+self.full_name)
		print('initial seeding density is '+str(self.seeding_density)+' cells/cm^2')


# env = simpy.Environment()

# lab = Laboratory(env)
# lab.show_info_lab()

# donor = Donor(env,0)

# donor.show_info_donor()

# et = ExpansionTechnology(env,0,new_seed_tuple,harvest_density,no_instance)

# et.show_info_et()


