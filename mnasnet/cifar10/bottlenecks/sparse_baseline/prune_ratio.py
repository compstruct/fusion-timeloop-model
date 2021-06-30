import numpy as np
import tensorflow as tf


model = tf.keras.models.load_model("./../../pruned_25/pruned_25.h5")
layers = model.layers
#model.summary()

ii = 0
i = 0
conv_number = 0
depthwise_number = 0
dense_number = 0
for layer in layers:
    if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        tmp = layer.get_weights()[0]
        mask =  np.absolute(tmp) !=0
        prune_ratio = np.sum(mask) / np.size(tmp)
        print("depthwise_" + str(depthwise_number) + " : " + str(prune_ratio))
        print(tmp.shape)
        depthwise_number += 1
    elif isinstance(layer, tf.keras.layers.Conv2D):
        if layer.name != "conv2d" and layer.name != "conv2d_35":
            i += 1
            if i%2 == 1:
              print("\n*** block" + str(i//2) + "***")
        tmp = layer.get_weights()[0]
        mask =  np.absolute(tmp) !=0
        prune_ratio = np.sum(mask) / np.size(tmp)
        print("conv_" + str(conv_number) + " : " + str(prune_ratio))
        print(tmp.shape)
        conv_number += 1
    elif isinstance(layer, tf.keras.layers.Dense):
        tmp = layer.get_weights()[0]
        mask =  np.absolute(tmp) !=0
        prune_ratio = np.sum(mask) / np.size(tmp)
        print("dense_" + str(dense_number) + " weight : " + str(prune_ratio))
        print(tmp.shape)
        tmp = layer.get_weights()[1]
        mask =  np.absolute(tmp) !=0
        prune_ratio = np.sum(mask) / np.size(tmp)
        print("dense_" + str(dense_number) + "bias : " + str(prune_ratio))
        print(tmp.shape)
        dense_number += 1

