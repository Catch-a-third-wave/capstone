import pandas as pd
import numpy as np
import os 

def load_survey_data(path, name):
    '''Function to read in survey data files from csv and import it into a dictionary of dataframes - used for global country and region data.'''
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

    print('Read in survey data completed.')
    return dataframes


