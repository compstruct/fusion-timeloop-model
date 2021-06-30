import numpy as np
import sys
import pandas
import os
import subprocess
import time
import yaml
import ResMaker.fusion as fusion



#*****Configurations********
#simulator configs
DELAY = 20
pred_mapper_pars = []
pred_dw_mapper_pars = []
main_mapper_pars = []

#fusion acc. config
F_PEs = 128
X_PEs = 8
PRED_SPATIAL_GLB = {}
PRED_SPATIAL_DUMMY = {}

#Fusion CNN configs
F_BLOCKS = 13
f_in_ch   = []
f_midd_ch = []
f_out_ch = []
f_pixels = []
f_stride = []




#**************************************************************************************
#Prediction Funstions******************************************************************
#**************************************************************************************

def fix_layer_shape(BLOCK_DIR, layer, block):
    with open(BLOCK_DIR + layer + "/prob/prob.yaml", 'r') as file:
        prob = yaml.safe_load(file)

    if layer == 'conv':
        prob['problem']['instance']['M'] = f_midd_ch[block]
        prob['problem']['instance']['Wstride'] = f_stride[block]
        prob['problem']['instance']['Hstride'] = f_stride[block]

    elif layer == 'decom':
        prob['problem']['instance']['C'] = f_in_ch[block]
        prob['problem']['instance']['M'] = f_midd_ch[block]

    if layer == 'decom':
        prob['problem']['instance']['P'] = f_pixels[block] * f_stride[block]
        prob['problem']['instance']['Q'] = f_pixels[block] * f_stride[block]
    else:
        prob['problem']['instance']['P'] = f_pixels[block]
        prob['problem']['instance']['Q'] = f_pixels[block]
    with open(BLOCK_DIR + layer + "/prob/prob.yaml", 'w') as file:
        yaml.dump(prob, file)

def fix_block_shape(BLOCK_DIR, block):
    fix_layer_shape(BLOCK_DIR, 'decom', block)
    fix_layer_shape(BLOCK_DIR, 'conv', block)


def fix_layer_constraints(BLOCK_DIR, layer, block):

    with open(BLOCK_DIR + layer + "/constraints/constraints.yaml", 'r') as file:
        const = yaml.safe_load(file)

    for i in range(len(const['architecture_constraints']['targets'])):
        current_const = const['architecture_constraints']['targets'][i]

        if current_const['target'] == 'shared_glb' and current_const['type'] == 'spatial':
            const['architecture_constraints']['targets'][i]['factors'] = PRED_SPATIAL_GLB[layer]

        elif current_const['target'] == 'DummyBuffer' and current_const['type'] == 'spatial':
            const['architecture_constraints']['targets'][i]['factors'] = PRED_SPATIAL_DUMMY[layer]

    with open(BLOCK_DIR + layer + "/constraints/constraints.yaml", 'w') as file:
        yaml.dump(const, file)

def fix_block_constraints(BLOCK_DIR, block):
    fix_layer_constraints(BLOCK_DIR, 'decom', block)
    fix_layer_constraints(BLOCK_DIR, 'conv', block)



def fix_pred_mapper(DIR):

    global pred_mapper_pars, pred_dw_mapper_pars

    with open(DIR + "mapper/mapper.yaml", 'r') as file:
        mapper = yaml.safe_load(file)

    mapper['mapper']['timeout'] = pred_mapper_pars[0]
    mapper['mapper']['victory-condition'] = pred_mapper_pars[1]

    with open(DIR + "mapper/mapper.yaml", 'w') as file:
        yaml.dump(mapper, file)

    with open(DIR + "dw_mapper/mapper.yaml", 'r') as file:
        mapper = yaml.safe_load(file)

    mapper['mapper']['timeout'] = pred_dw_mapper_pars[0]
    mapper['mapper']['victory-condition'] = pred_dw_mapper_pars[1]

    with open(DIR + "dw_mapper/mapper.yaml", 'w') as file:
        yaml.dump(mapper, file)



