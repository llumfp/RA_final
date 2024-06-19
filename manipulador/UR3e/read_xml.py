
xml_file = 'taskfile_tampconfig_chess1_pls_final.xml'
csv_file = 'taskfile_tampconfig_chess1_pls_final.csv'

with open(xml_file) as f:
    lines = f.readlines()


inits = []
confs = {}
configs = []
path = 1
i = 0
while not i == len(lines):
    if lines[i].split()[0] in ["<Transit>","<Transfer"]:
        i+=1
        configs.append((lines[i].split()[0],[]))
        confs[f'path{path}'] = []
        while not lines[i].split()[0] in ["</Transit>","</Transfer>"]:
            confs[f'path{path}'].append([float(i) for i in lines[i].split()[1:7]])
            configs[-1][1].append([float(i) for i in lines[i].split()[1:7]])
            i+=1
        path+=1
        i+=1
    else:
        i+=1


        