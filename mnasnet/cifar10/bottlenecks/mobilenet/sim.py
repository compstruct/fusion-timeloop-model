import time
import Sim.bl_sim as bl_sim
import Sim.f_sim as f_sim
import ResMaker.combined as csvmaker
#*****Configurations********
#simulator configs
DELAY = 60

CSV_ONLY = False

simulate_bl = True
sparse_bl_only = True

simulate_fusion = False

bl_mapper = [50000, 1000]
bl_dwmapper = [10000, 300]

f_mapper = [50000, 1000]
f_dw_mapper = [10000, 300]
f_main_mapper = [5000, 400]


#baseline acc. config
BL_PEs = 72
#baseline CNN configs
BL_BLOCKS = 16
bl_in_ch   = [16] + [24] * 2 + [32] * 3 + [64] * 4 + [96] * 3 + [160] * 3
BL_EXPANSION = 6
bl_midd_ch = []
for i in range(BL_BLOCKS):
    bl_midd_ch.append(bl_in_ch[i] * BL_EXPANSION)
bl_out_ch = [24] * 2 + [32] * 3 + [64] * 4 + [96] * 3 + [160] * 3 +[320]
bl_pixels = [32] * 5 + [16] * 6 + [8] * 5
bl_stride = [1] * 5 + [2] + [1] * 5 + [2] + [1] * 4



#fusion acc. config
F_PEs = 64
X_PEs = 8
PRED_SPATIAL_GLB = {'decom':'N=1 R=1 S=1 P=1 Q=8 M=1 C=1', 'conv':'N=1 R=1 S=1 P=1 C=1 Q=4 M=2'}
PRED_SPATIAL_DUMMY = {'decom':'N=1 R=1 S=1 P=1 Q=1 C=1 M=8', 'conv':'N=1 R=1 S=1 P=1 C=1 Q=1 M=8'}
ADDERS = 20
PRED1_QTZ = False
PRED2_QTZ = True
PRED_QTZ = 3
Q_BLOCKS = 15  #up to what block uses quantized prediction
#Fusion CNN configs
F_BLOCKS = 14
f_in_ch   = [16] + [24] * 3 + [32] * 4 + [40] * 6
f_midd_ch = [864] * F_BLOCKS
f_out_ch = [24] * 3 + [32] * 4 + [40] * 6 + [80]
f_pixels = [32] * 3 + [16] * 4 + [8] * 7
f_stride = [1] * 3 + [2] + [1] * 3 + [2] + [1] * 6

prune_factors = [0.01]*14

sim_begin_time = time.time()

print("Simulation begins")

if simulate_bl:
    bl_sim.sim(DELAY, bl_mapper, bl_dwmapper, BL_BLOCKS, bl_in_ch, bl_midd_ch, bl_out_ch, bl_pixels, bl_stride, CSV_ONLY, sparse_bl_only)
if simulate_fusion:
    f_sim.sim(CSV_ONLY, DELAY, f_main_mapper, f_mapper, f_dw_mapper, F_PEs, X_PEs, PRED_SPATIAL_GLB, PRED_SPATIAL_DUMMY,\
          F_BLOCKS, f_in_ch, f_midd_ch, f_out_ch, f_pixels, f_stride, ADDERS, prune_factors, PRED1_QTZ, PRED2_QTZ, PRED_QTZ, Q_BLOCKS)

sim_end_time = time.time()
print("simulation took", sim_end_time - sim_begin_time)

csvmaker.make_combined_csv()
