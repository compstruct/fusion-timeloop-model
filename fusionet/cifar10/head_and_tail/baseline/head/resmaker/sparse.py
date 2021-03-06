import numpy as np
import math
import sys
import pandas
import csv

debug_DRAM_frac = False
PE = 256

POINTER_BITS = 32
DRAM_access_e = 512/4
GLB_access_e = 75.22/4
SPAD_access_e = 4.37
int_add_e = 0.054
COMPARATOR_e = 0.015

stats = [ [] for _ in range(8)]

in_ch = []
midd_ch = []
out_ch = []

stride = []
pixels = []

w_sparsity = []
g_sparsity = []
a_sparsity = []

DRAM_perc = []

#Break down for weights
dense_DRAM_e = []
dense_glb_e = []
dense_spad_e = []
dense_mac_e = []

sparse_DRAM_e = []
sparse_glb_e = []
sparse_spad_e = []
sparse_mac_e = []

DRAM_weights_saved_e = []
glb_weights_saved_e = []
spad_weights_saved_e = []

DRAM_activations_saved_e = []
glb_activations_saved_e = []
spad_activations_saved_e = []

DRAM_masks_e = []
glb_masks_e = []
spad_masks_e = []

DRAM_pointer_e = []
glb_pointer_e = []
spad_pointer_e = []

comparator_e = []

dense_mac_e = []
sparse_mac_e = []
saved_mac_e = []

#Break down for activations
dense_ifmap_e = [[] for _ in range(3)]
sparse_ifmap_e = [[] for _ in range(3)]

dense_ofmap_e = [[] for _ in range(3)]




#similar to dense
def get_layer_residual_stats(file, block):
    global out_ch, pixels
    with open(file) as f:
        txt = f.readlines()
    e = 0.0
    c = 0.0

    total_activations = 2 * (pixels[block]**2) * out_ch[block]

    #ind_DRAM_begin = txt.index('Level 4')
    #ind_DRAM_end = txt.index('Networks')
    #DRAM_section = txt[ind_DRAM_begin:ind_DRAM_end]
    #read acts from
    #DRAM
    e += DRAM_access_e * total_activations
    #GLB
    e += GLB_access_e * total_activations
    #SPAD
    e += SPAD_access_e * total_activations

    e += int_add_e * total_activations/2
    #write acts back
    e += DRAM_access_e * total_activations/2
    e += GLB_access_e * total_activations/2
    e += SPAD_access_e * total_activations/2
    e *= 0.000001

    c = int(total_activations/2/PE)

    return e, c


#(similar to dense) since poolings have 1 in_ch -> this fixes the input channel energy for them
def fix_pooling(file, layer, block):
    global in_ch, out_ch, pixels, stride

    with open(file) as f:
       txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')
    DRAM_perc.append(float(txt[ind+13].split()[2]) / float(txt[ind+18].split()[2]))

    e = float(txt[ind+4].split()[1])
    c = int(txt[ind+3].split()[1])

    ind_DRAM_begin = txt.index('Level 4')
    ind_DRAM_end = txt.index('Networks')
    DRAM_section = txt[ind_DRAM_begin:ind_DRAM_end]
    DRAM_ifmaps_e = float(DRAM_section[DRAM_section.index('Inputs:')+12].split()[3])

    print(DRAM_ifmaps_e)
    e += DRAM_ifmaps_e*1e-6*(out_ch[block]-1)

    return e, c


