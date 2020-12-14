import pandas as pd

def delete_other_gender(df):
    ''' Deletes the rows with 'other' in the gender column.'''
    df1 = df[df['gender']!='other']
    return df1

def deal_with_NaNs_masks(df):
    '''Updates NaN's in smoothed_pct_wear_mask_all_time_weighted with numbers from smoothedpct_wear_mask_all_time_weighted and removes lines with NaN's in smoothed_pct_cli.'''
    # Updating NaN's in the smoothed_pct column with numbers from the smoothedpct column.
    df_to_update = df[['smoothedpct_wear_mask_all_time_weighted','smoothed_pct_wear_mask_all_time_weighted']]
    print('NaNs before update:', df_to_update['smoothed_pct_wear_mask_all_time_weighted'].isna().sum())
    df_to_update['smoothed_pct_wear_mask_all_time_weighted'].update(df_to_update['smoothedpct_wear_mask_all_time_weighted'])
    print('NaNs after update:', df_to_update['smoothed_pct_wear_mask_all_time_weighted'].isna().sum())
    # drop this column from the survey data
    df.drop(columns='smoothedpct_wear_mask_all_time_weighted', axis=1, inplace=True)
    # add the 'smoothed_pct_wear_mask_all_time_weighted' column from df_to_update to the survey data
    df['smoothed_pct_wear_mask_all_time_weighted'] = df_to_update['smoothed_pct_wear_mask_all_time_weighted']
    print('Updated NaNs in wear_mask_all_time.')
    df = df[df['smoothed_pct_cli'].notna()]
    return df


def deal_with_NaNs_corona_stats(df):
    '''Removes negative case numbers, deals with NaNs and removes Hong Kong.'''
    # Change negative numbers of new cases and deaths per million to 0
    df.loc[df["new_cases_smoothed_per_million"] < 0, "new_cases_smoothed_per_million"] = 0
    df.loc[df["new_deaths_smoothed_per_million"] < 0, "new_deaths_smoothed_per_million"] = 0
    # Deal with NaNs in 'new_cases_smoothed_per_million' column
    df.loc[df['new_cases_smoothed_per_million'].isna(), "new_cases_smoothed_per_million"] = 0
    # Deal with NaNs in 'new_deaths_smoothed_per_million' column
    df.loc[df['new_deaths_smoothed_per_million'].isna(), "new_deaths_smoothed_per_million"] = 0
    # Deal with NaNs in 'median_age' column
    df.loc[df['location'] == 'Dominica', "median_age"] = 34.9
    df.loc[df['location'] == 'Andorra', "median_age"] = 46.2
    # Deal with NaNs in 'aged_65_and_older' column.
    df.loc[df['location'] == 'Dominica', "aged_65_older"] = 12.12
    df.loc[df['location'] == 'Taiwan', "aged_65_older"] = 16
    df.loc[df['location'] == 'Andorra', "aged_65_older"] = 17.36
    df.loc[df['location'] == 'Western Sahara', "aged_65_older"] = 4.1
    # Remove Hong Kong, as it has much missing data.
    df = df[df['location'] != 'Hong Kong']
    # Replace missing value in total_cases_per_million (Venezuela, 2020-06-18) with value of the previous day 
    df.loc[df['total_cases_per_million'].isna(), "total_cases_per_million"] = 110.775
    print('NaNs removed.')
    return df

def prepare_mask_req(mask_wearing_requirements):
    '''Drops and renames columns, extracts country name and deals with 'full_country' column.'''
    # Drop columns GDP and Population
    mask_wearing_requirements.drop(columns=["GDP (2018 in Millions)","Population"], axis=1, inplace=True)

    # Rename columns
    mask_wearing_requirements.rename(columns={"Country": "country","Masks Required? (At Least In Businesses)": "required","Type of Requirement?": "requirement_type","Date of Full Country Requirement": "mask_requirement_date","Recommend To Wear Masks?": "mask_recommended"}, inplace=True)

    # Extract country name between brackets in first column
    location = []
    for i in range(len(mask_wearing_requirements)):
        country_name = mask_wearing_requirements.at[mask_wearing_requirements.index[i],"country"].split('[', 1)[1].split(']')[0]
        location.append(country_name)
    mask_wearing_requirements["country"] = location

    # add observations of yes public transport to full country
    mask_wearing_requirements["required"].replace("Yes (Public Transport)", "Full Country", inplace=True)

    print('Step 1 of cleaning requirements completed.')
    return mask_wearing_requirements

def dummies_mask_req(mask_wearing_requirements):
    '''Creates column with dummy variables for 'required' column and renames columns of dummy variables.'''
    # Make dummy variables out of the required column
    dummies = pd.get_dummies(mask_wearing_requirements['required'])
    mask_wearing_requirements = mask_wearing_requirements.join(dummies)

    # Rename dummy variables
    mask_wearing_requirements.rename(columns={"Full Country": "mask_required_full_country","No": "mask_not_required","No, But Recommends Masks": "mask_not_required_recommended","No, But Universal Mask Usage": "mask_not_required_universal","Parts of Country": "mask_required_part_country"}, inplace=True)

    # Make content of requirement_type column lower case
    mask_wearing_requirements["requirement_type"] = mask_wearing_requirements["requirement_type"].str.lower()

    print('Step 2 of cleaning requirements completed.')
    return mask_wearing_requirements

