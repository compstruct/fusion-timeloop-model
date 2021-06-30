import pandas as pd
import numpy as np

DEBUG = True

network_head = {
  'baseline' : "head_and_tail/baseline/bl_head/results/bl.csv",
  #'fused' : "head_and_tail/fused/fus_head/results/bl.csv",  no fused version for Cifar100
}

bottlenecks = "bottlenecks/results/res.csv"
bottlenecks_columns = 16

network_tail = {
  'baseline' : "head_and_tail/baseline/bl_tail/results/bl.csv",
  #'fused' : "head_and_tail/fused/fus_tail/results/bl.csv",   no fused version for Cifar100
}

head_bl = pd.read_csv(network_head["baseline"])
#head_fus = pd.read_csv(network_head["fused"])
bn = pd.read_csv(bottlenecks)
tail_bl = pd.read_csv(network_tail["baseline"])
#tail_fus = pd.read_csv(network_tail["fused"])


bn_names = bn["block"].tolist()[:bottlenecks_columns]
for i, name in enumerate(bn_names):
  bn_names[i] = "b"+str(name)

col0 = head_bl["1_block"].tolist() + bn_names + tail_bl["1_block"].tolist()

col1 = head_bl["2_energy"].tolist() + bn["1_PW1_e"].tolist()[:bottlenecks_columns] + tail_bl["2_energy"].tolist()
col2 = ['0']*len(head_bl["2_energy"].tolist()) +  bn["2_DW_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["2_energy"].tolist())
col3 = ['0']*len(head_bl["2_energy"].tolist()) +  bn["3_PW2_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["2_energy"].tolist())

col4 = head_bl["3_cycles"].tolist() + bn["4_PW1_c"].tolist()[:bottlenecks_columns] + tail_bl["3_cycles"].tolist()
col5 = ['0']*len(head_bl["3_cycles"].tolist()) +  bn["5_DW_c"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["3_cycles"].tolist())
col6 = ['0']*len(head_bl["3_cycles"].tolist()) +  bn["6_PW2_c"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["3_cycles"].tolist())

col7 = head_bl["2_energy"].tolist() + bn["sparse_PW1_e"].tolist()[:bottlenecks_columns] + tail_bl["2_energy"].tolist()
col8 = ['0']*len(head_bl["2_energy"].tolist()) +  bn["sparse_DW_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["2_energy"].tolist())
col9 = ['0']*len(head_bl["2_energy"].tolist()) +  bn["sparse_PW2_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["2_energy"].tolist())

col10 = head_bl["3_cycles"].tolist() + bn["sparse_PW1_C"].tolist()[:bottlenecks_columns] + tail_bl["3_cycles"].tolist()
col11 = ['0']*len(head_bl["3_cycles"].tolist()) +  bn["sparse_DW_C"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["3_cycles"].tolist())
col12 = ['0']*len(head_bl["3_cycles"].tolist()) +  bn["sparse_PW2_C"].tolist()[:bottlenecks_columns] + ['0']*len(tail_bl["3_cycles"].tolist())

"""
col13 = ['0']*len(head_fus["2_energy"].tolist()) +  bn["1_pred_decom_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_fus["2_energy"].tolist())
col14 = ['0']*len(head_fus["2_energy"].tolist()) +  bn["2_pred_conv_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_fus["2_energy"].tolist())
col15 = head_fus["2_energy"].tolist() +  bn["3_main_e"].tolist()[:bottlenecks_columns] + tail_fus["2_energy"].tolist()
col16 = ['0']*len(head_fus["2_energy"].tolist()) +  bn["4_overhead_e"].tolist()[:bottlenecks_columns] + ['0']*len(tail_fus["2_energy"].tolist())

col17 = ['0']*len(head_fus["3_cycles"].tolist()) +  bn["5_pred_decom_c"].tolist()[:bottlenecks_columns] + ['0']*len(tail_fus["3_cycles"].tolist())
col18 = ['0']*len(head_fus["3_cycles"].tolist()) +  bn["6_pred_conv_c"].tolist()[:bottlenecks_columns] + ['0']*len(tail_fus["3_cycles"].tolist())
col19 = head_fus["3_cycles"].tolist() +  bn["7_main_c"].tolist()[:bottlenecks_columns] + tail_fus["3_cycles"].tolist()
"""

if DEBUG:
  print(len(col0))
  print(len(col1))
  print(len(col2))
  print(len(col3))
  print(len(col4))
  print(len(col5))
  print(len(col6))
  print(len(col7))
  print(len(col8))
  print(len(col9))
  print(len(col10))
  print(len(col11))
  print(len(col12))
  #print(len(col13))
  #print(len(col14))
  #print(len(col15))
  #print(len(col16))
  #print(len(col17))
  #print(len(col18))
  #print(len(col19))




data = {
  'layer' : col0,
  'PW1/L1_e' : col1,
  'PW2_e' : col2,
  'PW3_e' : col3,
  'PW1/L1_c' : col4,
  'PW2_c' : col5,
  'PW3_c' : col6,
  'sparse_PW1/L1_e' : col7,
  'sparse_PW2_e' : col8,
  'sparse_PW3_e' : col9,
  'sparse_PW1_c' : col10,
  'sparse_DW_c' : col11,
  'sparse_PW2_c' : col12,
  #'pred_decom_e' : col13,
  #'pred_conv_e' : col14,
  #'main_e' : col15,
  #'overhead_e' : col16,
  #'pred_decom_c' : col17,
  #'pred_conv_c' : col18,
  #'main_c' : col19
}

final_df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
final_df.to_csv('result.csv')
