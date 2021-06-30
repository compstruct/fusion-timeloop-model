from ResMaker.Package.Utils import *

#Global fmap buffer
prediction_glb_actions = [[None,'idle'], [addr_data(0,0),'write'], [addr_data(0,1),'write'], [addr_data(1,0),'write'], [addr_data(1,1),'write'],\
                    [addr_data(0,0),'read'], [addr_data(0,1),'read'], [addr_data(1,0),'read'], [addr_data(1,1),'read']]

and_gate_actions = [[None,'idle'], [None,'process']]

#***********************************************************************************************
#PE local buffers
weight_buffer_actions = [[None,'idle'], [addr_data(0,0),'write'], [addr_data(0,1),'write'], [addr_data(1,0),'write'], [addr_data(1,1),'write'],\
                    [addr_data(0,0),'read'], [addr_data(0,1),'read'], [addr_data(1,0),'read'], [addr_data(1,1),'read']]

weigth_indices_actions = [[None,'idle'], [addr_data(0,0),'write'], [addr_data(0,1),'write'], [addr_data(1,0),'write'], [addr_data(1,1),'write'],\
                    [addr_data(0,0),'read'], [addr_data(0,1),'read'], [addr_data(1,0),'read'], [addr_data(1,1),'read']]

prediction_buffer_actions = [[None,'idle'], [addr_data(0,0),'write'], [addr_data(0,1),'write'], [addr_data(1,0),'write'], [addr_data(1,1),'write'],\
                    [addr_data(0,0),'read'], [addr_data(0,1),'read'], [addr_data(1,0),'read'], [addr_data(1,1),'read']]

adders_actions = [[None,'idle'], [None,'add']]

#Index Aliases into the action lists
action_write  = 4
action_read = 8
action_bitwise = 1
action_Add = 1
action_Buffer = 6
action_mac_random = 1
action_process = 1
