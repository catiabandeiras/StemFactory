#the GUI to run the MSC

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#Import the discrete event simulation modules

import simpy
import random
import time
import sys

#Increase the recursion limit to avoid the limits of recursion with scipy

sys.setrecursionlimit(5000)

#from pass_example import *
from int_database import *

from labsetup_new import *

class MainGui:

	def __init__(self,master):

		#Put all the applications here

		self.menubar = Menubar(master,self)

		self.frame = ttk.Frame(master)

		#Stack the frame

		self.frame.pack()

		ttk.Label(self.frame,text="Output messages:").grid(row=1,column=0)
		self.text = Text(self.frame,width=80,height=20)
		self.text.grid(row=2,column=0,columnspan=3)

		#self.text.insert('1.0','Created GUI\n')

		#Initialize the global variables

		self.NET_PROFIT = 0

		self.SALES_PRICE = 25000

		self.AREA_FACILITY = 0

		self.AREA_UNIT = 0

		self.TOTAL_WORKERS = 0

		self.TOTAL_BSC = 0

		self.TOTAL_INCUBATORS = 0

		self.TOTAL_BIOREACTORS = 0

		self.TYPE_OF_ET = ' '

		self.TYPE_OF_MC	= ' '

		self.SOURCE_OF_MSC = ' '

		self.TYPE_OF_MEDIA = ' '

		self.INITIAL_CELLS_PER_DONOR_AVG = 0

		self.INITIAL_CELLS_PER_DONOR_SD = 0

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

class Menubar(MainGui):

	def __init__(self,master,main_gui):

		#Creates a menubar constructor

		self.menubar = Menu(master)

		master.config(menu = self.menubar)

		#Creates a notebook constructor

		project = Menu(self.menubar)
		help = Menu(self.menubar)
		about = Menu(self.menubar)

		self.menubar.add_cascade(menu = project, label = 'Project')
		project.add_command(label = "Define parameters",command = lambda : self.define_parms(master,main_gui))
		project.add_command(label = "Start simulation",command = lambda : self.start_simulation(master,main_gui))

		self.menubar.add_cascade(menu = help, label = 'Help')
		self.menubar.add_cascade(menu = about, label = 'About')

	def define_parms(self,master,main_gui):

		self.topwindow = TopWindow(master,main_gui)

		#MainGui.AREA_FACILITY = 200

	def start_simulation(self,master,main_gui):

		#self.AREA_FACILITY = 

		result = messagebox.askyesno(title = 'Start simulation', message = 'Are you sure you want to start the simulation?')		

		if result == True:

			#Launch the simulation through the function

			#self.run_simulation()
			print('Start the simulation!')
			#print(MainGui.AREA_FACILITY)

			#create an instance of the class internal database

			int_db = InternalDatabase(main_gui)

			env = simpy.Environment()

			env.process(labsetup(env,main_gui,int_db))

			env.run(until=365.25)

class TopWindow:

	def __init__(self,master,main_gui):

		#Creates the window

		self.window_new = Toplevel(master)
		self.window_new.title('Define Model Parameters')

		#Attaches the notebook panel

		self.notebook = MainNotebook(self.window_new,main_gui)

class MainNotebook:

	def __init__(self,topwindow,main_gui):

		self.notebook = ttk.Notebook(topwindow)
		self.notebook.pack()

		#Add each notebook frame as possible

		self.facility = FacilityPanel(self.notebook,main_gui)
		self.culture = CulturePanel(self.notebook,main_gui)
		self.growth = GrowthPanel(self.notebook,main_gui)
		self.manual = ManualPanel(self.notebook,self.culture,main_gui)
		self.demand = DemandPanel(self.notebook,main_gui)

