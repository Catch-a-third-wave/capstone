# Functions file for the capstone project "Cath a third wave"
import pandas as pd
import numpy as np
import os 

# Function to import multiple files into a dictionary - use for global country and region data
def get_data(path, name):
    filenames = os.listdir(path)
    filenames = [f for f in filenames if f.lower().endswith(".csv")]
    filenames.sort()
    
    dataframes = {}
    df_names = []

    for filename in filenames:
        df_name = name + "_" + filename[0:2]# the name for the dataframe
        df_names.append(df_name)
        file = "{}/{}".format(path,filename)
        dataframes[df_name] = pd.read_csv(file)
    
    return dataframes


# Function to make the date column the proper data type and add a month column
def insert_month(df):
    df['date'] = pd.to_datetime(df.loc[:,'date'])
    df["month"]=pd.DatetimeIndex(df['date']).month
    return df

