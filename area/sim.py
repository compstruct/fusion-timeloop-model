import numpy as np
import sys
import pandas
import subprocess
import time
import yaml
import csv

#*****Configurations********

#baseline acc. config
BL_PEs = 72
F_PEs = 64
F_PE_ADDERS = 6

FUSION_AREA = 0.0
fusion_PE = {}
fusion_global = {}

BASELINE_AREA = 0.0
baseline_PE = {}
baseline_global = {}

def sim_fusion_area(DIR, F_DIR):
    p = subprocess.Popen(['accelergy', F_DIR+"/main", "-o", DIR+"fusion_main_output"],\
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()
    p = subprocess.Popen(['accelergy', F_DIR+"/overhead", "-o", DIR+"fusion_overhead_output"],\
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()

def read_fusion_area(DIR):
    with open(DIR + "ART.yaml") as file:
        fusion_main = yaml.safe_load(file)
    for element in fusion_main['ART']['tables']:
        if "DummyBuffer" not in element['name'] and  "DRAM" not in element['name']:
            component = element['name'].split('.')[-1]
            if "PE" in element['name']:
                fusion_PE[component] = element['area']
            else:
                fusion_global[component] = element['area']


def fusion_area(DIR, F_DIR):

    global FUSION_AREA, F_PE_ADDERS

    sim_fusion_area(DIR, F_DIR)

    read_fusion_area(DIR+"fusion_main_output/")
    read_fusion_area(DIR+"fusion_overhead_output/")

    for key in fusion_global:
        if key == 'binary_decoder':
            fusion_global[key] *= 8*(F_PE_ADDERS*4)
        if  key != 'pred_glb':
            FUSION_AREA += fusion_global[key]

    for key in fusion_PE:
        if key == 'bit_masks_and':
            fusion_PE[key] *= (F_PE_ADDERS*4)*2

        if key == 'mux':  #reconfigurable adders mux
            fusion_PE[key] *= (F_PE_ADDERS*4)
        elif key == 'mux_':   #zero replacing mux
            fusion_PE[key] *= F_PE_ADDERS
        elif key == 'adders':
            fusion_PE[key] *= F_PE_ADDERS  #F_PE_ADDERS
        elif key == 'adder_fifo':
            fusion_PE[key] *= F_PE_ADDERS

        FUSION_AREA += fusion_PE[key]*F_PEs




def sim_baseline_area(DIR, BL_DIR):
    p = subprocess.Popen(['accelergy', BL_DIR, "-o", DIR+"baseline_output"],\
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()


def read_baseline_area(DIR):
    with open(DIR + "ART.yaml") as file:
        baseline_area = yaml.safe_load(file)
    for element in baseline_area['ART']['tables']:
        if "DummyBuffer" not in element['name'] and  "DRAM" not in element['name']:
            component = element['name'].split('.')[-1]
            if "PE" in element['name']:
                baseline_PE[component] = element['area']
            else:
                baseline_global[component] = element['area']




def baseline_area(DIR, BL_DIR):

    global BASELINE_AREA

    sim_baseline_area(DIR, BL_DIR)
    read_baseline_area(DIR+"baseline_output/")

    for key in baseline_global:
        BASELINE_AREA += baseline_global[key]

    for key in baseline_PE:
        if key == 'decoding':
            baseline_PE[key] *= 4
        BASELINE_AREA += baseline_PE[key]*BL_PEs



def area_sim():

    global FUSION_AREA
    global BASELINE_AREA

    DIR = "./area/"
    BL_DIR = "./../accelerator/baseline/"
    F_DIR = "./../accelerator/fusion/"

    fusion_area(DIR, F_DIR)
    baseline_area(DIR, BL_DIR)

    print("baseline area is: " ,BASELINE_AREA)
    print("fusion area is: ", FUSION_AREA)
    #print(FUSION_AREA/BASELINE_AREA)



def write_results(DIR):

    global BASELINE_AREA
    global FUSION_AREA

    with open(DIR + 'baseline_area.csv', 'w') as f:
        for key in baseline_global.keys():
            f.write("%s,%.2f\n"%(key,baseline_global[key]))
        for key in baseline_PE.keys():
            f.write("%s,%.2f\n"%(key,baseline_PE[key]))
        f.write("%s,%.2f\n"%('total',BASELINE_AREA))

    with open(DIR + 'fusion_area.csv', 'w') as f:
        for key in fusion_global.keys():
            f.write("%s,%.2f\n"%(key, fusion_global[key]))
        for key in fusion_PE.keys():
            f.write("%s,%.2f\n"%(key, fusion_PE[key]))
        f.write("%s,%.2f\n"%('total',FUSION_AREA))

print("beginning area simulations")
area_sim()
write_results("./area/")
print("total area ratio is ", FUSION_AREA/BASELINE_AREA)
#for key in fusion_global.keys():
#  print(key)
#for key in fusion_PE.keys():
#  print(key)
