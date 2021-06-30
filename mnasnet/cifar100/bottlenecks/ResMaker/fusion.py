import numpy as np
import sys
import pandas
import ResMaker.Package.FusionSim as FusionSim
import subprocess
import math


#fusion acc. config
F_PEs = 64
ADDERS = 16
#Fusion CNN configs
F_BLOCKS = 2
f_in_ch   = []
f_midd_ch = []
f_out_ch = []
f_pixels = []
f_stride = []
prune_factors = []



#Adjusting prediction simulations for 2-bit predictions
def adjust_pred(file, IN_CHANNELS, MIDD_CHANNELS, qtz=[4]*F_BLOCKS, pred1_qtz=False, pred2_qtz=False, decomp=True, block=1, q_blocks=10):
    global ADDERS
    conv = not decomp
    GLB_ACCESS_ENERGY = 18.8
    DRAM_ACCESS_ENERGY = 128.0
    DRAM_WIDTH = 16
    GLB_WIDTH = 8
    ADD_ENERGY = 0.000000043
    MAC_ENERGY = 0.00000022
    PRED_EFF = 7/8
    PRED_FMAP_BITRATIO = qtz[block]/16

    with open(file) as f:
        txt = f.readlines()
    txt = [x.strip() for x in txt]

    #energy values
    ind = txt.index('Summary Stats')
    raw_e = float(txt[ind+4].split()[1])
    total_MACs = float(txt[ind+7].split()[2])

    ind_DRAM_begin = txt.index('Level 6')
    ind_DRAM_end = txt.index('Networks')
    DRAM_section = txt[ind_DRAM_begin:ind_DRAM_end]
    total_fmaps = int(DRAM_section[DRAM_section.index('Outputs:')+1].split()[3])
    DRAM_ofmaps_e = float(DRAM_section[DRAM_section.index('Outputs:')+12].split()[3])
    DRAM_ifmaps_e = float(DRAM_section[DRAM_section.index('Inputs:')+12].split()[3])
    DRAM_weights_e = float(DRAM_section[DRAM_section.index('Weights:')+12].split()[3])

    ind_GLB_begin = txt.index('Level 5')
    GLB_section = txt[ind_GLB_begin:ind_DRAM_begin]
    glb_ofmap_e = float(GLB_section[GLB_section.index('Outputs:')+12].split()[3])
    glb_ifmap_e = float(GLB_section[GLB_section.index('Inputs:')+12].split()[3])

    spad_section = txt[txt.index('Level 2'):txt.index('Level 3')]
    spad_weights_e = float(spad_section[spad_section.index('Weights:')+12].split()[3])

    ifmap_buffer_section = txt[txt.index('Level 3'):txt.index('Level 4')]
    ifmap_buffer_e = float(ifmap_buffer_section[ifmap_buffer_section.index('Inputs:')+12].split()[3])


    MAC_section = txt[txt.index('Level 0'):txt.index('Level 1')]
    MAC_e = float(MAC_section[MAC_section.index('STATS')+4].split()[3])

    if decomp:
        total_MACs_adjusted = total_MACs/IN_CHANNELS
    else:
        total_MACs_adjusted = total_MACs/9
    total_ADDs = total_MACs

    pred_DRAM_energy = total_fmaps*DRAM_ACCESS_ENERGY/DRAM_WIDTH

    #Adjusting energy
    adjusted_e = raw_e * 1000000
    adjusted_e += pred_DRAM_energy  #energy for writing pred masks to pred GLB
    adjusted_e -= PRED_EFF*DRAM_weights_e  #energy for fetching weights from DRAM
    adjusted_e -= PRED_EFF*spad_weights_e  #energy for reading weights from SPAD
    adjusted_e -= MAC_e            #energy for MACs

    if conv:
        #to fix simulation of depthwise layers
        adjusted_e -= (DRAM_ifmaps_e)
        adjusted_e += (DRAM_ifmaps_e) * MIDD_CHANNELS

        if pred2_qtz and block<q_blocks:
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (DRAM_ifmaps_e * MIDD_CHANNELS) #energy for reading ifmaps
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (glb_ifmap_e)
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (ifmap_buffer_e)
        elif pred2_qtz:
            adjusted_e -= 7/8 * (DRAM_ifmaps_e * MIDD_CHANNELS)
            adjusted_e -= 7/8 * (glb_ifmap_e)

        adjusted_e -= glb_ofmap_e  #don't write back fmaps even to GLB if predicting second layer
        adjusted_e -= DRAM_ofmaps_e    #energy for writing fmaps to DRAM

    else:
        if pred2_qtz and block<q_blocks:
            #Only sending to DRAM is post quantization, because C is looped in GLB
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (DRAM_ifmaps_e)
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (glb_ifmap_e)
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * (ifmap_buffer_e)
            adjusted_e -= (1.00 - PRED_FMAP_BITRATIO) * DRAM_ofmaps_e

        elif pred2_qtz:
            adjusted_e -= 7/8 * DRAM_ofmaps_e
            adjusted_e -= 7/8 * glb_ofmap_e

    adjusted_e *= 0.000001
    if pred2_qtz:
        adjusted_e += MAC_ENERGY*total_MACs_adjusted + ADD_ENERGY*total_ADDs*(PRED_FMAP_BITRATIO)
    else:
        adjusted_e += MAC_ENERGY*total_MACs_adjusted + ADD_ENERGY*total_ADDs

    #****DEBUG******
    #debug
    if decomp:
        print(pred_DRAM_energy, DRAM_ifmaps_e, (PRED_FMAP_BITRATIO)*DRAM_ofmaps_e, (1-PRED_EFF) * DRAM_weights_e, (1-PRED_EFF) * spad_weights_e, MAC_e, MAC_ENERGY*total_MACs_adjusted + ADD_ENERGY*total_ADDs, adjusted_e)
    else:
        print(pred_DRAM_energy, (PRED_FMAP_BITRATIO)*DRAM_ifmaps_e, 0, (1-PRED_EFF) * DRAM_weights_e, spad_weights_e, MAC_e, MAC_ENERGY*total_MACs_adjusted + ADD_ENERGY*total_ADDs, adjusted_e)

    #cycle
    adjusted_c = int(math.floor(int(txt[txt.index('Summary Stats')+3].split()[1]) / ADDERS))

    return (adjusted_e, adjusted_c)


