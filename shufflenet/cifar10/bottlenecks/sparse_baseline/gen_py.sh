#!/bin/bash

echo "import numpy as np" > convert_comp.py
echo "import numpy as np" > convert_decomp.py
echo "import numpy as np" > convert_conv.py


SIM_DIR="./../baseline"
CURRENT_DIR="sparse_baseline"

for i in $(seq 1 15);
do
	python3 convert_map_to_py.py --file ${SIM_DIR}/b${i}/comp/output/timeloop-mapper.map.txt --name comp${i} >> convert_comp.py
	echo >> convert_comp.py
	python3 convert_map_to_py.py --file ${SIM_DIR}/b${i}/decom/output/timeloop-mapper.map.txt --name decomp${i} >>  convert_decomp.py
	echo >> convert_decomp.py
        python3 convert_map_to_py.py --file ${SIM_DIR}/b${i}/conv/output/timeloop-mapper.map.txt --name conv${i} >>  convert_conv.py
        echo >> convert_conv.py
done

python3 gen_route.py --comp 1 >> convert_comp.py
python3 gen_route.py --comp 0 >> convert_decomp.py
python3 gen_route.py --comp 2 >> convert_conv.py
