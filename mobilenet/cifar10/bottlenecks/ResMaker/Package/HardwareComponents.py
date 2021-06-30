from ResMaker.Package.ActionCount import *
from ResMaker.Package.Actions import *
import copy
from math import ceil


class HardwareComponent(action_counts):
    def __init__(self, name, actions):
        super().__init__(name)
        self.add_actions(actions)

    def add_action(self, args):
        super().add_action(arguments=args[0], name=args[1])

    def add_actions(self, actions):
        for action in copy.deepcopy(actions):
            self.add_action(action)


class SRAM(HardwareComponent):
    def __init__(self, name, size, bandwidth, n_banks, n_ports, actions):
        self.bandwidth = bandwidth
        self.n_banks = n_banks
        self.n_ports = n_ports
        self.size = size
        super().__init__(name, actions)


class RegFile(HardwareComponent):
    def __init__(self, name, size, bandwidth, n_banks, n_ports, actions):
        self.bandwidth = bandwidth
        self.n_banks = n_banks
        self.n_ports = n_ports
        self.size = size
        super().__init__(name, actions)


class Adders(HardwareComponent):
    def __init__(self, name, bandwidth, actions):
        self.bandwidth = bandwidth
        super().__init__(name, actions)


class Bitwise(HardwareComponent):
    def __init__(self, name, bandwidth, actions):
        self.bandwidth = bandwidth
        super().__init__(name, actions)


class PE:

    def __init__(self, name, components_names):
        self.sub_components_names = components_names
        self.sub_components = []
        self.name = name

        ##_____________ PE Components ___________##
        #pred spad
        self.prediction_buffer = SRAM(name=name+self.sub_components_names[len(self.sub_components)], size=0, bandwidth=8, n_banks=4, n_ports=2, actions=prediction_buffer_actions)
        self.sub_components.append(self.prediction_buffer)

        #fusion unit
        self.adders = Adders(name=name+self.sub_components_names[len(self.sub_components)], bandwidth=64, actions=adders_actions)
        self.sub_components.append(self.adders)

        self.bit_masks_and  = Bitwise(name=name+self.sub_components_names[len(self.sub_components)], bandwidth=8, actions=and_gate_actions)
        self.sub_components.append(self.bit_masks_and)

        self.mux_ = Bitwise(name=name+self.sub_components_names[len(self.sub_components)], bandwidth=8, actions=and_gate_actions)
        self.sub_components.append(self.mux_)

        self.mux = Bitwise(name=name+self.sub_components_names[len(self.sub_components)], bandwidth=16, actions=and_gate_actions)
        self.sub_components.append(self.mux)

        self.components_dict = {}
        for component in self.sub_components_names:
            self.components_dict[component] = self.sub_components[self.sub_components_names.index(component)]

    def get_dict(self):
        dicts = []
        for i in range(len(self.sub_components)):
            component = self.sub_components[i]
            dicts.append(component.get_dict())
        return dicts

    def inc_action_count(self, sub_component, action, count):
         component = self.components_dict.get(sub_component)
         component.inc_action(action, count)



    def process_layer(self, layer, cycles, total_PE, PE_adders):

        prediction_buffer_writes = ceil(layer['midd_ch'] / self.prediction_buffer.bandwidth) * ceil((layer['pixels']**2)/total_PE) * 9
        prediction_buffer_reads =  (PE_adders)  * cycles

        self.prediction_buffer.inc_action(action_write, prediction_buffer_writes)
        self.prediction_buffer.inc_action(action_read, prediction_buffer_reads)

        total_adds = ceil(PE_adders * cycles)
        self.adders.inc_action(action_Add, total_adds)

        total_bit_masks = ceil(PE_adders * cycles)
        self.bit_masks_and.inc_action(1, total_bit_masks)

        total_mux_ = ceil(PE_adders * cycles)
        self.mux_.inc_action(1, total_mux_)


        total_mux = ceil(PE_adders * 2 * cycles)
        self.mux.inc_action(1, total_mux)


class Chip:

    def __init__(self, name, total_PE, PE_components):
        self.name = name
        self.total_PE = total_PE
        self.prediction_glb = SRAM(name=self.name+'pred_glb', size=0, bandwidth=64, n_banks=2, n_ports=1, actions=prediction_glb_actions)
        self.global_AND_gate = Bitwise(name=self.name+'binary_decoder', bandwidth=64, actions=and_gate_actions)
        self.PEs = []
        for PE_number in range(self.total_PE):
            self.PEs.append(PE(name=self.name+'PE['+str(PE_number) +']', components_names=PE_components))

    def process(self, layer, cycles, outer_M, PE_adders):
        prediction_glb_writes = ceil( (layer['midd_ch'] * ((layer['pixels'])*(layer['pixels'])) )/self.prediction_glb.bandwidth)*2
        prediction_glb_reads = prediction_glb_writes
        self.prediction_glb.inc_action(action_write, prediction_glb_writes)
        self.prediction_glb.inc_action(action_read, prediction_glb_reads)

        total_ands = ceil(cycles * 24 * PE_adders)
        self.global_AND_gate.inc_action(action_bitwise, total_ands)

        for PE in self.PEs:
            PE.process_layer(layer, cycles, self.total_PE, PE_adders)
