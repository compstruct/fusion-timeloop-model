import numpy as np
import sys
import pandas
import csv

stats = [ [] for _ in range(6)]
midd_channels = []



sparse_stats = [ [] for _ in range(3)]


def get_sparse_layer_energy(file, layer, MIDD_CHANNELS, sparsity=0.91, sparse_ind_bits=10):


    with open(file) as f:
        txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')
    e = float(txt[ind+4].split()[1])


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

    ind_wbuffer_begin = txt.index('Level 2')
    ind_wbuffer_end = txt.index('Level 3')
    wbuffer_section = txt[ind_wbuffer_begin:ind_wbuffer_end]
    wbuffer_weights_e = float(wbuffer_section[wbuffer_section.index('Weights:')+12].split()[3])

    ind_ifmap_buffer_begin = txt.index('Level 3')
    ind_ifmap_buffer_end = txt.index('Level 4')
    ifmap_buffer_section = txt[ind_ifmap_buffer_begin:ind_ifmap_buffer_end]
    ifmap_buffer_weights_e = float(ifmap_buffer_section[ifmap_buffer_section.index('Inputs:')+12].split()[3])

    #only depthwise layer needs it's simulation fixed
    if layer == 'conv':
        e -= (glb_ifmap_e + DRAM_ifmaps_e)*0.000001
        e += (glb_ifmap_e + DRAM_ifmaps_e)*0.000001*MIDD_CHANNELS
    #only pw layers are sparse
    else:
        DRAM_weights_e *= sparsity
        e -= DRAM_weights_e * 0.000001
        e += DRAM_weights_e * 0.000001 * sparse_ind_bits/16

        wbuffer_weights_e *= sparsity
        e -= wbuffer_weights_e * 0.000001
        e += wbuffer_weights_e * 0.000001 * sparse_ind_bits/16

        ifmap_buffer_weights_e *= sparsity
        e -= ifmap_buffer_weights_e * 0.000001
    return e



def get_sparse_block_energy(DIR, block, groups):

    global sparse_stats, midd_channels

    for layer in ['decom', 'conv', 'comp']:
        file = DIR + "b" +str(block+1) + "/" + layer + "/output/timeloop-mapper.stats.txt"
        e = get_sparse_layer_energy(file, layer, midd_channels[block])
        if layer == 'decom':
            sparse_stats[0].append(e*groups)
        elif layer == 'conv':
            sparse_stats[1].append(e)
        else:
            sparse_stats[2].append(e*groups)

def sparse_csv(groups):
    global sparse_stats
    with open('./results/sparse_bl_res.csv', mode='r') as sparse_bl_file:
        sparse_bl_reader = csv.reader(sparse_bl_file)

        #summarize sparse results in a new CSV
        with open("./results/sprase_bl_summary.csv", 'w', newline='') as sparse_bl_summarized_file:
            sparse_bl_writer = csv.writer(sparse_bl_summarized_file, quoting=csv.QUOTE_ALL)
            sparse_bl_writer.writerow(["sparse_PW1_e", "sparse_DW_e", "sparse_PW2_e", "sparse_PW1_C", "sparse_PW2_C", "sparse_DW_C"])
            i = -1
            data = []
            for row in sparse_bl_reader:
                if i>=0:
                    if i%3==0 and i>1:
                        sparse_bl_writer.writerow([sparse_stats[0][i//3 -1], sparse_stats[1][i//3 -1], sparse_stats[2][i//3 -1]]+data)
                        data = []
                    if i % 3 == 2:
                        data.append(str(int(row[-1])))
                    else:
                        data.append(str(int(row[-1])*groups))
                i += 1
            sparse_bl_writer.writerow([sparse_stats[0][-1], sparse_stats[1][-1], sparse_stats[2][-1]]+data)



def get_layer_stats(file, groups, MIDD_CHANNELS, layer):

    with open(file) as f:
        txt = f.readlines()

    txt = [x.strip() for x in txt]
    ind = txt.index('Summary Stats')

    e = float(txt[ind+4].split()[1])
    c = int(txt[ind+3].split()[1])

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
    if layer == 'conv':
        e -= (glb_ifmap_e + DRAM_ifmaps_e)*0.000001
        e += (glb_ifmap_e + DRAM_ifmaps_e)*0.000001*MIDD_CHANNELS
    else:
        e *= groups
        c *= groups

    return (e,c)



def get_block_stats(DIR, block, groups):

    global stats, midd_channels

    for layer in ['decom', 'comp', 'conv']:
        file = DIR + "b" +str(block+1) + "/" + layer + "/output/timeloop-mapper.stats.txt"
        e, c = get_layer_stats(file, groups, midd_channels[block], layer)
        if layer == 'decom':
            stats[0].append(e)
            stats[1].append(c)
        elif layer == 'comp':
            stats[2].append(e)
            stats[3].append(c)
        else:
            stats[4].append(e)
            stats[5].append(c)



def make_csv(blocks, DIR, groups, bl_midd_channels):

    global stats, midd_channels
    midd_channels = bl_midd_channels

    for block in range(blocks):
        get_block_stats(DIR, block, groups)


    df = pandas.DataFrame(data={"1_PW1_e": stats[0], "2_PW2_e": stats[2], "3_DW_e": stats[4],\
                                "4_PW1_c": stats[1], "5_PW2_c": stats[3], "6_DW_c": stats[5]})
    df.to_csv("results/bl_res.csv", sep=',',index=False, float_format='%.2f')

    for block in range(blocks):
        get_sparse_block_energy(DIR, block, groups)
    sparse_csv(groups)