class FacilityPanel:

	def __init__(self,main_notebook,main_gui):

		self.frame = ttk.Frame(main_notebook)
		main_notebook.add(self.frame,text = "Facility")

		#Create the label and entry for total area
		ttk.Label(self.frame,text="Total GMP facility area:").grid(row=0,column=0)
		self.total_area = ttk.Entry(self.frame,width=15)
		self.total_area.insert(END,'400')
		self.total_area.config(state=DISABLED)
		self.total_area.grid(row=1,column=0)

		#Create a label for the choice of unit area
		ttk.Label(self.frame,text="Area unit:").grid(row=0,column=1)
		self.area_unit = IntVar()
		self.area_unit.set(1)
		#self.area_unit.config(state=DISABLED)
		ttk.Radiobutton(self.frame,text="sq. mt.",variable=self.area_unit,value=1).grid(row=1,column=1)
		ttk.Radiobutton(self.frame,text="sq. ft.",variable=self.area_unit,value=2).grid(row=2,column=1)


		#Create the labels for numbers
		ttk.Label(self.frame,text = "Number of workers:").grid(row=3,column=0)
		self.total_workers = ttk.Entry(self.frame,width=15)
		self.total_workers.insert(END,'1')
		self.total_workers.config(state=DISABLED)
		self.total_workers.grid(row=4,column=0)

		#Create the labels for numbers
		ttk.Label(self.frame,text = "Number of BSCs:").grid(row=3,column=1)
		self.total_bscs = ttk.Entry(self.frame,width=15)
		self.total_bscs.insert(END,'1')
		self.total_bscs.config(state=DISABLED)
		self.total_bscs.grid(row=4,column=1)

		#Create the labels for numbers
		ttk.Label(self.frame,text = "Number of incubators:").grid(row=5,column=0)
		self.total_incubators = ttk.Entry(self.frame,width=15)
		self.total_incubators.insert(END,'1')
		self.total_incubators.config(state=DISABLED)
		self.total_incubators.grid(row=6,column=0)

		#Create the labels for numbers
		ttk.Label(self.frame,text = "Number of bioreactor systems:").grid(row=5,column=1)
		self.total_bioreact = ttk.Entry(self.frame,width=15)
		self.total_bioreact.insert(END,'1')
		self.total_bioreact.config(state=DISABLED)
		self.total_bioreact.grid(row=6,column=1)
		#print(type(self.total_bioreact.get()))

		main_gui.AREA_FACILITY = int(self.total_area.get())
		main_gui.AREA_UNIT = self.area_unit.get()
		main_gui.TOTAL_WORKERS = int(self.total_workers.get())
		main_gui.TOTAL_BSC = int(self.total_bscs.get())
		main_gui.TOTAL_INCUBATORS = int(self.total_incubators.get())
		main_gui.TOTAL_BIOREACTORS = int(self.total_bioreact.get())

		main_gui.NET_PROFIT = 0

		main_gui.SALES_PRICE = 25000

		#Add the buttons

		ttk.Button(self.frame,text="Save",command = lambda: self.save_facility(main_gui)).grid(row=7,column=0,pady = 5,padx=5,sticky="e")
		ttk.Button(self.frame,text="Clear",command = lambda: self.clear_facility()).grid(row=7,column=1,pady = 5,padx=5,sticky="w")

	def save_facility(self,main_gui):

		#Method where all the values from facility frame will be saved
		main_gui.AREA_FACILITY = int(self.total_area.get())
		main_gui.AREA_UNIT = self.area_unit.get()
		main_gui.TOTAL_WORKERS = int(self.total_workers.get())
		main_gui.TOTAL_BSC = int(self.total_bscs.get())
		main_gui.TOTAL_INCUBATORS = int(self.total_incubators.get())
		main_gui.TOTAL_BIOREACTORS = int(self.total_bioreact.get())
		#print('Facility commands saved!')
		#print(AREA_FACILITY)
	
	def clear_facility(self):

		#Method where all values added from facility frame will be cleared

		self.total_area.delete(0,'end')
		self.area_unit.set(1)
		self.total_workers.delete(0,'end')
		self.total_bscs.delete(0,'end')
		self.total_incubators.delete(0,'end')
		self.total_bioreact.delete(0,'end')

