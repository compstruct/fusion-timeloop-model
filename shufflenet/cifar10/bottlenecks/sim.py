import time
import Sim.bl_sim as bl_sim
import Sim.f_sim as f_sim
import ResMaker.combined as csvmaker

#*****Configurations********
#simulator configs
DELAY = 60
simulate_bl = False
bl_sparse_only = False
simulate_fusion = True
CSV_ONLY = False

bl_mapper = [50000, 1000]
bl_dwmapper = [10000, 400]
#baseline acc. config
BL_PEs = 72
#baseline CNN configs
BL_BLOCKS = 15
BL_GROUPS = 3
bl_in_ch   = [24] + [60] * 4 + [120] * 8 + [240] * 2
bl_midd_ch = [240] * 4 + [480] * 8 + [960] * 3
bl_out_ch = [60] * 4 + [120] * 8 + [240] * 3
bl_pixels = [32] * 3 + [16] * 8 + [8] * 4
bl_stride =  [1] * 3 + [2] + [1] * 7 + [2] + [1] * 3

F_BLOCKS = 15
qtz_blocks = F_BLOCKS + 1

pred1_qtz = True
pred2_qtz = True
qtz = [4]*4 + [4]*(qtz_blocks-4)

f_mapper = [50000, 1000]
f_dw_mapper = [10000, 400]
f_main_mapper = [5000, 400]

#fusion acc. config
F_PEs = 64
X_PEs = 8
PRED_SPATIAL_GLB = {'decom':'N=1 R=1 S=1 ', 'comp':'N=1 R=1 S=1'}
PRED_SPATIAL_DUMMY = {'decom':'N=1 R=1 S=1 ', 'comp':'N=1 R=1 S=1'}

PER_PE_ADDERS = 6
ADDERS = PER_PE_ADDERS * 4

#Fusion CNN configs
F_BLOCKS = 15
F_GROUPS = 3
f_in_ch   = [24] + [18] * 2 + [24] * 4 + [42] * 8
f_midd_ch = [2574] * 7 + [2604] * 8
f_out_ch = [18] * 2 + [24] * 4 + [42] * 8 + [84]
f_pixels = [32] * 2 + [16] * 4 + [8] * 9
f_stride = [1] * 2 + [2] + [1] * 3 + [2] + [1] * 8

prune_factors = [0.01]*15

sim_begin_time = time.time()

print("Simulation begins")


#if not CSV_ONLY:
if simulate_bl:
    bl_sim.sim(CSV_ONLY, DELAY, bl_mapper, bl_dwmapper, BL_BLOCKS, BL_GROUPS, bl_in_ch, bl_midd_ch, bl_out_ch, bl_pixels, bl_stride, bl_sparse_only)
if simulate_fusion:
    f_sim.sim(CSV_ONLY, DELAY, f_main_mapper, f_mapper, f_dw_mapper, F_PEs, X_PEs, PRED_SPATIAL_GLB, PRED_SPATIAL_DUMMY,\
          F_BLOCKS, F_GROUPS, f_in_ch, f_midd_ch, f_out_ch, f_pixels, f_stride, ADDERS, prune_factors, pred1_qtz, pred2_qtz, qtz, qtz_blocks)
csvmaker.make_combined_csv(groups=F_GROUPS)


sim_end_time = time.time()
print("simulation took", sim_end_time - sim_begin_time)
