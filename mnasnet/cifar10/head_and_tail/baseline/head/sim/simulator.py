import numpy as np
import sys
import pandas
import os
import subprocess
import time
import yaml
import resmaker.bl as bl
import resmaker.sparse as sparse

#Simulator configs
debug_timeloop_output = False
mapper_pars = []
dw_mapper_pars = []
root = ""
#baseline CNN configs
BLOCKS = 0
batch = 1

in_ch   = []
out_ch = []

pixels = []
strides = []

descriptions = []
names = []


def run_timeloop(DIR, LAYER_DIR, layer = "pw"):

    accelerator_path = "./../../../../../accelerator"
    if layer == "dw" or layer == "conv" or layer == "max_pool" or layer == "ave_pool":
        mapper = DIR+'dw_mapper/mapper.yaml'
    else:
        mapper = DIR+'mapper/mapper.yaml'

    if not debug_timeloop_output:
        p = subprocess.Popen(['timeloop-mapper', accelerator_path+'/baseline/arch.yaml', accelerator_path+'/baseline/components/smartbuffer_RF.yaml',
                         accelerator_path+'/baseline/components/smartbuffer_SRAM.yaml', mapper, LAYER_DIR+'prob/prob.yaml',
                         LAYER_DIR+'constraints/arch_constraints.yaml', LAYER_DIR+'constraints/map_constraints.yaml', '-o', LAYER_DIR+'output'], 
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            time.sleep(3)
            p.communicate(input="a")
            if p.poll() != None:
                break
    else:
        subprocess.run(['timeloop-mapper', accelerator_path+'/baseline/arch.yaml', accelerator_path+'/baseline/components/smartbuffer_RF.yaml',
                        accelerator_path+'/baseline/components/smartbuffer_SRAM.yaml',\
                     mapper, LAYER_DIR+'prob/prob.yaml', LAYER_DIR+'constraints/arch_constraints.yaml',\
                     LAYER_DIR+'constraints/map_constraints.yaml', '-o', LAYER_DIR+'output'])

    return

#*****************Setup layer as Timeloop problem**************
#**************************************************************

def fix_layer_shape_forward(BLOCK_DIR, layer, block, bottleneck=False):

    global in_ch, out_ch, pixels, strides, batch

    problem_file = BLOCK_DIR + "prob/prob.yaml"

    with open(problem_file, 'r') as file:
        prob = yaml.safe_load(file)
    prob['problem']['instance']['C'] = in_ch[block]
    prob['problem']['instance']['M'] = out_ch[block]
    prob['problem']['instance']['Wstride'] = strides[block]
    prob['problem']['instance']['Hstride'] = strides[block]

    if layer == "conv" or layer == "max_pool":
        prob['problem']['instance']['S'] = 3
        prob['problem']['instance']['R'] = 3

    elif layer == "ave_pool":
        prob['problem']['instance']['S'] = 8
        prob['problem']['instance']['R'] = 8

    elif layer == "FC" or layer == "pw" or layer == "gpw":
        prob['problem']['instance']['S'] = 1
        prob['problem']['instance']['R'] = 1

    prob['problem']['instance']['P'] = pixels[block]
    prob['problem']['instance']['Q'] = pixels[block]
    prob['problem']['instance']['N'] = 1

    with open(problem_file, 'w') as file:
        yaml.dump(prob, file)



def fix_mapper(DIR):

    global mapper_pars, dw_mapper_pars

    with open(DIR + "mapper/mapper.yaml", 'r') as file:
        mapper = yaml.safe_load(file)

    mapper['mapper']['timeout'] = mapper_pars[0]
    mapper['mapper']['victory-condition'] = mapper_pars[1]

    with open(DIR + "mapper/mapper.yaml", 'w') as file:
        yaml.dump(mapper, file)

    with open(DIR + "dw_mapper/mapper.yaml", 'r') as file:
        dw_mapper = yaml.safe_load(file)

    dw_mapper['mapper']['timeout'] = dw_mapper_pars[0]
    dw_mapper['mapper']['victory-condition'] = dw_mapper_pars[1]

    with open(DIR + "dw_mapper/mapper.yaml", 'w') as file:
        yaml.dump(dw_mapper, file)

    return



#def fix_layer_constraints(BLOCK_DIR, name, layer, block, stage):

#    with open(BLOCK_DIR + layer + "/constraints/arch_constraints.yaml", 'r') as file:
#        const = yaml.safe_load(file)

#    for i in range(len(const['architecture_constraints']['targets'])):
#        current_const = const['architecture_constraints']['targets'][i]

#        if current_const['target'] == 'shared_glb' and current_const['type'] == 'spatial':
#            if stage == "weight_update":
#                const['architecture_constraints']['targets'][i]['factors'] = "Q=1 P=1 R=1 S=1 N=1 M=1 C=16"
#            elif train:
#                const['architecture_constraints']['targets'][i]['factors'] = "Q=1 P=1 R=1 S=1 C=1 M=1 N=16"
#            else:
#                const['architecture_constraints']['targets'][i]['factors'] = "Q=1 P=1 R=1 S=1 M=1 N=1 C=16"

#        elif current_const['target'] == 'spad' and current_const['type'] == 'temporal':
#            if layer in ["conv", "dw", "max_pool", "ave_pool"]:
#                const['architecture_constraints']['targets'][i]['factors'] = ""
#            else:
#                const['architecture_constraints']['targets'][i]['factors'] = "R=1 S=1"
            #if layer in ["conv", "dw", "max_pool"]:
             #   const['architecture_constraints']['targets'][i]['factors'] = "R=3 S=3"
            #elif layer == "ave_pool":
             #   const['architecture_constraints']['targets'][i]['factors'] = "R=7 S=7"
            #else:
             #   const['architecture_constraints']['targets'][i]['factors'] = "R=1 S=1"

#    with open(BLOCK_DIR + layer + "/constraints/arch_constraints.yaml", 'w') as file:
#        yaml.dump(const, file)





def dense_sim(train=True):

    global descriptions, root

    DIR = root + "/"
    fix_mapper(DIR)

    for tmp_block in range(BLOCKS):
        if tmp_block != 0:
            subprocess.run(['rm', '-rf', DIR + names[tmp_block]])
            subprocess.run(['cp', '-r', DIR + "conv1", DIR + names[tmp_block]])

        #fix_layer_constraints(DIR, model_description[tmp_block], tmp_block, stage, train)

        fix_layer_shape_forward(DIR + names[tmp_block] + "/", descriptions[tmp_block], tmp_block)

        t1 = time.time()
        run_timeloop(DIR, DIR + names[tmp_block] + "/", layer=descriptions[tmp_block])
        t2 = time.time()
        print("simulation for " + names[tmp_block] + " and it took", int(t2-t1))
        time.sleep(3)
    return



def simulate(timeloop_output, mapper, dw_mapper, blocks, loc_in_ch, loc_out_ch, loc_pixels,
      loc_stride, loc_batch, m_desc, m_names, CSV_only, loc_root="./baseline"):

    global mapper_pars, dw_mapper_pars, debug_timeloop_output, root
    global BLOCKS, batch
    global in_ch, out_ch, pixels, strides, descriptions, names

    debug_timeloop_output = timeloop_output
    mapper_pars = mapper
    dw_mapper_pars = dw_mapper
    root = loc_root

    BLOCKS = blocks
    batch = 1

    in_ch   = loc_in_ch
    out_ch = loc_out_ch

    pixels = loc_pixels
    strides = loc_stride

    descriptions = m_desc
    names = m_names

    if (not CSV_only):
        dense_sim()
    bl.make_csv(BLOCKS, "./baseline/", in_ch, out_ch, pixels, strides, descriptions, names)
