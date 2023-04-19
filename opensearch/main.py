import pandas as pd
import regex as re

d = {'operations' : [],
     'values' : []
     }

admin_ops = ['delete-index', 'create-index', 'cluster-health', 'index-append', 'refresh', 'index-stats', 'force-merge', 'create-snapshot', 'delete-snapshot', 'wait-for-snapshot-creation', 'restore-snapshot', 'index', 'index-update', 'refresh-after-force-merge', 'wait-until-merges-finish', 'refresh-after-index', 'start-transform',
'wait-for-transform',
'delete-transform', 'put-settings',
'create-transform', 'default', 'create-snapshot-repository']

f = open("default.json","r")
ops = []
for line in f:
    line.strip()
    if re.search(r"operation*", line):
        if re.search(r"[a-z]*{", line) or re.search(r"description*", line):
            continue
        l = line.split(':')
        x = l[1].strip()
        x = x.replace('\"','')
        if x[-1] == ',':
            x = x.replace(',','')
        print(x) 
        if x in admin_ops:
            d['operations'].append(x)
            d['values'].append('Admin operation (NOT-INTERESTED)')
        else:
            d['operations'].append(x)
            d['values'].append('INTERESTED')
        print(d)

df = pd.DataFrame(d)
df.to_excel('operations_noaa.xlsx')



##############################
# parsing the operations now #
##############################



f = open("default_ops.json", "r")
out = open("scripts_noaa.txt", "w")
flag = False
for line in f:
    line.strip()
    if re.search(r"name", line):
        l = line.split(':')
        x = l[1].strip()
        x = x.replace('\"','')
        if x[-1] == ',':
            x = x.replace(',','')
        if x not in admin_ops:
            flag = True
        else:
            flag = False
    if flag:
        out.write(line)