class CulturePanel:

	def __init__(self,main_notebook,main_gui):

		self.frame = ttk.Frame(main_notebook)
		main_notebook.add(self.frame,text="Culture conditions")

		#Create the label to select the type of ET
		ttk.Label(self.frame,text="Type of expansion technology:").grid(row=0,column=0,columnspan=2)
		self.type_et = StringVar()
		self.type_et.set('planar')
		self.planar = ttk.Radiobutton(self.frame,text="Planar",variable=self.type_et,value='planar',command = lambda: self.block_et_type())
		self.planar.grid(row=1,column=0)
		self.mc = ttk.Radiobutton(self.frame,text="Microcarrier",variable=self.type_et,value='microcarrier',command = lambda: self.block_et_type())
		self.mc.grid(row=1,column=1)
		self.planar.config(state=DISABLED)
		self.mc.config(state=DISABLED)
		#print(type(self.type_et))
		#print(type(self.type_et.get()))
		#Type of microcarriers when applicable

		ttk.Label(self.frame,text="Type of microcarrier:").grid(row=0,column=2,columnspan=2)
		self.type_mc = StringVar()
		self.type_mc.set('cultispher')
		self.type_mc_1 = ttk.Radiobutton(self.frame,text="Cultispher G",variable=self.type_mc,value='cultispher',state=DISABLED)
		self.type_mc_1.grid(row=1,column=2)
		self.type_mc_2 = ttk.Radiobutton(self.frame,text="Cytodex 1",variable=self.type_mc,value='cytodex1',state=DISABLED)
		self.type_mc_2.grid(row=2,column=2)
		self.type_mc_3 = ttk.Radiobutton(self.frame,text="Cytodex 3",variable=self.type_mc,value='cytodex3',state=DISABLED)
		self.type_mc_3.grid(row=3,column=2)
		self.type_mc_4 = ttk.Radiobutton(self.frame,text="SoloHill Plastic",variable=self.type_mc,value='solohill',state=DISABLED)
		self.type_mc_4.grid(row=1,column=3)
		self.type_mc_5 = ttk.Radiobutton(self.frame,text="CellBIND",variable=self.type_mc,value='cellbind',state=DISABLED)
		self.type_mc_5.grid(row=2,column=3)
		self.type_mc_6 = ttk.Radiobutton(self.frame,text="Synthemax II",variable=self.type_mc,value='synthemax2',state=DISABLED)
		self.type_mc_6.grid(row=3,column=3)

		#Add type of MSCs
		ttk.Label(self.frame,text="MSC source:").grid(row=4,column=0,columnspan=2)
		self.source_msc = StringVar()
		self.source_msc.set('bm')
		self.asc_button = ttk.Radiobutton(self.frame,text="Adipose tissue",variable=self.source_msc,value='asc')
		self.asc_button.grid(row=5,column=0)
		self.asc_button.config(state=DISABLED)
		self.bm_button = ttk.Radiobutton(self.frame,text="Bone marrow",variable=self.source_msc,value='bm')
		self.bm_button.grid(row=6,column=0)
		self.bm_button.config(state=DISABLED)
		self.ucm_button = ttk.Radiobutton(self.frame,text="Umbilical cord matrix",variable=self.source_msc,value='ucm')
		self.ucm_button.grid(row=7,column=0)
		self.ucm_button.config(state=DISABLED)

		#Add type of culture medium
		ttk.Label(self.frame,text="Culture medium:").grid(row=4,column=2,columnspan=2)
		self.type_media = StringVar()
		self.type_media.set('fbs')
		self.fbs_button = ttk.Radiobutton(self.frame,text="DMEM + 10% FBS",variable=self.type_media,value='fbs')
		self.fbs_button.grid(row=5,column=2)
		self.hpl_button = ttk.Radiobutton(self.frame,text="DMEM + 5% hPL",variable=self.type_media,value='hpl')
		self.hpl_button.grid(row=6,column=2)
		self.stempro_button = ttk.Radiobutton(self.frame,text="StemPro SFM XF",variable=self.type_media,value='stempro')
		self.stempro_button.grid(row=7,column=2)
		self.fbs_button.config(state=DISABLED)
		self.hpl_button.config(state=DISABLED)
		self.stempro_button.config(state=DISABLED)
		#Add the buttons

		main_gui.TYPE_OF_ET = self.type_et.get()
		#print(self.type_et.get())
		#global TYPE_OF_MC
		main_gui.TYPE_OF_MC = self.type_mc.get()
		#print(self.type_mc.get())
		#global SOURCE_OF_MSC
		main_gui.SOURCE_OF_MSC = self.source_msc.get()
		#global TYPE_OF_MEDIA
		main_gui.TYPE_OF_MEDIA = self.type_media.get()

		ttk.Button(self.frame,text="Save",command = lambda: self.save_culture(main_gui)).grid(row=8,column=1,pady = 5,padx=5,sticky="e")
		ttk.Button(self.frame,text="Clear",command = lambda: self.clear_culture()).grid(row=8,column=2,pady = 5,padx=5,sticky="w")

		#print(self.type_et.get())

	def save_culture(self,main_gui):

		#Method where all the values from culture frame will be saved
		#global TYPE_OF_ET
		main_gui.TYPE_OF_ET = self.type_et.get()
		#print(self.type_et.get())
		#global TYPE_OF_MC
		main_gui.TYPE_OF_MC = self.type_mc.get()
		#print(self.type_mc.get())
		#global SOURCE_OF_MSC
		main_gui.SOURCE_OF_MSC = self.source_msc.get()
		#global TYPE_OF_MEDIA
		main_gui.TYPE_OF_MEDIA = self.type_media.get()
		#print('Saved culture commands!')

	def clear_culture(self):

		#Method where all values added from culture frame will be cleared
		self.type_et.set('planar')
		self.type_mc.set('cultispher')
		#Blocks the et type
		self.block_et_type()
		self.source_msc.set('asc')
		self.type_media.set('fbs')
		#print('Cleared commands')

	def block_et_type(self):

		#Blocks unnecessary inputs according to the type of expansion tech

		if self.type_et.get() == 'planar':

			#It is planar, so can disable the suspension based outputs
			self.type_mc_1.config(state=DISABLED)
			self.type_mc_2.config(state=DISABLED)
			self.type_mc_3.config(state=DISABLED)
			self.type_mc_4.config(state=DISABLED)
			self.type_mc_5.config(state=DISABLED)
			self.type_mc_6.config(state=DISABLED)
			#ManualPanel.sd_suspension.config(state=DISABLED)

		elif self.type_et.get() == 'microcarrier':

			#Enable these variables
			self.type_mc_1.config(state=ACTIVE)
			self.type_mc_2.config(state=ACTIVE)
			self.type_mc_3.config(state=ACTIVE)
			self.type_mc_4.config(state=ACTIVE)
			self.type_mc_5.config(state=ACTIVE)
			self.type_mc_6.config(state=ACTIVE)
			#ManualPanel.sd_suspension.config(state=ACTIVE)

