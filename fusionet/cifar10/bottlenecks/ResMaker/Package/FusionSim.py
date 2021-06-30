import yaml
import random
from ResMaker.Package.Actions import *
from ResMaker.Package.HardwareComponents import *
import sys
from functools import reduce


#*********************************************************************
#Setup & Configuration ***********************************************
VERSION = 0.2
TOTAL_PE = 64
PE_COMPONENTS = ['.prediction_buffer', '.adders', '.bit_masks_and', '.mux_', '.mux']
ACC_NAME = 'fusion_chip.'

global chip
#*********************************************************************
#initialize all the hardware component objects from their classes*****
def init():
    global chip
    global TOTAL_PE
    #Initializing the Chip
    chip = Chip(name=ACC_NAME, total_PE=TOTAL_PE, PE_components=PE_COMPONENTS)


#*********************************************************************
#Simulate network by getting action count of each component **********
def simulate_network(layer, cycles, outer_M, PE_adders):
    global chip
    chip.process(layer, cycles, outer_M, PE_adders)


#*********************************************************************
#dumps a dictionary into a yaml file *********************************
def write_yaml(dict, file_name):
    with open(file_name, 'w') as file:
        yaml.dump(dict, file)
#get action counts from all components into a dictionary
def create_yaml(file):
    global chip

    #append all the dictionaries from all component to a list
    dicts = []

    dicts += [chip.prediction_glb.get_dict()]
    dicts += [chip.global_AND_gate.get_dict()]
    for PE in chip.PEs:
        dicts += PE.get_dict()

    final_dict = {'action_counts': {'version': VERSION, 'local':dicts}}
    write_yaml(final_dict, file)


def create_action_counts(in_ch, midd_ch, out_ch, pixels, stride, prune_factor, cycles, outer_M, file, PE_adders, total_PEs):
    global TOTAL_PE
    TOTAL_PE = total_PEs
    layer = {"in_ch":in_ch, "midd_ch":midd_ch, "out_ch":out_ch,
             "pixels":pixels, "stride":stride,
             "prune_factor":prune_factor}
    init()
    simulate_network(layer, cycles, outer_M, PE_adders);
    create_yaml(file)
