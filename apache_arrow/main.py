import os
import pyarrow
import time
import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq
from pyarrow.csv import read_csv

arrow_d = {'operations' : [], 'time' : [], 'mem' : []}
panda_d = {'operations' : [], 'time' : [], 'mem' : []}

def calculate_ram_used():
    total_memory, used_memory, free_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
 
    # Memory usage
    return round((used_memory/total_memory) * 100, 2)

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def csv_read(file):
    print(f'THE SIZE OF CSV FILE IS {convert_bytes(os.stat(file).st_size)}')
    start_arrow = time.time()
    arrow_read = read_csv(file)
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_read = pd.read_csv(file, low_memory=False)
    pd_mem = calculate_ram_used()
    end_pd = time.time()

    arrow_d['operations'].append('read')
    panda_d['operations'].append('read')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)

    return arrow_read, pd_read

# def parquet_read(file):
#     print(f'THE SIZE OF PARQUET FILE IS {convert_bytes(os.stat(file).st_size)}')
#     start_pd = time.time()
#     pd_read = pd.read_parquet(file)
#     end_pd = time.time()
#     start_arrow = time.time()
#     arrow_read = pq.read_table(file)
#     end_arrow = time.time()

#     print(f'arrow parquet read time = {round((end_arrow-start_arrow),2)}')
#     print(f'pandas parquet read time = {round((end_pd-start_pd),2)}')

#     return arrow_read, pd_read

def test_sort(arrow_table, pd_table):
    start_arrow = time.time()
    sorted_arrow = arrow_table.sort_by([('total_amount', 'ascending')])
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_table.sort_values(by = "total_amount")
    pd_mem = calculate_ram_used()
    end_pd = time.time()


    arrow_d['operations'].append('sort')
    panda_d['operations'].append('sort')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)



def test_aggrigation(arrow_table, pd_table):
    #calculating sum
    start_arrow = time.time()
    pa_sum = pc.sum(arrow_table['tip_amount'])
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_sum = pd_table['tip_amount'].sum()
    pd_mem = calculate_ram_used()
    end_pd = time.time()
    arrow_d['operations'].append('sum')
    panda_d['operations'].append('sum')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)

    #calculating max
    start_arrow = time.time()
    pa_max = pc.max(arrow_table['tip_amount'])
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_max = pd_table['tip_amount'].max()
    pd_mem = calculate_ram_used()
    end_pd = time.time()
    arrow_d['operations'].append('max')
    panda_d['operations'].append('max')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)

    #calculating min
    start_arrow = time.time()
    pa_min = pc.min(arrow_table['tip_amount'])
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_min = pd_table['tip_amount'].min()
    pd_mem = calculate_ram_used()
    end_pd = time.time()
    arrow_d['operations'].append('min')
    panda_d['operations'].append('min')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)

    #calculating count
    start_arrow = time.time()
    pa_count = pc.count(arrow_table['tip_amount'])
    arrow_mem = calculate_ram_used()
    end_arrow = time.time()
    start_pd = time.time()
    pd_count = pd_table['tip_amount'].count()
    pd_mem = calculate_ram_used()
    end_pd = time.time()
    arrow_d['operations'].append('count')
    panda_d['operations'].append('count')
    arrow_d['time'].append(round((end_arrow-start_arrow),2))
    panda_d['time'].append(round((end_pd-start_pd),2))
    arrow_d['mem'].append(arrow_mem)
    panda_d['mem'].append(pd_mem)
    

def main():

    arrow_table, pd_table = csv_read('taxi.csv')
    # calculate_ram_used()
    # arrow_table2, pd_table2 = parquet_read('yellow_tripdata_2020-01.parquet')

    test_aggrigation(arrow_table, pd_table)

    test_sort(arrow_table, pd_table)
    arrow_df=pd.DataFrame.from_dict(arrow_d)
    panda_df=pd.DataFrame.from_dict(panda_d)
    merged_results=pd.merge(arrow_df, panda_df, how='inner', on='operations')
    merged_results.columns = ['operations', 'time_arrow', 'mem_arrow', 'time_pandas', 'mem_pandas']
    print(merged_results)

main()