import numpy as np
import tensorflow as tf
from convert_comp import *
from convert_decomp import *
from convert_conv import *

SPARSITY=0.80
FILENAME="./tf_model/post_prune.h5"

# check sparsity and filename quickly
#if FILENAME.find(str(SPARSITY).split(".")[1].strip()) < 0:
#        print("Check File Name and sparsity")
#        quit()

model = tf.keras.models.load_model(FILENAME)
layers = model.layers
#model.summary()
g = open("./../results/sparse_bl_res.csv".format(int(SPARSITY*100)), "w")

i = 0
conv_number = 0
depthwise_number = 0
dense_number = 0

RAW_DUMP=1

g.write("Block,R,S,C,M,PEs,iter,MACs/iter,Dense MACs,Sparse MACs,Dense MAC Cycles,Best Sparse MAC Cycles,Sparse MAC Cycles\n")

for layer in layers:
    if isinstance(layer,tf.keras.layers.DepthwiseConv2D) or isinstance(layer, tf.keras.layers.Conv2D):
        blk_num = int( (i-1) /3)
        print("Blk {} - {} - {}".format(blk_num, layer.name, layer.get_weights()[0].shape))

        # (i -1)%3 == 1 are depthwise layers, so ignore
        if blk_num > 16 or blk_num < 1:
            i += 1
            continue

        # decomp layer
        if (i-1) % 3 == 0:
            worktiles = decomp_worktiles(layer.get_weights()[0], blk_num)
        # comp layer
        elif (i-1) % 3 == 2:
            worktiles = comp_worktiles(layer.get_weights()[0], blk_num)
        elif (i-1) % 3 == 1:
            worktiles = conv_worktiles(layer.get_weights()[0], blk_num)
        else:
            i += 1
            continue

        for k,v in worktiles.items():
            if len(v) != len(worktiles[(0,0)]):
                print("ERROR")
                quit()
        print("\t{} PEs, {} iterations, {} MACs per iteration".format(len(worktiles.keys()), len(worktiles[(0,0)]), len(worktiles[(0,0)][0])))

        if RAW_DUMP:
            if (i-1) % 3 == 1:
                h = open("./csvs/{}_conv_raw_{}.csv".format(blk_num, int(SPARSITY*100)), "w")
            else:
                h = open("./csvs/{}_{}comp_raw_{}.csv".format(blk_num, "de" if i % 7 == 0 else "", int(SPARSITY*100)), "w")

            h.write("PE,")

            for it in range(len(worktiles[(0,0)])):
                h.write("{},".format(it))
            h.write("\n")
            for k, v in worktiles.items():
                h.write("{},".format(str(k).replace(",", "-")))
                for w in v:
                    h.write("{},".format(np.sum(np.absolute(w) != 0)))
                h.write("\n")

        dense_macs = 0
        sparse_macs_t = 0
        sparse_mac_cycles = 0

        for k, v in worktiles.items():
            dense_macs += sum([len(x) for x in v])
            sparse_macs_t += np.sum(np.absolute(v) != 0)

        for it in range(len(worktiles[(0,0)])):
            sparse_mac_cycles += max([np.sum(np.absolute(worktiles[x][it]) != 0) for x in worktiles.keys()])

        if RAW_DUMP:
            h.close()

        print("\t{} MACs (Dense), {} MACs (Sparse)".format(dense_macs, sparse_macs_t))
        print("\t{} Dense MAC cycles".format(int(dense_macs/len(worktiles.keys()))))
        print("\t~{} Theoretical MAC cycles".format(int((sparse_macs_t/dense_macs)*dense_macs/len(worktiles.keys()))))
        print("\t{} Actual MAC cycles".format(sparse_mac_cycles))
        g.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(blk_num, layer.get_weights()[0].shape[0],\
          layer.get_weights()[0].shape[1], layer.get_weights()[0].shape[2], layer.get_weights()[0].shape[3], \
                                     len(worktiles.keys()), len(worktiles[(0,0)]), len(worktiles[(0,0)][0]), \
                                            dense_macs, sparse_macs_t, int(dense_macs/len(worktiles.keys())),\
                        int((sparse_macs_t/dense_macs)*dense_macs/len(worktiles.keys())), sparse_mac_cycles))
        i += 1

    #if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
    #    blk_num = int(i/7)
    #    print("Blk {} - {} - {}".format(blk_num, layer.name, layer.get_weights()[0].shape))
    #    i += 1



g.close()