#******************************************************
def get_main_data(file):
    with open(file) as f:
        txt = f.readlines()
    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')
    e = float(txt[ind+4].split()[1])
    ind_DRAM_begin = txt.index('Level 4')
    ind_DRAM_end = txt.index('Networks')
    DRAM_section = txt[ind_DRAM_begin:ind_DRAM_end]
    DRAM_weights_e = float(DRAM_section[DRAM_section.index('Weights:')+12].split()[3])
    e -= (DRAM_weights_e*0.000001)
    c = int(txt[txt.index('Summary Stats')+3].split()[1])
    return (e,c)



weight_DRAM_l = []
pred_DRAM_l = []
pred_glb_l = []
binary_decode_l = []
pred_buffer_l = []
masks_l = []
mux__l = []
mux_l = []
adders_l = []



def get_extra_energy(file, fused_weights, block):

    global F_PEs
    DRAM_ACCESS_ENERGY = 128.00
    GLB_ACCESS_ENERGY = 18.00

    WEIGHTS_BITS = 16
    INDEX_BITS = 10
    INDEX_FACTOR = (WEIGHTS_BITS/INDEX_BITS)
    WEIGHTS_REFETCH = (f_pixels[block]**2) / F_PEs

    with open(file) as f:
        txt = f.readlines()
    txt = [x.strip() for x in txt]

    weight_DRAM =  fused_weights * DRAM_ACCESS_ENERGY * INDEX_FACTOR * WEIGHTS_REFETCH

    ind = 4
    pred_DRAM = float(txt[ind].split()[1]) * (DRAM_ACCESS_ENERGY/GLB_ACCESS_ENERGY)
    pred_glb = 0 #float(txt[ind].split()[1])
    binary_decode = float(txt[ind+2].split()[1])
    pred_buffer = float(txt[ind+4].split()[1])
    adders = float(txt[ind+6].split()[1])
    masks = float(txt[ind+8].split()[1])
    mux_ = float(txt[ind+10].split()[1])
    mux = float(txt[ind+12].split()[1])

    e = (weight_DRAM + pred_DRAM + pred_glb + binary_decode + F_PEs*(pred_buffer+masks+mux_+mux+adders))*0.000001

    weight_DRAM_l.append(weight_DRAM*0.000001)
    pred_DRAM_l.append(pred_DRAM*0.000001)
    pred_glb_l.append(pred_glb*0.000001)
    binary_decode_l.append(binary_decode*0.000001)
    pred_buffer_l.append(F_PEs*pred_buffer*0.000001)
    masks_l.append(F_PEs*masks*0.000001)
    mux__l.append(F_PEs*mux_*0.000001)
    mux_l.append(F_PEs*mux*0.000001)
    adders_l.append(F_PEs*adders*0.000001)
    return e



