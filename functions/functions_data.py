import pandas as pd
import numpy as np
import os 

# Function to import multiple files into a dictionary - use for global country and region data.
def get_data(path, name):
    '''Function to read in data files from csv and import it into a dictionary of dataframes - used for global country and region data.'''
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

    print('Read in data completed.')
    return dataframes


# Function to make the date column the proper data type and add a month column.
def insert_month(df):
    '''Changes object date to datetime object date and creates a column with month.'''
    df['date'] = pd.to_datetime(df.loc[:,'date'])
    df["month"]=pd.DatetimeIndex(df['date']).month
    print('Created month column.')
    
    return df