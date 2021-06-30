import time
import sim.simulator as simulator

#import ResMaker.combined as csvmaker
#*****Configurations********
#simulator configs

#Debug print statements
debug_print_model = True
debug_timeloop_output = True

SIMULATE = True
CSV_ONLY = False

mapper = [50000, 1000]
dwmapper = [10000, 300]


#baseline acc. config
PEs = 72
#CNN configs*****************

batch_size = 1
descriptions = ["pw"] + ["FC"]
BLOCKS = len(descriptions)
names = []
conv_i = pw_i = dw_i = ave_pool_i = fc_i = 1
for desc in descriptions:
    if desc == "conv":
        names.append("conv"+str(conv_i))
        conv_i += 1
    elif desc == "FC":
        names.append("FC"+str(fc_i))
        fc_i += 1
    elif desc == "pw":
        names.append("PW"+str(fc_i))
        pw_i += 1

pixels = [8, 1]
stride = [1, 1]

in_ch   = [320, 1280]
out_ch = [1280, 10]

#*****************************

if debug_print_model == True:
    for i in range(BLOCKS):
        print("Name: " + names[i]  + "    type: " + descriptions[i] + "  in_ch= " + str(in_ch[i]) +\
              "   out_ch= " + str(out_ch[i]) + "   pixels= " + str(pixels[i]) + "   stride= " + str(stride[i]))

sim_begin_time = time.time()
print("Simulation begins")

if SIMULATE:
    simulator.simulate(debug_timeloop_output, mapper, dwmapper,\
                       BLOCKS, in_ch, out_ch,\
                       pixels, stride, batch_size, descriptions,\
                       names, CSV_ONLY)

sim_end_time = time.time()
print("simulation took", sim_end_time - sim_begin_time)
