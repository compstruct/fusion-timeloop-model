import numpy as np
import sys
import pandas
import csv

debug_DRAM_frac = False
PE = 72
DRAM_access_e = 512/4
GLB_access_e = 75.22/4
SPAD_access_e = 4.37
ADD_e = 0.054
MAC_e = 2.2
COMPARATOR_e = 0.015



in_ch = []
out_ch = []

strides = []
pixels = []



def fix_pooling(file, layer, block):
    global in_ch, out_ch, pixels, stride

    with open(file) as f:
       txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')

    e = float(txt[ind+4].split()[1])
    c = int(txt[ind+3].split()[1])

    DRAM_section = txt[txt.index('Level 4'):txt.index('Networks')]
    DRAM_ifmaps_e = float(DRAM_section[DRAM_section.index('Inputs:')+12].split()[3])
    e += DRAM_ifmaps_e*1e-6*(out_ch[block]-1)

    mac_section = txt[txt.index('Level 0'):txt.index('Level 1')]
    mac_e = float(mac_section[14].split()[3])

    if layer == "ave_pool":
        e = e + (-1.00 * mac_e + mac_e * 1/8 + MAC_e/2.2 * ADD_e) * 1e-6
    else:
        e = e + (-1.00 * mac_e + mac_e/MAC_e * COMPARATOR_e) * 1e-6

    return e, c



def get_layer_stats(file, layer=""):

    with open(file) as f:
        txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')

    e = float(txt[ind+4].split()[1])
    c = int(txt[ind+3].split()[1])
    if layer == "gpw":
        e *= 4
        c *= 4

    return e, c



def make_csv(blocks, DIR, in_channels, out_channels, pixs, stride, model_desc, name):

    global out_ch, pixels, model_description, in_ch, strides

    names = name
    total_e = []
    total_c = []
    out_ch = out_channels
    pixels = pixs
    in_ch = in_channels
    strides = stride
    model_description = model_desc

    for block, layer in enumerate(model_description):

        if (layer == "max_pool" or layer == "ave_pool"):
            e, c = fix_pooling(DIR + names[block] +"/output/timeloop-mapper.stats.txt", layer, block)
        else:
            e, c = get_layer_stats(DIR + names[block] +"/output/timeloop-mapper.stats.txt")
        total_e.append(e)
        total_c.append(c)

    df = pandas.DataFrame(data={"1_block":names, "2_energy":total_e, "3_cycles":total_c})

    df.to_csv("results/bl.csv", sep=',',index=False)
