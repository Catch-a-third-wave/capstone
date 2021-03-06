import pandas as pd 
 
  #Function to create two dictionaries based on the Human Development Index and its levels.
def get_hdi(path,filename):
    '''This function creates two dictionaries based on the Human Development Index and its levels.'''
    
    # Read in the xlsx-file with data
    file = "{}/{}".format(path,filename)
    hdi_data = pd.read_excel(file, header=None)
    
    # Replace the country names in the hdi_data with the corresponding country names as used in
    # the regions data frame.
    hdi_data[1] = hdi_data[1].replace(to_replace ="Viet Nam", value ="Vietnam") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Czechia", value ="Czech Republic") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Russian Federation", value ="Russia") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Venezuela (Bolivarian Republic of)", value ="Venezuela") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Korea (Republic of)", value ="South Korea") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Bolivia (Plurinational State of)", value ="Bolivia") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Hong Kong, China (SAR)", value ="Hong Kong") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Moldova (Republic of)", value ="Moldova") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Tanzania (United Republic of)", value ="Tanzania") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Lao People's Democratic Republic", value ="Laos") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Congo (Democratic Republic of the)", value ="Democratic Republic of the Congo") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Samoa", value ="American Samoa") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Palestine, State of", value ="Palestine") 
    hdi_data[1] = hdi_data[1].replace(to_replace ="Antigua and Barbuda", value ="Antigua") 
       
    # Select the useful rows and columns from the hdi data file to make the hdi.
    df_hdi = hdi_data.iloc[7:200, 1:3]
    
    # Remove the title rows indicating the human development level.
    df_hdi = df_hdi[df_hdi[2].notna()]
    
    # Append missing countries
    df_hdi_missing = pd.DataFrame([["Macau", 0.914],["Aland Islands", 0.911],["Taiwan", 0.911],["Puerto Rico, U.S.", 0.845],["Western Sahara", 0.6764393349141735]],columns = [1,2])
    df_hdi = pd.concat([df_hdi,df_hdi_missing])
     
    # Make a dictionary with countries as keys and the hdi as values.
    dict_hdi = dict(df_hdi.values.tolist())
    
    ## Create hdi-levels dictionary
    
    # Select the useful rows and column from the hdi data file to make the hdi-levels.
    df_levels = hdi_data.iloc[7:200, [1]]
    
    # Create an index based on the title rows indicating the hdi-level.
    idx = df_levels[(df_levels[1].str.contains("HUMAN DEVELOPMENT"))].index
    
    # Use the index to create new dataframes per hdi-level.
    df_very_high = df_levels.iloc[idx[0]-6:idx[1]-7, :]
    df_high = df_levels.iloc[idx[1]-6:idx[2]-7, :]
    df_medium = df_levels.iloc[idx[2]-6:idx[3]-7, :]
    df_low = df_levels.iloc[idx[3]-6:, :]
    
    # Add a column with the hdi-level per data frame.
    df_very_high[2] = "very high"
    df_high[2] = "high"
    df_medium[2] = "medium"
    df_low[2] = "low"

    # Append missing countries
    df_levels_high_missing = pd.DataFrame([["Macau", "very high"],["Aland Islands", "very high"],["Taiwan", "very high"],["Puerto Rico, U.S.", "very high"]],columns = [1,2])
    df_very_high = pd.concat([df_very_high,df_levels_high_missing])
    
    df_levels_medium_missing = pd.DataFrame([["Western Sahara","medium"]], columns = [1,2])
    df_medium = pd.concat([df_medium,df_levels_medium_missing])
    
    # Concatenate dataframes.
    df_hdi_levels = pd.concat([df_very_high, df_high, df_medium, df_low])
    
    # Make a dictionary with countries as keys and hdi-levels as values.
    dict_hdi_levels = dict(df_hdi_levels.values.tolist())
    
    print('Creating dictionaries for hdi and hdi-levels completed.')
    return dict_hdi, dict_hdi_levels    
    
    #Function creates a column in the regions table with the hdi and the hdi-levels.
def create_hdi_columns(countries, dict_hdi, dict_hdi_levels):
    '''This function uses the hdi dictionary and the hdi-levels dictionary to create a column
    in the regions table with the hdi and the hdi-levels.'''
    
    # Create empty lists for hdi and hdi levels
    index = []
    levels = []
    
    # Get the hdi values for the countries in the regions dataframe and append it to the list.
    for i in range(len(countries)):  
        hd_idx = dict_hdi.get(countries.at[countries.index[i],"country_agg"],"NaN")
        index.append(hd_idx)
    print('Creating hdi list completed.')
    
    # Get the hdi index for the countries in the regions dataframe and append it to the list.
    for i in range(len(countries)):  
        hdi_lvls = dict_hdi_levels.get(countries.at[countries.index[i],"country_agg"],"NaN")
        levels.append(hdi_lvls)
    print('Creating hdi-level list completed.')
    
    # Fill the appended lists into their corresponding columns.
    countries["hdi"] = index
    countries["hdi_level"] = levels
    
    return countries
