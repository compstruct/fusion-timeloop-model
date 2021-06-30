import numpy as np
import sys
import pandas
import os
import subprocess
import time
import yaml
import ResMaker.baseline as baseline

#Simulator configs
DELAY = 10
mapper_pars = []
dw_mapper_pars = []
#baseline CNN configs
BL_BLOCKS = 0
bl_in_ch   = []
bl_midd_ch = []
bl_out_ch = []
bl_pixels = []
bl_stride = []






def run_timeloop(DIR, LAYER_DIR, dw=False):
    if dw==True:
        mapper = DIR+'dw_mapper/mapper.yaml'
    else:
        mapper = DIR+'mapper/mapper.yaml'

    p = subprocess.Popen(['timeloop-mapper', './../accelerator/baseline/arch.yaml', './../accelerator/baseline/components/smartbuffer_RF.yaml', './../accelerator/baseline/components/smartbuffer_SRAM.yaml',\
                     mapper, LAYER_DIR+'prob/prob.yaml', LAYER_DIR+'constraints/arch_constraints.yaml',\
                     LAYER_DIR+'constraints/map_constraints.yaml', '-o', LAYER_DIR+'output'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        time.sleep(3)
        p.communicate(input="a")
        if p.poll() != None:
            break


def fix_layer_shape(BLOCK_DIR, layer, block):

    global bl_in_ch, bl_midd_ch, bl_out_ch, bl_pixels, bl_stride

    with open(BLOCK_DIR + layer + "/prob/prob.yaml", 'r') as file:
        prob = yaml.safe_load(file)

    if layer == 'conv':
        prob['problem']['instance']['M'] = bl_midd_ch[block]
        prob['problem']['instance']['Wstride'] = bl_stride[block]
        prob['problem']['instance']['Hstride'] = bl_stride[block]

    elif layer == 'decom':
        prob['problem']['instance']['C'] = bl_in_ch[block]
        prob['problem']['instance']['M'] = bl_midd_ch[block]

    else:
        prob['problem']['instance']['C'] = bl_midd_ch[block]
        prob['problem']['instance']['M'] = bl_out_ch[block]

    if layer == 'decom':
        prob['problem']['instance']['P'] = bl_pixels[block] * bl_stride[block]
        prob['problem']['instance']['Q'] = bl_pixels[block] * bl_stride[block]
    else:
        prob['problem']['instance']['P'] = bl_pixels[block]
        prob['problem']['instance']['Q'] = bl_pixels[block]

    with open(BLOCK_DIR + layer + "/prob/prob.yaml", 'w') as file:
        yaml.dump(prob, file)


def fix_block_shape(BLOCK_DIR, block):
    fix_layer_shape(BLOCK_DIR, 'decom', block)
    fix_layer_shape(BLOCK_DIR, 'conv', block)
    fix_layer_shape(BLOCK_DIR, 'comp', block)



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



def dense_baseline_sim():

    DIR = "./baseline/"
    fix_mapper(DIR)

    for block in range(BL_BLOCKS):

        if block != 0:
            if os.path.isfile(DIR + 'b'+str(block+1)):
                subprocess.run(['rm', '-rf', DIR + 'b'+str(block+1)])
            subprocess.run(['cp', '-r', DIR + 'b'+str(block), DIR + 'b'+str(block+1)])


        BLOCK_DIR = DIR + "b"  + str(block+1) + "/"
        fix_block_shape(BLOCK_DIR, block)

        t1 = time.time()
        run_timeloop(DIR, BLOCK_DIR+"decom/")
        t2 = time.time()
        print("baseline simulation" + "pw1 of block " + str(block+1) + " and it took", t2-t1)
        time.sleep(3)

        t1 = time.time()
        run_timeloop(DIR, BLOCK_DIR+"conv/", dw=True)
        t2 = time.time()
        print("baseline simulation" + "dw of block " + str(block+1) + " and it took", t2-t1)
        time.sleep(3)

        t1 = time.time()
        run_timeloop(DIR, BLOCK_DIR+"comp/")
        t2 = time.time()
        print("baseline simulation" + "pw2 of block " + str(block+1) + " and it took", t2-t1)
        time.sleep(3)



def sparse_baseline_sim():
    os.chdir("sparse_baseline")
    p = subprocess.Popen(['rm', 'csvs/*', 'convert_comp.py', 'convert_decomp.py', 'convert_conv.py', 'temp_91.csv', 'temp.csv'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()
    print("runing sparse baseline simulatons")
    #subprocess.run(['./gen_py.sh'])
    #subprocess.run(['python3', 'analyze_layers.py'])
    p = subprocess.Popen(['./gen_py.sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()
    p = subprocess.Popen(['python3', 'analyze_layers.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.wait()
    print("finished sparse baeline simulations")
    os.chdir("..")




def sim(delay, mapper, dw_mapper, blocks, in_ch, midd_ch, out_ch, pixels, stride, CSV_only, sparse_only):

    global DELAY, mapper_pars, dw_mapper_pars
    global BL_BLOCKS
    global bl_in_ch, bl_midd_ch, bl_out_ch, bl_pixels, bl_stride

    DELAY = delay
    mapper_pars = mapper
    dw_mapper_pars = dw_mapper
    BL_BLOCKS = blocks
    bl_in_ch   = in_ch
    bl_midd_ch = midd_ch
    bl_out_ch = out_ch
    bl_pixels = pixels
    bl_stride = stride
    if not CSV_only:
        if not sparse_only:
            dense_baseline_sim()
        sparse_baseline_sim()
    baseline.make_csv(BL_BLOCKS, "./baseline/", bl_midd_ch)