def dummies_public_mask_req(mask_wearing_requirements):
    '''Creates dummy variables for 'everywhere_in_public' column.'''
    # Create everywhere in public dummy variable
    everywhere_in_public = []
    everywhere = ["everywhere in public","everywhere in public where social distancing isn't possible","public transport + everywhere in public with more than 10 people","public transport + select states: everywhere","all crowded places + universal mask usage","all indoor public places + outdoor within 20 meters of others","public transport + everywhere in public where social distancing isn't possible","public transport, markets, supermarkets & crowded places","everywhere in public (major cities)"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in everywhere:
            everywhere_in_public.append(1)
        else:
            everywhere_in_public.append(0)

    mask_wearing_requirements["mask_everywhere_in_public"] = everywhere_in_public

    print('Step 3 of cleaning requirements completed.')
    return mask_wearing_requirements

def dummies_indoors_mask_req(mask_wearing_requirements):
    '''Creates dummy variables for public_indoors column.'''
    # Create public indoors variable
    public_indoors = []
    indoors = ["all indoor public places","public transport & stores","all indoor public places with multiple people","public transport + shops","all commercial establishments","public transport & shopping","supermarkets, banks & some indoor spaces","public roads & business employees","public transport + shopping","public transport + markets + most public places","public transportation, medical facilities, shops, and malls","certain public places","public transit, shops, and supermarkets","all indoor public places + outdoor within 20 meters of others","public transit, cinemas, churches, theaters, banks, and restaurants","public transport, markets, supermarkets & crowded places"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in indoors:
            public_indoors.append(1)
        else:
            public_indoors.append(0)
            
    mask_wearing_requirements["mask_public_indoors"] = public_indoors

    print('Step 4 of cleaning requirements completed.')
    return mask_wearing_requirements

def dummies_transport_mask_req(mask_wearing_requirements):
    '''Creates dummy variable for public_transport column.'''
    # create public transport variable
    public_transport = []
    transport= ["public transport","public transport & stores","public transport + shops","public transport & shopping","public roads & business employees","public transport + shoppingpublic transport + markets + most public places","public transportation, medical facilities, shops, and malls","public transport + everywhere in public with more than 10 people","public transit, shops, and supermarkets","public transport + select states: everywhere","public transit, cinemas, churches, theaters, banks, and restaurants","public transport + everywhere in public where social distancing isn't possible","public buses & at airports","public transport, markets, supermarkets & crowded places"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in transport:
            public_transport.append(1)
        else:
            public_transport.append(0)
            
    mask_wearing_requirements["mask_public_transport"] = public_transport

    print('Step 5 of cleaning requirements completed.')
    return mask_wearing_requirements

def data_types_mask_req(mask_wearing_requirements):
    '''Drops 'required' and 'requirement_type' columns, changes mask_recommended to binary, sets missing date to 29 April 2020 and creates datetime object.'''
    # Drop required and requirement_type columns
    mask_wearing_requirements.drop(columns=["required","requirement_type"], axis=1, inplace=True)
    
    # Change mask_recommended from 'Yes/No' to binary 0/1
    mask_wearing_requirements.loc[mask_wearing_requirements["mask_recommended"] == "Yes", "mask_recommended"] = 1
    mask_wearing_requirements.loc[mask_wearing_requirements["mask_recommended"] == "No", "mask_recommended"] = 0
    mask_wearing_requirements.loc[mask_wearing_requirements["mask_recommended"].isna(), "mask_recommended"] = 0
    mask_wearing_requirements["mask_recommended"] = mask_wearing_requirements["mask_recommended"].astype('uint8')

    # Set missing dates in 'mask_requirement_date' to 29 April 2020
    mask_wearing_requirements.loc[mask_wearing_requirements["mask_requirement_date"].isna(), "mask_requirement_date"] = pd.to_datetime("2020-04-29")

    # Make datetime object from 'mask_requirement_date'
    mask_wearing_requirements['mask_requirement_date'] = pd.to_datetime(mask_wearing_requirements.loc[:,'mask_requirement_date'])

    print('Step 6 of cleaning requirements completed.')
    return mask_wearing_requirements

def rename_hdi_countries(path,filename):
    '''Renames the countries in the Human Development Index that are named different than the survey data.'''
    
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
    
    return hdi_data

def create_hdi_dict(hdi_data):
    '''Creates a HDI dictionary. Make sure you run rename_hdi_countries first.'''
     # Select the useful rows and columns from the hdi data file to make the hdi.
    df_hdi = hdi_data.iloc[7:200, 1:3]
    
    # Remove the title rows indicating the human development level.
    df_hdi = df_hdi[df_hdi[2].notna()]
    
    # Append missing countries
    df_hdi_missing = pd.DataFrame([["Macau", 0.914],["Aland Islands", 0.911],["Taiwan", 0.911],["Puerto Rico, U.S.", 0.845],["Western Sahara", 0.6764393349141735]],columns = [1,2])
    df_hdi = pd.concat([df_hdi,df_hdi_missing])
     
    # Make a dictionary with countries as keys and the hdi as values.
    dict_hdi = dict(df_hdi.values.tolist())
    print('Creating dictionaries for hdi completed.')
    return dict_hdi

def create_hdi_levels_dict(hdi_data):
    '''Creates a HDI-levels dictionary. Make sure you run rename_hdi_countries first.'''
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
    
    print('Creating dictionaries for hdi-levels completed.')
    return dict_hdi_levels    