def fix_weight_energy(memory, memory_e, section, e, density, in_channel, out_channel, k, sparse=True):

    global dense_DRAM_e, dense_glb_e, dense_spad_e, sparse_DRAM_e, sparse_glb_e, sparse_spad_e
    global DRAM_weights_saved_e, glb_weights_saved_e, spad_weights_Saved_e
    global DRAM_masks_e, glb_masks_e, spad_masks_e
    global DRAM_pointer_e, glb_pointer_e, spad_pointer_e

    if 'Weights:' in section:
        w_e = 1e-6 * float(section[section.index('Weights:')+12].split()[3])
        e_adjusted = e - w_e + density * w_e

        if memory == "DRAM":
            mask_array_e = (k**2 * in_channel * out_channel) / 16 * memory_e
            pointer_array_e = out_channel * POINTER_BITS / 16 * memory_e

            dense_DRAM_e.append(w_e)
            if sparse:
                sparse_DRAM_e.append(density * w_e + 1e-6*(mask_array_e + pointer_array_e))
                DRAM_weights_saved_e.append(w_e - density * w_e - 1e-6*(mask_array_e + pointer_array_e))
                DRAM_masks_e.append(mask_array_e*1e-6)
                DRAM_pointer_e.append(pointer_array_e*1e-6)
            else:
                sparse_DRAM_e.append(w_e)
                DRAM_weights_saved_e.append(0)
                DRAM_masks_e.append(0)
                DRAM_pointer_e.append(0)

        elif memory == "glb":
            mask_array_e = (k**2 * in_channel * out_channel) / 16 * memory_e * 2 #GLB needs both write and read
            pointer_array_e = 0

            dense_glb_e.append(w_e)
            if sparse:
                sparse_glb_e.append(density * w_e + 1e-6*(mask_array_e + pointer_array_e))
                glb_weights_saved_e.append(w_e - density * w_e - 1e-6*(mask_array_e + pointer_array_e))
                glb_masks_e.append(mask_array_e*1e-6)
                glb_pointer_e.append(pointer_array_e*1e-6)
            else:
                sparse_glb_e.append(w_e)
                glb_weights_saved_e.append(0)
                glb_masks_e.append(0)
                glb_pointer_e.append(0)

        else:
            mask_array_e = 0
            pointer_array_e = 0

            dense_spad_e.append(w_e)
            if sparse:
                 sparse_spad_e.append(density * w_e + (mask_array_e + pointer_array_e)*1e-6)
                 spad_weights_saved_e.append(w_e - density * w_e - (mask_array_e + pointer_array_e)*1e-6)
            else:
                 sparse_spad_e.append(w_e)
                 spad_weights_saved_e.append(0)
            spad_masks_e.append(mask_array_e)
            spad_pointer_e.append(pointer_array_e)

        e_adjusted += (mask_array_e + pointer_array_e)*1e-6

    else:
        e_adjusted = e
        if memory == "glb":
            dense_glb_e.append(0)
            sparse_glb_e.append(0)
            glb_masks_e.append(0)
            glb_pointer_e.append(0)
            glb_weights_saved_e.append(0)
        elif memory == "spad":
            dense_spad_e.append(0)
            sparse_spad_e.append(0)
            spad_weights_saved_e.append(0)

    return e_adjusted



def fix_act_energy(memory, section, e, density, sparse=True):
    global dense_ifmap_e, sparse_ifmap_e

    if 'Inputs:' in section:

        if not sparse:
            density = 1.0

        a_e = 1e-6 * float(section[section.index('Inputs:')+12].split()[3])
        e_adjusted = e - a_e + density * a_e
        if memory == "DRAM":
            dense_ifmap_e[0].append(a_e)
            sparse_ifmap_e[0].append(density * a_e)
        elif memory == "glb":
            dense_ifmap_e[1].append(a_e)
            sparse_ifmap_e[1].append(density * a_e)
        else:
            dense_ifmap_e[2].append(a_e)
            sparse_ifmap_e[2].append(density * a_e)

    else:
        e_adjusted = e
        if memory == "DRAM":
            dense_ifmap_e[0].append(0)
            sparse_ifmap_e[0].append(0)
        elif memory == "glb":
            dense_ifmap_e[1].append(0)
            sparse_ifmap_e[1].append(0)
        else:
            sparse_ifmap_e[2].append(0)
            dense_ifmap_e[2].append(0)

    return e_adjusted

def log_ofmap_energy(memory, section):
    global dense_ofmap_e
    if 'Outputs:' in section:
        a_e = 1e-6 * float(section[section.index('Outputs:')+12].split()[3])
        if memory == "DRAM":
            dense_ofmap_e[0].append(a_e)
        elif memory == "glb":
            dense_ofmap_e[1].append(a_e)
        else:
            dense_ofmap_e[2].append(a_e)

    else:
        if memory == "DRAM":
            dense_ofmap_e[0].append(0)
        elif memory == "glb":
            dense_ofmap_e[1].append(0)
        else:
            dense_ofmap_e[2].append(0)
    return