class GrowthPanel:

	def __init__(self,main_notebook,main_gui):

		self.frame = ttk.Frame(main_notebook)
		main_notebook.add(self.frame,text="Growth characteristics")

		#add the labels for cells/donor and max CPDs
		ttk.Label(self.frame,text="Average P0 million cells/donor:").grid(row=0,column=0)
		self.cells_donor = ttk.Entry(self.frame,width=15)
		self.cells_donor.insert(END,1)
		self.cells_donor.grid(row=1,column=0)
		self.cells_donor.config(state=DISABLED)

		ttk.Label(self.frame,text="SD P0 million cells/donor:").grid(row=0,column=1)
		self.cells_donor_sd = ttk.Entry(self.frame,width=15)
		self.cells_donor_sd.insert(END,0)
		self.cells_donor_sd.grid(row=1,column=1)
		self.cells_donor_sd.config(state=DISABLED)

		ttk.Label(self.frame,text="Maximum number CPDs").grid(row=0,column=2)
		self.max_cpds = ttk.Entry(self.frame,width=15)
		self.max_cpds.insert(END,20)
		self.max_cpds.grid(row=1,column=2)
		self.max_cpds.config(state=DISABLED)

		#Add the radiobuttons for the maximum number of passages
		ttk.Label(self.frame,text="Maximum number of passages:").grid(row=2,column=0)
		self.max_pass = IntVar()
		self.max_pass.set(3)

		self.p1_button = ttk.Radiobutton(self.frame,text="1",variable=self.max_pass,value=1,command = lambda: self.block_passage_choice())
		self.p1_button.grid(row=3,column=0)
		self.p1_button.config(state=DISABLED)

		self.p2_button = ttk.Radiobutton(self.frame,text="2",variable=self.max_pass,value=2,command = lambda: self.block_passage_choice())
		self.p2_button.grid(row=4,column=0)
		self.p2_button.config(state=DISABLED)	
		
		self.p3_button = ttk.Radiobutton(self.frame,text="3",variable=self.max_pass,value=3,command = lambda: self.block_passage_choice())
		self.p3_button.grid(row=5,column=0)
		self.p3_button.config(state=DISABLED)		

		self.p4_button = ttk.Radiobutton(self.frame,text="4",variable=self.max_pass,value=4,command = lambda: self.block_passage_choice())
		self.p4_button.grid(row=6,column=0)
		self.p4_button.config(state=DISABLED)

		self.p5_button = ttk.Radiobutton(self.frame,text="5",variable=self.max_pass,value=5,command = lambda: self.block_passage_choice())
		self.p5_button.grid(row=7,column=0)
		self.p5_button.config(state=DISABLED)

		#Add the entry fields of growth rates per passage
		ttk.Label(self.frame,text="Growth rate/day per passage:").grid(row=2,column=1,columnspan=2)
		ttk.Label(self.frame,text="P1").grid(row=3,column=1)
		
		self.gr_p1 = ttk.Entry(self.frame,width=15)
		self.gr_p1.grid(row=3,column=2)
		self.gr_p1.insert(END,0.21)
		self.gr_p1.config(state=DISABLED)

		ttk.Label(self.frame,text="P2").grid(row=4,column=1)
		self.gr_p2 = ttk.Entry(self.frame,width=15)
		self.gr_p2.grid(row=4,column=2)
		self.gr_p2.insert(END,0.20)

		ttk.Label(self.frame,text="P3").grid(row=5,column=1)
		self.gr_p3 = ttk.Entry(self.frame,width=15)
		self.gr_p3.grid(row=5,column=2)
		self.gr_p3.insert(END,0.18)

		ttk.Label(self.frame,text="P4").grid(row=6,column=1)
		self.gr_p4 = ttk.Entry(self.frame,width=15)
		self.gr_p4.grid(row=6,column=2)

		ttk.Label(self.frame,text="P5").grid(row=7,column=1)
		self.gr_p5 = ttk.Entry(self.frame,width=15)
		self.gr_p5.grid(row=7,column=2)

		#Begin by putting the commands from P2 to P5 disabled since the initial state is P1

		self.gr_p2.state(['disabled'])
		self.gr_p3.state(['disabled'])
		self.gr_p4.state(['disabled'])
		self.gr_p5.state(['disabled'])

		main_gui.INITIAL_CELLS_PER_DONOR_AVG = round(float(self.cells_donor.get()),3)*1e6

		main_gui.INITIAL_CELLS_PER_DONOR_SD = round(float(self.cells_donor_sd.get()),3)*1e6

		main_gui.MAXIMUM_NUMBER_CPD = round(float(self.max_cpds.get()),2)

		main_gui.MAX_NO_PASSAGES = self.max_pass.get()

		main_gui.GR_P1 = round(float(self.gr_p1.get()),2)
		main_gui.GR_P2 = round(float(self.gr_p2.get()),2)
		main_gui.GR_P3 = round(float(self.gr_p3.get()),2)
		main_gui.GR_P4 = 0
		main_gui.GR_P5 = 0

		#Add the buttons

		ttk.Button(self.frame,text="Save",command = lambda: self.save_growth(main_gui)).grid(row=8,column=0,pady = 5,padx=5,sticky="e")
		ttk.Button(self.frame,text="Clear",command = lambda: self.clear_growth()).grid(row=8,column=1,pady = 5,padx=5,sticky="w")

	def block_passage_choice(self):

		#Method that will block certain passage parameters given the radiobutton

		if self.max_pass.get() == 1:

			self.gr_p2.state(['disabled'])
			self.gr_p3.state(['disabled'])
			self.gr_p4.state(['disabled'])
			self.gr_p5.state(['disabled'])
		
		elif self.max_pass.get() == 2:
		
			self.gr_p2.state(['!disabled'])
			self.gr_p3.state(['disabled'])
			self.gr_p4.state(['disabled'])
			self.gr_p5.state(['disabled'])

		elif self.max_pass.get() == 3:
		
			self.gr_p2.state(['!disabled'])
			self.gr_p3.state(['!disabled'])
			self.gr_p4.state(['disabled'])
			self.gr_p5.state(['disabled'])

		elif self.max_pass.get() == 4:
		
			self.gr_p2.state(['!disabled'])
			self.gr_p3.state(['!disabled'])
			self.gr_p4.state(['!disabled'])
			self.gr_p5.state(['disabled'])

		elif self.max_pass.get() == 5:
		
			self.gr_p2.state(['!disabled'])
			self.gr_p3.state(['!disabled'])
			self.gr_p4.state(['!disabled'])
			self.gr_p5.state(['!disabled'])
		else:
			pass

	def save_growth(self,main_gui):

		#Method where all the values from growth frame will be saved

		main_gui.INITIAL_CELLS_PER_DONOR_AVG = round(float(self.cells_donor.get()),3)*1e6

		main_gui.INITIAL_CELLS_PER_DONOR_SD = round(float(self.cells_donor_sd.get()),3)*1e6

		main_gui.MAXIMUM_NUMBER_CPD = round(float(self.max_cpds.get()),2)

		main_gui.MAX_NO_PASSAGES = self.max_pass.get()

		main_gui.GR_P1 = round(float(self.gr_p1.get()),2)
		main_gui.GR_P2 = 0
		main_gui.GR_P3 = 0
		main_gui.GR_P4 = 0
		main_gui.GR_P5 = 0

		if 'disabled' not in self.gr_p2.state():
			main_gui.GR_P2 = round(float(self.gr_p2.get()),2)
		if 'disabled' not in self.gr_p3.state():
			main_gui.GR_P3 = round(float(self.gr_p3.get()),2)
		if 'disabled' not in self.gr_p4.state():
			main_gui.GR_P4 = round(float(self.gr_p4.get()),2)
		if 'disabled' not in self.gr_p5.state():
			main_gui.GR_P5 = round(float(self.gr_p5.get()),2)
		#Add the passage values later due to the blocking of certain values
		#Needs an additional function, maybe block all values to zero?
		print('Saved all the growth variables!')

	def clear_growth(self):

		#Method where all the values from growth frame will be deleted or reset
		self.cells_donor.delete(0,'end')
		self.max_cpds.delete(0,'end')
		self.max_pass.set(1)
		self.gr_p1.delete(0,'end')
		self.gr_p2.delete(0,'end')
		self.gr_p3.delete(0,'end')
		self.gr_p4.delete(0,'end')
		self.gr_p5.delete(0,'end')
		#Block the passage to return to initial config
		self.block_passage_choice()
		#Needs to check what to do with the passage numbers
		#print('Cleared all the growth variables!')

