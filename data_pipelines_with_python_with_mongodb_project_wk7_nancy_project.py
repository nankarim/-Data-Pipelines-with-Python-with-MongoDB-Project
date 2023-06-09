# -*- coding: utf-8 -*-
"""Data_Pipelines_with_Python_with_MongoDB_Project_Wk7_Nancy_project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J552uE0iyKPyAJwlzUFQit8IPCgiRumG
"""

import pandas as pd

# Extraction function
def extract_data():
  # Load call log data from CSV file
    call_logs = pd.read_csv('call_logs.csv')
  # Load billing data from CSV file
    billing_systems = pd.read_csv('billing_systems.csv')

call_logs = pd.read_csv('call_logs.csv')
billing_systems = pd.read_csv('billing_systems.csv')
# Add a new column with identical values to both datasets
call_logs['merge_col'] = 1
billing_systems['merge_col'] = 1
# Merge the datasets on the new column
merged_data = pd.merge(call_logs, billing_systems, on='merge_col')
# Drop the merge column
merged_data.drop('merge_col', axis=1, inplace=True)

# Convert call duration to minutes for easier analysis
merged_data['duration_minutes'] = merged_data['call_duration'] / 60

import logging
# Use Python logging module to log errors and activities
def merge_data():
      logger = logging.getLogger(__name__)
      logger.info("Data extraction completed.")
      return merged_data

# Transformation function
# remove observations with missing values and duplicates
df_drop = merged_data.dropna()
merged_data.drop_duplicates(inplace=True)

# group the data by relevant parameters
grouped_data = merged_data.groupby(['call_id', 'call_duration', 'call_date', 'call_type','transaction_id','caller_number','receiver_number','customer_id','transaction_amount','transaction_date','transaction_type'])

#aggregate the grouped data
aggregated_data = grouped_data.agg({
    'call_duration': ['sum', 'count', 'mean']
})

# Identify patterns in the data

# Use data compression techniques to optimize performance
import gzip
compressed_data = gzip.compress(aggregated_data.to_json().encode())

import logging
# Use Python logging module to log errors and activities
def compressed_data():
      logger = logging.getLogger(__name__)
      logger.info("Data extraction completed.")
      return compressed_data

# Loading function
#def load_data(compressed_data):

!curl ipecho.net/plain

!pip install pymongo
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://nancyproject1:Galaxy123!@cluster0.0bkm2h2.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('mongodbproj')
collection = db.call_records

collection.create_index([('customer_id', pymongo.ASCENDING)])

#Use bulk inserts to optimize performance
    
documents = [
    {"customer_id": 1, "timestamp": "2022-01-01T00:00:00Z", "call_type": "outgoing", "duration": 120},
    {"customer_id": 1, "timestamp": "2022-01-02T00:00:00Z", "call_type": "incoming", "duration": 60},
    {"customer_id": 2, "timestamp": "2022-01-01T01:00:00Z", "call_type": "outgoing", "duration": 180}
]

operations = [pymongo.InsertOne(doc) for doc in documents]

# Use the write concern option to ensure that data is written to disk
collection.acknowledge_writes(w=1, j=True)

# Use Python logging module to log errors and activities
logger = logging.getLogger(__name__)
logger.info("Data loading completed.")

if __name__ == '__main__':
    file_path = 'call_logs.csv'
    data = extract_data(file_path)
    transformed_data = transform_data(data)
    load_data(transformed_data)