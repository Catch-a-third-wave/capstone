# Functions file for the capstone project "Cath a third wave".
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

# Function to update NaNs in the smoothed_pct_wear_mask_all_time_weighted with numbers from the  smoothedpct column and to remove lines of NaNs in smoothed_pct_cli.
def deal_with_NaNs_masks(df):
    '''Updates NaN's in smoothed_pct_wear_mask_all_time_weighted with numbers from smoothedpct_wear_mask_all_time_weighted and removes lines with NaN's in smoothed_pct_cli.'''
    # Updating NaN's in the smoothed_pct column with numbers from the smoothedpct column.
    df_to_update = df[['smoothedpct_wear_mask_all_time_weighted','smoothed_pct_wear_mask_all_time_weighted']]
    print('NaNs before update:', df_to_update['smoothed_pct_wear_mask_all_time_weighted'].isna().sum())
    df_to_update['smoothed_pct_wear_mask_all_time_weighted'].update(df_to_update['smoothedpct_wear_mask_all_time_weighted'])
    print('NaNs after update:', df_to_update['smoothed_pct_wear_mask_all_time_weighted'].isna().sum())
    # drop these two columns from the df regions
    df.drop(columns='smoothedpct_wear_mask_all_time_weighted', axis=1, inplace=True)
    # add the 'smoothed_pct_wear_mask_all_time_weighted' column from df_to_update to the regions set
    df['smoothed_pct_wear_mask_all_time_weighted'] = df_to_update['smoothed_pct_wear_mask_all_time_weighted']
    print('Updated.')
    df = df[df['smoothed_pct_cli'].notna()]
    return df

    # Function to create a new dataframe for data on masks.
def create_df_masks(df):
    '''Function to create a data frame for data on masks.'''
    df_masks = df[["country_agg","GID_0","region_agg","GID_1","country_region_numeric","gender","age_bucket","smoothed_pct_cli","date","month"]]
    mask_names = df.columns[(df.columns.str.contains("mask") & (df.columns.str.contains("weighted")))]

    for i in mask_names:
        df_masks[str(i)] = df[str(i)]
    
    return df_masks