class ManualPanel:

	def __init__(self,main_notebook,culture_panel,main_gui):

		self.frame5 = ttk.Frame(main_notebook)
		main_notebook.add(self.frame5,text="Manual operations")

		#Create a paned window

		self.panedwindow = ttk.Panedwindow(self.frame5, orient = VERTICAL)
		self.panedwindow.pack(fill = BOTH, expand = True)

		#Create three subframes

		self.frame5_1 = ttk.Frame(self.panedwindow)
		self.frame5_2 = ttk.Frame(self.panedwindow)
		self.frame5_3 = ttk.Frame(self.panedwindow)
		self.frame5_4 = ttk.Frame(self.panedwindow)

		self.panedwindow.add(self.frame5_1, weight = 1)
		self.panedwindow.add(self.frame5_2, weight = 1)
		self.panedwindow.add(self.frame5_3, weight = 1)
		self.panedwindow.add(self.frame5_4, weight = 1)

		#Create the labels for the seeding pane

		ttk.Label(self.frame5_1,text="Planar seeding density (cells/cm^2):").grid(row=0,column=0)
		self.sd_planar = ttk.Entry(self.frame5_1,width=15)
		self.sd_planar.insert(END,3000)
		self.sd_planar.config(state=DISABLED)
		self.sd_planar.grid(row=1,column=0)

		ttk.Label(self.frame5_1,text="Suspension seeding density (cells/ml):").grid(row=2,column=0)
		self.sd_suspension = ttk.Entry(self.frame5_1,width=15)
		self.sd_suspension.grid(row=3,column=0)
		self.sd_suspension.config(state=DISABLED)

		ttk.Label(self.frame5_1,text="Working volume ratio for suspension:").grid(row=0,column=1)
		self.workvolratio = ttk.Entry(self.frame5_1,width=15)
		self.workvolratio.grid(row=1,column=1)
		self.workvolratio.config(state=DISABLED)

		ttk.Label(self.frame5_1,text="Microcarrier adhesion ratio:").grid(row=2,column=1)
		self.mc_adh_ratio = ttk.Entry(self.frame5_1,width=15)
		self.mc_adh_ratio.grid(row=3,column=1)
		self.mc_adh_ratio.config(state=DISABLED)

		ttk.Label(self.frame5_1,text="Microcarrier concentration:").grid(row=4,column=1)
		self.mc_conc = ttk.Entry(self.frame5_1,width=15)
		self.mc_conc.grid(row=5,column=1)
		self.mc_conc.config(state=DISABLED)

		#Create labels and entries for feeding pane

		ttk.Label(self.frame5_2,text="Feeding period planar (days):").grid(row=0,column=0)
		self.fp_planar = ttk.Entry(self.frame5_2,width=15)
		self.fp_planar.insert(END,3)
		self.fp_planar.grid(row=1,column=0)
		self.fp_planar.config(state=DISABLED)

		ttk.Label(self.frame5_2,text="Feeding period suspension (days):").grid(row=2,column=0)
		self.fp_suspension = ttk.Entry(self.frame5_2,width=15)
		self.fp_suspension.grid(row=3,column=0)
		self.fp_suspension.config(state=DISABLED)

		ttk.Label(self.frame5_2,text="Fraction of working volume replaced (planar):").grid(row=0,column=1)
		self.wv_planar = ttk.Entry(self.frame5_2,width=15)
		self.wv_planar.insert(END,1)
		self.wv_planar.grid(row=1,column=1)
		self.wv_planar.config(state=DISABLED)

		ttk.Label(self.frame5_2,text="Fraction of working volume replaced (suspension):").grid(row=2,column=1)
		self.wv_suspension = ttk.Entry(self.frame5_2,width=15)
		self.wv_suspension.grid(row=3,column=1)
		self.wv_suspension.config(state=DISABLED)

		#Create labels and entries for harvesting pane

		ttk.Label(self.frame5_3,text="Planar harvesting density (cells/cm^2):").grid(row=0,column=0)
		self.hd_planar = ttk.Entry(self.frame5_3,width=15)
		self.hd_planar.insert(END,25000)
		self.hd_planar.grid(row=1,column=0)
		self.hd_planar.config(state=DISABLED)

		ttk.Label(self.frame5_3,text="Suspension harvesting density (cells/ml):").grid(row=2,column=0)
		self.hd_suspension = ttk.Entry(self.frame5_3,width=15)
		self.hd_suspension.grid(row=3,column=0)
		self.hd_suspension.config(state=DISABLED)

		ttk.Label(self.frame5_3,text="Harvesting efficiency (planar):").grid(row=0,column=1)
		self.heff_planar = ttk.Entry(self.frame5_3,width=15)
		self.heff_planar.insert(END,1)
		self.heff_planar.grid(row=1,column=1)
		self.heff_planar.config(state=DISABLED)

		ttk.Label(self.frame5_3,text="Harvesting efficiency (suspension):").grid(row=2,column=1)
		self.heff_suspension = ttk.Entry(self.frame5_3,width=15)
		self.heff_suspension.grid(row=3,column=1)
		self.heff_suspension.config(state=DISABLED)

		main_gui.SD_PLANAR = round(float(self.sd_planar.get()),2)

		#global FEEDING_VARS
		main_gui.FP_PLANAR = round(float(self.fp_planar.get()),2)
		main_gui.WV_PLANAR = round(float(self.wv_planar.get()),2)

		main_gui.HD_PLANAR = round(float(self.hd_planar.get()),2)
		main_gui.HEFF_PLANAR = round(float(self.heff_planar.get()),2)

		main_gui.SD_SUSPENSION = 0
		main_gui.MC_ADH_RATIO = 0
		main_gui.MC_CONC = 0
		main_gui.WORKING_VOLUME_RATIO = 0

		main_gui.FP_SUSPENSION = 0
		main_gui.WV_SUSPENSION = 0

		main_gui.HD_SUSPENSION = 0
		main_gui.HEFF_SUSPENSION = 0

		#Set these variables as disabled per default due to the planar default

		# self.sd_suspension.state(['disabled'])
		# self.workvolratio.state(['disabled'])
		# self.mc_adh_ratio.state(['disabled'])
		# self.mc_conc.state(['disabled'])
		# self.fp_suspension.state(['disabled'])
		# self.wv_suspension.state(['disabled'])
		# self.hd_suspension.state(['disabled'])
		# self.heff_suspension.state(['disabled'])

		# if culture_panel.type_et.get() == 'planar':

		# 	self.sd_suspension.state(['disabled'])
		# 	self.workvolratio.state(['disabled'])
		# 	self.mc_adh_ratio.state(['disabled'])
		# 	self.mc_conc.state(['disabled'])
		# 	self.fp_suspension.state(['disabled'])
		# 	self.wv_suspension.state(['disabled'])
		# 	self.hd_suspension.state(['disabled'])
		# 	self.heff_suspension.state(['disabled'])

		# elif culture_panel.type_et.get() == 'microcarrier':

		# 	self.sd_suspension.state(['!disabled'])
		# 	self.workvolratio.state(['!disabled'])
		# 	self.mc_adh_ratio.state(['!disabled'])
		# 	self.mc_conc.state(['!disabled'])
		# 	self.fp_suspension.state(['!disabled'])
		# 	self.wv_suspension.state(['!disabled'])
		# 	self.hd_suspension.state(['!disabled'])
		# 	self.heff_suspension.state(['!disabled'])			

		#Create buttons

		#Add the buttons

		ttk.Button(self.frame5_4,text="Save", command = lambda: self.save_manual(culture_panel,main_gui)).grid(row=0,column=0,pady = 5,padx=5,sticky="e")
		ttk.Button(self.frame5_4,text="Clear",command = lambda: self.clear_manual()).grid(row=0,column=1,pady = 5,padx=5,sticky="w")

	def save_manual(self,culture_panel,main_gui):

		#Method to save all values form manual frame
		#global SEEDING_VARS

		main_gui.SD_PLANAR = round(float(self.sd_planar.get()),2)

		#global FEEDING_VARS
		main_gui.FP_PLANAR = round(float(self.fp_planar.get()),2)
		main_gui.WV_PLANAR = round(float(self.wv_planar.get()),2)

		main_gui.HD_PLANAR = round(float(self.hd_planar.get()),2)
		main_gui.HEFF_PLANAR = round(float(self.heff_planar.get()),2)

		main_gui.SD_SUSPENSION = 0
		main_gui.MC_ADH_RATIO = 0
		main_gui.MC_CONC = 0
		main_gui.WORKING_VOLUME_RATIO = 0

		main_gui.FP_SUSPENSION = 0
		main_gui.WV_SUSPENSION = 0

		main_gui.HD_SUSPENSION = 0
		main_gui.HEFF_SUSPENSION = 0

		if culture_panel.type_et.get() == 'microcarrier':
			main_gui.SD_SUSPENSION = round(float(self.sd_suspension.get()),2)
			main_gui.MC_ADH_RATIO = round(float(self.mc_adh_ratio.get()),2)
			main_gui.MC_CONC = round(float(self.mc_conc.get()),2)
			main_gui.WORKING_VOLUME_RATIO = round(float(self.workvolratio.get()),2)

			main_gui.FP_SUSPENSION = round(float(self.fp_suspension.get()),2)
			main_gui.WV_SUSPENSION = round(float(self.wv_suspension.get()),2)

			main_gui.HD_SUSPENSION = round(float(self.hd_suspension.get()),2)
			main_gui.HEFF_SUSPENSION = round(float(self.heff_suspension.get()),2)

		print('Saved manual operation commands!')

	def clear_manual(self):

		self.sd_planar.delete(0,'end')
		self.sd_suspension.delete(0,'end')
		self.workvolratio.delete(0,'end')
		self.mc_adh_ratio.delete(0,'end')
		self.mc_conc.delete(0,'end')
		self.fp_planar.delete(0,'end')
		self.fp_suspension.delete(0,'end')
		self.wv_planar.delete(0,'end')
		self.wv_suspension.delete(0,'end')
		self.hd_planar.delete(0,'end')
		self.hd_suspension.delete(0,'end')
		self.heff_planar.delete(0,'end')
		self.heff_suspension.delete(0,'end')