def run_timeloop(DIR, LAYER_DIR, dw=False):
    if dw == True:
        mapper = DIR+'dw_mapper/mapper.yaml'
    else:
        mapper = DIR+'mapper/mapper.yaml'

    p = subprocess.Popen(['timeloop-mapper', './../accelerator/fusion/predictions/arch.yaml', './../accelerator/fusion/predictions/components/smartbuffer_RF.yaml',\
                          './../accelerator/fusion/predictions/components/smartbuffer_SRAM.yaml', mapper, LAYER_DIR+'prob/prob.yaml', LAYER_DIR+'constraints/constraints.yaml',\
                          '-o', LAYER_DIR+'output'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        time.sleep(3)
        p.communicate(input="a")
        if p.poll() != None:
            break


def fusion_pred_sim(DIR):
    PRED_DIR = DIR + "predictions/"
    fix_pred_mapper(PRED_DIR)
    for block in range(F_BLOCKS):
        PRED_BLOCK_DIR = PRED_DIR + "b"  + str(block+1) + "/"

        if block != 0:
            if os.path.isfile(PRED_DIR + 'b'+str(block+1)):
                subprocess.run(['rm', '-rf', PRED_DIR + 'b'+str(block+1)])
            subprocess.run(['cp', '-r', PRED_DIR+ 'b'+str(block), PRED_DIR + 'b'+str(block+1)])

        fix_block_shape(PRED_BLOCK_DIR, block)
        fix_block_constraints(PRED_BLOCK_DIR, block)

        t1 = time.time()
        run_timeloop(PRED_DIR, PRED_BLOCK_DIR+"decom/")
        t2 = time.time()
        print("fusion predictions pw block ", block+1, " and took ", t2-t1)

        t1 = time.time()
        run_timeloop(PRED_DIR, PRED_BLOCK_DIR+"conv/", dw=True)
        t2 = time.time()
        print("fusion predictions dw block ", block+1, " and took ", t2-t1)

#****************************************************************************************************
#****************************************************************************************************



#**************************************************************************************
#Main Computation Funstions************************************************************
#**************************************************************************************
def fix_block_constraints_main(BLOCK_DIR, block):

    #if f_pixels[block] == 32:
    #    q_dummy_spatial = 16
    #    q_glb_spatial = 2
    #    p_spatial = X_PEs//2

    #else:
    #    q_dummy_spatial = f_pixels[block]
    #    q_glb_spatial = 0
    #    p_spatial = X_PEs

    with open(BLOCK_DIR + "constraints/constraints.yaml", 'r') as file:
        const = yaml.safe_load(file)

    for i in range(len(const['architecture_constraints']['targets'])):
        current_const = const['architecture_constraints']['targets'][i]

        if current_const['target'] == 'shared_glb' and current_const['type'] == 'temporal':
            const['architecture_constraints']['targets'][i]['factors'] = 'N=1 R=1 S=1 Q=1 C=' + str(f_in_ch[block]) + ' M=' + str(f_out_ch[block])

        elif current_const['target'] == 'shared_glb' and current_const['type'] == 'spatial':
            const['architecture_constraints']['targets'][i]['factors'] = 'N=1 R=1 S=1 C=1 M=1 P=' + str(8) + ' Q=' + str(1)

        elif current_const['target'] == 'DummyBuffer' and current_const['type'] == 'spatial':
            const['architecture_constraints']['targets'][i]['factors'] = 'N=1 R=1 S=1 C=1 M=1 P=1 Q=' + str(8)

    with open(BLOCK_DIR + "constraints/constraints.yaml", 'w') as file:
        yaml.dump(const, file)



def fix_block_shape_main(BLOCK_DIR, block):
    with open(BLOCK_DIR + "prob/prob.yaml", 'r') as file:
        prob = yaml.safe_load(file)

    prob['problem']['instance']['Wstride'] = f_stride[block]
    prob['problem']['instance']['Hstride'] = f_stride[block]
    prob['problem']['instance']['C'] = f_in_ch[block]
    prob['problem']['instance']['M'] = f_out_ch[block]
    prob['problem']['instance']['P'] = f_pixels[block]
    prob['problem']['instance']['Q'] = f_pixels[block]

    with open(BLOCK_DIR + "prob/prob.yaml", 'w') as file:
        yaml.dump(prob, file)


def fix_main_mapper(DIR):

    global main_mapper_pars

    with open(DIR + "mapper/mapper.yaml", 'r') as file:
        mapper = yaml.safe_load(file)

    mapper['mapper']['timeout'] = main_mapper_pars[0]
    mapper['mapper']['victory-condition'] = main_mapper_pars[1]

    with open(DIR + "mapper/mapper.yaml", 'w') as file:
        yaml.dump(mapper, file)


def fusion_main_sim(DIR):

    MAIN_DIR = DIR + "main_computations/"
    fix_main_mapper(MAIN_DIR)
    for block in range(F_BLOCKS):
        MAIN_BLOCK_DIR = MAIN_DIR + "b"  + str(block+1) + "/"

        if block != 0:
            if os.path.isfile(MAIN_DIR + 'b'+str(block+1)):
                subprocess.run(['rm', '-rf', MAIN_DIR + 'b'+str(block+1)])
            subprocess.run(['cp', '-r', MAIN_DIR+ 'b'+str(block), MAIN_DIR + 'b'+str(block+1)])

        fix_block_shape_main(MAIN_BLOCK_DIR, block)
        fix_block_constraints_main(MAIN_BLOCK_DIR, block)

        p = subprocess.Popen(['timeloop-mapper', './../accelerator/fusion/main/arch.yaml',\
                     './../accelerator/fusion/main/components/smartbuffer_RF.yaml', './../accelerator/fusion/main/components/smartbuffer_SRAM.yaml',\
                     MAIN_DIR+'mapper/mapper.yaml', MAIN_BLOCK_DIR+'prob/prob.yaml', MAIN_BLOCK_DIR+'constraints/constraints.yaml',\
                     '-o', MAIN_BLOCK_DIR+'output'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            time.sleep(3)
            p.communicate(input="a")
            if p.poll() != None:
                break

        print("block ", block+1, "of main computations simulations")
        time.sleep(3)
#****************************************************************************************************
#****************************************************************************************************



def fusion_sim():
    DIR = "./fusion/"
    #fusion_pred_sim(DIR)
    fusion_main_sim(DIR)



def sim(CSV_only, delay, main_mapper, pred_mapper, pred_dw_mapper, pes, xpes, spatial_x, spatial_y, blocks,\
        in_ch, midd_ch, out_ch, pixels, stride, adders, prune_factors, pred1_qtz, pred2_qtz, pred_qtz, q_blocks):

    global DELAY, main_mapper_pars, pred_mapper_pars, pred_dw_mapper_pars,\
           F_PEs, X_PEs, PRED_SPATIAL_GLB, PRED_SPATIAL_DUMMY,\
           F_BLOCKS, f_in_ch, f_midd_ch, f_out_ch, f_pixels, f_stride

    DELAY = delay
    main_mapper_pars = main_mapper
    pred_mapper_pars = pred_mapper
    pred_dw_mapper_pars = pred_dw_mapper

    F_PEs = pes
    X_PEs = xpes
    PRED_SPATIAL_GLB = spatial_x
    PRED_SPATIAL_DUMMY = spatial_y

    F_BLOCKS = blocks
    f_in_ch   = in_ch
    f_midd_ch = midd_ch
    f_out_ch = out_ch
    f_pixels = pixels
    f_stride = stride

    if not CSV_only:
        fusion_sim()
    fusion.make_csv(F_BLOCKS, F_PEs, adders, f_in_ch, f_midd_ch, f_out_ch, f_pixels,\
                    f_stride, prune_factors, pred1_qtz=pred1_qtz, pred2_qtz=pred2_qtz, pred_qtz=pred_qtz, q_blocks=q_blocks)
