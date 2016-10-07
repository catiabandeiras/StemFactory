# -*- coding: utf-8 -*-

#
# A Comprehensive list of events to handle:
#   profit - nice doing! You were able to profif in this exercise
#   loss - not this time! - Doing this will result in a loss.
#   Max_Passages_reached - ??
#   Max_CPD_reached - Not enough cells grown
#
#
#
class SimulationEvent(object):

    def __init__(self, simTime, eventName):
        self.simTime   = simTime
        self.eventName = eventName