def make_csv(BLOCKS, pes, PE_adders, in_ch, midd_ch, out_ch, pixels, stride, pruning, pred1_qtz=False, pred2_qtz=False, pred_qtz=4, q_blocks=10):

    global F_PEs, ADDERS, F_BLOCKS, f_in_ch, f_midd_ch, f_out_ch, f_pixels, f_stride, prune_factors

    F_PEs = pes
    ADDERS = PE_adders
    #Fusion CNN configs
    F_BLOCKS = BLOCKS
    f_in_ch   = in_ch
    f_midd_ch = midd_ch
    f_out_ch = out_ch
    f_pixels = pixels
    f_stride = stride
    prune_factors = pruning



    decom_e = []
    decom_c = []
    for block in range(BLOCKS):
        file = "fusion/predictions/b" +str(block+1) + "/decom/output/timeloop-mapper.stats.txt"
        in_ch = f_in_ch[block]
        midd_ch = f_midd_ch[block]
        e, c = adjust_pred(file, in_ch, midd_ch, pred1_qtz=pred1_qtz, pred2_qtz=pred2_qtz, qtz=pred_qtz, block=block, q_blocks= q_blocks)
        decom_e.append(e)
        decom_c.append(c)

    conv_e = []
    conv_c = []
    for block in range(BLOCKS):
        file = "fusion/predictions/b" + str(block+1) + "/conv/output/timeloop-mapper.stats.txt"
        in_ch = f_in_ch[block]
        midd_ch = f_midd_ch[block]
        e, c = adjust_pred(file, in_ch, midd_ch, decomp=False, pred1_qtz=pred1_qtz, pred2_qtz=pred2_qtz, qtz=pred_qtz, block=block, q_blocks= q_blocks)
        conv_e.append(e)
        conv_c.append(c)



    main_e = []
    main_c = []
    for block in range(BLOCKS):
        if block not in [2, 5, 6, 9]:
            file = "fusion/main_computations/b" + str(block+1) + "/output/timeloop-mapper.stats.txt"
            e, c = get_main_data(file)
        main_e.append(e)
        main_c.append(c)



    extra_energy = []
    M = [1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 1]

    for block in range(BLOCKS):

        if block != 0:
            subprocess.run(["cp", "-r", "fusion/fusion_overhead/b" + str(block), "fusion/fusion_overhead/b" + str(block+1)])
        subprocess.run(["rm", "-rf", "fusion/fusion_overhead/b" + str(block+1) + "/output"])
        subprocess.run(["mkdir", "fusion/fusion_overhead/b" + str(block+1) + "/output"])

        ACCELERGY_DIR = "fusion/fusion_overhead/b" + str(block+1)

        #Create action counts for this block
        FusionSim.create_action_counts(in_ch=f_in_ch[block], midd_ch=f_midd_ch[block], out_ch=f_out_ch[block], pixels=f_pixels[block], stride=f_stride[block],\
                               prune_factor=prune_factors[block], cycles=main_c[block], outer_M=M[block], file=ACCELERGY_DIR+"/action_counts/action_counts.yaml",\
                               PE_adders=ADDERS, total_PEs=F_PEs)

        #call accelergy and get energy overhead for this block
        p = subprocess.Popen(["accelergy", "./../accelerator/fusion/overhead", ACCELERGY_DIR+"/action_counts/", "-o", ACCELERGY_DIR+"/output/"],\
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        p.wait()
        #subprocess.run(["accelergy", "fusion/fusion_overhead/arch/", ACCELERGY_DIR+"/action_counts/" , "-o", ACCELERGY_DIR+"/output/"])

        #use result of accelergy and create csv
        file = ACCELERGY_DIR + "/output/energy_estimation.yaml"
        fused_weights = f_in_ch[block] * f_midd_ch[block] * 9 * f_out_ch[block] * prune_factors[block]
        e = get_extra_energy(file, fused_weights, block)
        extra_energy.append(e)
        print("fusion overhead energy for block " + str(block+1))


    df = pandas.DataFrame(data={"1_pred_decom_e": decom_e, "2_pred_conv_e": conv_e, "3_main_e": main_e, "4_overhead_e": extra_energy,\
                                "5_pred_decom_c": decom_c, "6_pred_conv_c": conv_c, "7_main_c": main_c})

    df.to_csv("./results/fusion_results.csv", sep=',',index=False, float_format='%.2f')


    df2 = pandas.DataFrame(data={"1_weight_DRAM": weight_DRAM_l, "2_pred_DRAM": pred_DRAM_l, "3_pred_glb": pred_glb_l, "4_binary_decoder": binary_decode_l,\
                            "5_pred_buffer": pred_buffer_l, "6_zero_replace_flag": mux__l, "7_zero_replacing": mux_l, "8_adders":adders_l, "9_masks_AND": masks_l})
    df2.to_csv("./results/fusion_overhead.csv", sep=',',index=False, float_format='%.2f')