def get_layer_stats(file, layer="", density=1.0, stage="forward_pass", in_channels=16, out_channels=16, kernel=1):

    with open(file) as f:
        txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')
    #DRAM_perc.append(float(txt[ind+13].split()[2]) / float(txt[ind+18].split()[2]))

    e = float(txt[ind+4].split()[1])
    c = int(txt[ind+3].split()[1])

    DRAM_section = txt[txt.index('Level 4'):txt.index('Networks')]
    glb_section = txt[txt.index('Level 3'):txt.index('Level 4')]
    spad_section = txt[txt.index('Level 1'):txt.index('Level 2')]

    if stage == "forward_pass" or stage == "backward_pass":
        e = fix_weight_energy("DRAM", DRAM_access_e, DRAM_section, e, density, in_channels, out_channels, kernel)
        e = fix_weight_energy("glb", GLB_access_e, glb_section, e, density, in_channels, out_channels, kernel)
        e = fix_weight_energy("spad", SPAD_access_e, spad_section, e, density, in_channels, out_channels, kernel)

        fix_act_energy("DRAM", DRAM_section, e, density, sparse=False)
        fix_act_energy("glb", glb_section, e, density,sparse=False)
        fix_act_energy("spad", spad_section, e, density, sparse=False)

        log_ofmap_energy("DRAM", DRAM_section)
        log_ofmap_energy("glb", glb_section)
        log_ofmap_energy("spad", spad_section)

        if stage == "backward_pass":
            e += (in_channels * out_channels * (kernel**2) * COMPARATOR_e) * 1e-6
            comparator_e.append((in_channels * out_channels * (kernel**2) * COMPARATOR_e) * 1e-6)
        else:
            comparator_e.append(0)


    elif stage == "weight_update":

        #call fix weight just so that breakdown of weight energies are saved
        fix_weight_energy("DRAM", DRAM_access_e, DRAM_section, e, density, in_channels, out_channels, kernel, sparse=False)
        fix_weight_energy("glb", GLB_access_e, glb_section, e, density, in_channels, out_channels, kernel, sparse=False)
        fix_weight_energy("spad", SPAD_access_e, spad_section, e, density, in_channels, out_channels, kernel, sparse=False)

        e = fix_act_energy("DRAM", DRAM_section, e, density)
        e = fix_act_energy("glb", glb_section, e, density)
        e = fix_act_energy("spad", spad_section, e, density)

        log_ofmap_energy("DRAM", DRAM_section)
        log_ofmap_energy("glb", glb_section)
        log_ofmap_energy("spad", spad_section)

        comparator_e.append(0)

    mac_section = txt[txt.index('Level 0'):txt.index('Level 1')]
    mac_e = float(mac_section[14].split()[3])*1e-6
    dense_mac_e.append(mac_e)
    e = e - mac_e + density * mac_e
    sparse_mac_e.append(density * mac_e)
    saved_mac_e.append(mac_e-density * mac_e)
    c = int(math.ceil(c * density))

    return (e,c)



def get_block_stats(DIR, block, density, stage):

    global stats

    for layer in ['pw1', 'dw', 'pw2']:
        file = DIR + "b" +str(block-1) + "/" + layer + "/output/timeloop-mapper.stats.txt"
        tmp_k = 1
        if layer == "pw1":
            tmp_in_ch = in_ch[block]
            tmp_out_ch = midd_ch[block]
        elif layer == "dw":
            tmp_in_ch = midd_ch[block]
            tmp_out_ch = midd_ch[block]
            tmp_k = 3
        else:
            tmp_in_ch = midd_ch[block]
            tmp_out_ch = out_ch[block]


        e, c = get_layer_stats(file, layer, density=density, stage=stage, in_channels=tmp_in_ch, out_channels=tmp_out_ch, kernel=tmp_k)
        if layer == 'pw1':
            stats[0].append(e)
            stats[3].append(c)
        elif layer == 'dw':
            stats[1].append(e)
            stats[4].append(c)
        else:
            stats[2].append(e)
            stats[5].append(c)
            e, c = get_layer_residual_stats(file, block)
            stats[6].append(e)
            stats[7].append(c)


