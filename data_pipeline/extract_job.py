#import snappy
import os
import csv
import gzip
import time
import shutil
import psycopg2
import getopt, sys
from datetime import datetime
from minio import Minio
from dotenv import load_dotenv

# connect to the postgres server
def get_connection():
    connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="tpcd_db",
    user="aayush",
    password="test123"
    )
    return connection


#get the file location and file name
def get_filename(location, table_name):
    path = location
    file = f"{__file__}_{table_name}_{datetime.timestamp(datetime.now())}.csv"
    if path[-1] == '/':
        return path + file
    return path + '/' + file


# execute the sql
def execute(connect, file_name, query):
    cur = connect.cursor()
    cur.execute(f"{query}")
    
    #writing to csv file
    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        #csv_writer.writerow([cur.rowcount])
        csv_writer.writerow([att_name[0] for att_name in cur.description])
        csv_writer.writerows(cur)
    
    cur.close()
    connect.close()
    rows_affected = cur.rowcount
    return rows_affected 


#compress file
def compress(file):
    
    gz_file = file+'.gz'
    with open(file, "rb") as f_in:
        with gzip.open(gz_file, "wb", compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return gz_file

#calculate file size in KB, MB, GB
def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

#pushing to minIO
def push_file(file):
    load_dotenv()
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    minIO_host = "ec2-65-0-177-178.ap-south-1.compute.amazonaws.com:9000"
    minIO_client = Minio(minIO_host, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
    if minIO_client.bucket_exists(BUCKET_NAME):
        minIO_client.fput_object(BUCKET_NAME, file.split('/')[-1], file)
        print("UPLOAD SUCCESSFUL!")
        return BUCKET_NAME
    print("buket doesn't exits")


def main(location, query, table_name):
    connect = get_connection()
    file = get_filename(location, table_name)
    start = time.time()
    row_count = execute(connect, file, query)
    end = time.time()
    initial_size = os.stat(file).st_size
    compressed_file = compress(file)
    final_size = os.stat(compressed_file).st_size
    initial_size = convert_bytes(initial_size)
    final_size = convert_bytes(final_size)
    timestamp = datetime.now()
    buket = push_file(compressed_file)
    print(f" \ttime : {timestamp}\n \tstart time : {start}\n \tend time : {end}\n \tFile Size(Before compression) :  {initial_size}\n \tFile Size(After compression) :  {final_size}\n \tNumber of rows affected : {row_count}")

if __name__ == '__main__':
    location=""
    query=""
    table_name=""
    argumentsList = sys.argv[1:]

    for i in range(len(argumentsList)-1):
        if argumentsList[i]=="-d":
            location=argumentsList[i+1]
        elif argumentsList[i]=="-t":
            table_name=argumentsList[i+1]
        elif argumentsList[i]=="-q":
            query=argumentsList[i+1]

    #print(f"location: {location} query: {query} table_name: {table_name}")
    if location!="" and query!="" and table_name!="":
        main(location, query, table_name)
    else:
        print("please use all the arguments")