class DemandPanel:

	def __init__(self,main_notebook,main_gui):

		self.frame7 = ttk.Frame(main_notebook)
		main_notebook.add(self.frame7,text="Manufacturing demand")

		#Create the labels

		ttk.Label(self.frame7,text="Million cells/dose:").grid(row=0,column=0)
		self.cells_dose = ttk.Entry(self.frame7,width=15)
		self.cells_dose.grid(row=1,column=0)
		self.cells_dose.insert(END,75)
		self.cells_dose.config(state=DISABLED)

		ttk.Label(self.frame7,text="Number of doses/year:").grid(row=0,column=1)
		self.doses_year = ttk.Entry(self.frame7,width=15)
		self.doses_year.grid(row=1,column=1)
		self.doses_year.insert(END,1)
		self.doses_year.config(state=DISABLED)

		ttk.Label(self.frame7,text="Number of doses/lot:").grid(row=0,column=2)
		self.doses_lot = ttk.Entry(self.frame7,width=15)
		self.doses_lot.grid(row=1,column=2)
		self.doses_lot.insert(END,1)
		self.doses_lot.config(state=DISABLED)

				#global CELL_NUMBER_PER_DOSE
		main_gui.CELL_NUMBER_PER_DOSE = round(float(self.cells_dose.get()),2)*1e6

		#global ANNUAL_DEMAND
		main_gui.ANNUAL_DEMAND = int(self.doses_year.get())

		#global LOT_SIZE
		main_gui.LOT_SIZE = int(self.doses_lot.get())

		#Add buttons

		ttk.Button(self.frame7,text="Save",command = lambda: self.save_demand(main_gui)).grid(row=2,column=0,pady = 5,padx=5,sticky="e")
		ttk.Button(self.frame7,text="Clear",command = lambda: self.clear_demand()).grid(row=2,column=1,pady = 5,padx=5,sticky="w")


	def save_demand(self,main_gui):

		#Save all variables from demand frame

		#global CELL_NUMBER_PER_DOSE
		main_gui.CELL_NUMBER_PER_DOSE = round(float(self.cells_dose.get()),2)*1e6

		#global ANNUAL_DEMAND
		main_gui.ANNUAL_DEMAND = int(self.doses_year.get())

		#global LOT_SIZE
		main_gui.LOT_SIZE = int(self.doses_lot.get())

		print('Saved demand commands!')

	def clear_demand(self):

		#Clear all variables from demand frame
		self.cells_dose.delete(0,'end')
		self.doses_year.delete(0,'end')
		self.doses_lot.delete(0,'end')

# class SimulationTypePanel:

# 	def __init__(self,main_notebook):

# 		self.frame = ttk.Frame(main_notebook)
# 		main_notebook.add(self.frame,text = "Simulation type")

# class CostPanel:

# 	def __init__(self,main_notebook):

# class SimulationData(MainGui):

# 	#A class that will collect all data from the GUI

# 	def __init__(self,master):

# 		MainGui.__init__(self,master)

# 		self.AREA_FACILITY = 50

# 		#print(self.AREA_FACILITY)


def main():            
    
    root = Tk()
    #Avoid the menu to tear down
    root.option_add('*tearOff', False)

    msc_gui = MainGui(root)
    #sim_data = SimulationData(root)
#    print(msc_gui.LIST_OF_MAX_GROWTH_RATES)
#    print(MainGui.LIST_OF_MAX_GROWTH_RATES)

    root.mainloop()
    
if __name__ == "__main__": main()