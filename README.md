## Abstract

Many modern convolutional neural neworks (CNNs) rely on bottleneck block structures where the activation tensor is mapped between higher dimensions using an intermediate low dimension, and convolved with depthwise feature filters rather than multi-channel filters. Because most of the computation lies in computing the large dimensional tensors, however, such networks cannot be scaled without significant computation costs.

In this paper, we show how \emph{fusing} the layers inside these blocks can dramatically reduce the multiplication count (by 6--20x) at the cost of extra additions. ReLU nonlinearities are predicted dynamically, and only the activations that survive ReLU contribute to directly compute the output of the block. We also propose FusioNet, a CNN architecture optimized for fusion, as well as ARCHON, a novel accelerator design with a dataflow optimized for fused networks.

When FusioNet is executed on the proposed accelerator, it yields up to 5.8x faster inference compared to compact networks executed on a dense DNN accelerator, and 2.1x faster inference compared to the same networks when pruned and executed on a sparse DNN accelerator.

## Paper Link

[Accelerating DNNs Inference with Predictive Layer Fusion, in ICS'21](https://dl.acm.org/doi/10.1145/3447818.3460378)


## Requirements

The simulator is based on [Timeloop](https://github.com/NVlabs/timeloop). Please install [Timeloop](https://github.com/NVlabs/timeloop) and [Accelergy](https://github.com/Accelergy-Project/accelergy) using the guidelines provided on their pages.

You also need TensorFlow version 2.3.0 installed. Lastly, you will need Pandas and Numpy.


## Overview

We performed our experiments on two datasets, CIFARF10 and 100. We also used 3 accelerators:
* A baseline accelerator similar to Eyeriss
* An enhanced version of Eyeriss that supports sparse acceleration
* Archon, the accelerator that we introduced in our paper.



## Running Experiments

### Organization

Experiments are organized in terms of network and dataset. Each network in our experiments consists of a:
* head (usually a convolution with 3 channels and 24 to 32 filters)
* bottleneck body (sequence of bottleneck blocks)
* tail (a pointwise or regular convolution and a fully connected layer)
 
Figure below shows a part of the overall organization of directories.
```
fusion_sim
????????? mobilenet
|    ????????? cifar10
|    |       ????????? head_and_tail
|    |       |      ????????? fused
|    |       |      |       ????????? head
|    |       |      |       ????????? tail
|    |       |      ????????? baseline           
|    |       ????????? bottlenecks
|    ????????? cifar100
|            ????????? head_and_tail
|            |      ????????? baseline           
|            ????????? bottlenecks
.          
.    
????????? acceletrator
????????? area
```

### Running the Simulator

Simulating a network is possible by running the simulation for bottleneck sequence, head and tail. For example, to simulate execution of bottlenecks for MobileNetv2 & cifar10, go to the directory "cifar10/mobilenet/bottlenecks". The main source file is `sim.py` which has the description for both original and modified CNNs in it. It also has the following variables:
* *simulate_bl* : whether to run the simulation for baseline network on the baseline accelerators
* *sparse_bl_only* : only perform the sparse baseline simulator (if *simulate_bl* is True)
* *simulate_fusion* : whether to run the simulation for modified network on Archon accelerator
* *CSV_ONLY* : If True, only CSV will be generated from the reuslt of previous runs

Running the `sim.py` inside bottlenecks generate a csv file, `res.csv`, which contains the stats. We can similarly do this for the head and tail  of the network (separately for baseline and modified networks) to get the full network execution simulation. Once bottlenecks, heads and tails have been simulated, one can run the `make_result.py` to generate a single csv containing cycle and energy stats for the modified and baseline networks on the 3 accelerators.


## Details
### CSV files
Here we explain some examples of the columns you will see in the CSV files:
* layer: layer or block name
* PW1/L_e: first pointwise layer (in case of bottlenecks) or layer (in case of regular layers) energy on dense baseline accelerator.
* DW_e: energy for a depthwise layer in a bottleneck on dense baseline accelerator.
* PW1/L_c: first pointwise layer (in case of bottlenecks) or layer (in case of regular layers) cycles on dense baseline accelerator.
* sparse_PW2_e: energy for the second depthwise layer in a bottleneck on sparse baseline accelerator.
* pred_decom_e: energy for predicting pw1 layer (decompression) of a bottleneck block on Archon
* pred_conv_e: energy for predicting dw layer (convolution) of a bottleneck block on Archon
* main_e: energy for main fused convolution on Archon
* overhead_e: energy overhead for fusion 
* pred_conv_c: cycles for predicting dw layer (convolution) of a bottleneck block on Archon
* main_c: cycles for main fused convolution on Archon
 

### How does simulator work?
The simulator runs timeloop sequentially for each layer described in `sim.py`. Once all the layers have been simulated, it will extract the stats and dump them as a `.csv` file.

For sparsity support, simulator uses a pruned TensorFlow model (`.h5` file) and the result of dense baseline simulations. It reduces the cycles based on the slowest PE in each processing pass (i.e. due to workload imbalance found in model) and energy based on the sparsity of layer.
