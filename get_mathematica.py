import json
import sys
task1_path=sys.argv[1]
with open(task1_path, 'r') as fcc_file:
    fcc_data = json.load(fcc_file)
    matrix=[]
    for agent in fcc_data:
        matrix.append(fcc_data[agent])
    print(str(matrix).replace('[','{').replace(']','}'))