def make_csv(blocks, DIR, in_channels, midd_channels, out_channels, strides, pixs, model_desc, w_spar, g_spar, a_spar, debug_dram_frac=False, train=True):

    global stats, in_ch, midd_ch, out_ch, pixels, debug_DRAM_frac, model_description,\
           in_ch, stride, w_sparsity, g_sparsity, a_sparsity

    if train:
        stages = ["forward_pass", "backward_pass", "weight_update"]
    else:
        stages = ["forward_pass"]

    block_names = []
    stage_names = []
    total_e = []
    total_c = []
    out_ch = out_channels
    midd_ch = midd_channels
    in_ch = in_channels
    pixels = pixs
    stride = strides
    debug_DRAM_frac = debug_dram_frac
    model_description = model_desc
    w_sparsity = w_spar
    g_sparsity = g_spar
    a_sparsity = a_spar

    breakdown_layer_names = []
    breakdown_stage_names = []

    for stage in stages:

        for block, layer in enumerate(model_description):

            STAGE_DIR = DIR + stage + "/"

            stage_names.append(stage)

            if layer != "bottleneck":
                block_names.append(layer)
                if (layer == "max_pool" or layer == "ave_pool") and stage=="forward_pass":
                    e, c = fix_pooling(STAGE_DIR + layer +"/output/timeloop-mapper.stats.txt", layer, block)
                elif layer == "max_pool" or layer == "ave_pool":
                    e = 0
                    c = 0
                else:
                    breakdown_layer_names.append(layer)
                    breakdown_stage_names.append(stage)

                    if stage == "forward_pass":
                        local_density = (1.0 - w_sparsity[block])
                    elif stage == "backward_pass":
                        local_density = (1.0 - g_sparsity[block])
                    elif stage == "weight_update":
                        local_density = (1.0 - a_sparsity[block])

                    e, c = get_layer_stats(STAGE_DIR + layer +"/output/timeloop-mapper.stats.txt", density=local_density, stage=stage,
                                           in_channels=in_ch[block], out_channels=out_ch[block], kernel=3 if layer == "conv" else 1)

                for status in stats:
                    status.append(0)
                total_e.append(e)
                total_c.append(c)

            else: #here we are dealing with a bottleneck
                for i in range(3):
                    breakdown_stage_names.append(stage)
                breakdown_layer_names.append("b"+str(block)+"-pw1")
                breakdown_layer_names.append("b"+str(block)+"-dw")
                breakdown_layer_names.append("b"+str(block)+"-pw2")

                block_names.append(layer + str(block-1))

                if stage == "forward_pass":
                    local_density = (1.0 - w_sparsity[block])
                elif stage == "backward_pass":
                    local_density = (1.0 - g_sparsity[block])
                elif stage == "weight_update":
                    local_density = (1.0 - a_sparsity[block])

                get_block_stats(STAGE_DIR, block, local_density, stage)

                total_e.append(stats[0][block] + stats[1][block] + stats[2][block] + stats[6][block])
                total_c.append(stats[3][block] + stats[4][block] + stats[5][block] + stats[7][block])

    df = pandas.DataFrame(data={"0_stage":stage_names, "1_block": block_names, "2_PW1_e": stats[0],
                                "3_DW_e": stats[1], "4_PW2_e": stats[2], "5_residual_e": stats[6] ,
                                "6_block_total_e": total_e, "7_PW1_c": stats[3], "8_DW_c": stats[4],
                                "9_PW2_c": stats[5], "10_residual_c": stats[7], "11_block_total_c": total_c})

    df2 = pandas.DataFrame(data={
        "0_stage":breakdown_stage_names, "1_layer":breakdown_layer_names, "2_weights DRAM energy(dense)":dense_DRAM_e, "3_weights DRAM energy(sparse)":sparse_DRAM_e,
        "4_weights DRAM energy saved": DRAM_weights_saved_e, "5_weights masks DRAM energy overhead": DRAM_masks_e, "6_weights pointers DRAM energy overhead": DRAM_pointer_e,
        "7_weights glb energy(dense)":dense_glb_e, "8_weights glb energy(sparse)":sparse_glb_e, "9_weights glb energy saved": glb_weights_saved_e,
        "10_weights masks glb energy overhead": glb_masks_e, "11_weights pointers glb energy overhead": glb_pointer_e,
        "12_weights spad energy(dense)":dense_spad_e, "13_weights spad energy(sparse)":sparse_spad_e, "14_weights spad energy saved": spad_weights_saved_e,
        "15_iacts DRAM energy(dense)":dense_ifmap_e[0], "16_iacts DRAM energy(sparse)":sparse_ifmap_e[0],
        "17_iacts glb energy(dense)":dense_ifmap_e[1], "18_iacts glb energy(sparse)":sparse_ifmap_e[1],
        "19_iacts spad energy(dense)":dense_ifmap_e[2], "20_iacts spad energy(sparse)":sparse_ifmap_e[2],
        "21_oacts DRAM energy(dense)":dense_ofmap_e[0], "22_oacts glb energy(dense)":dense_ofmap_e[1], "23_oacts spad energy(dense)":dense_ofmap_e[2],
        "24_MACs energy(dense)":dense_mac_e, "25_MACs energy(sparse)":sparse_mac_e, "26_MACs energy saved":saved_mac_e, "27_gradient comparsion overhad": comparator_e
    })

    if train:
         df.to_csv("results/sparse_train.csv", sep=',',index=False)
         df2.to_csv("results/train_breakdown.csv")
    else:
        df.to_csv("results/sparse_inference.csv", sep=',',index=False)
        df2.to_csv("results/inference_breakdown.csv")

    if debug_DRAM_frac:
        ave = 0.0
        for item in DRAM_perc:
            ave += item
        print(ave/len(DRAM_perc))


#just test
#get_layer_stats("../baseline/forward_pass/b1/pw1/output/timeloop-mapper.stats.txt")
