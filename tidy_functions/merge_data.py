import pandas as pd

def merge_corona_stats(survey_data,covid_cases):
    '''This function merges the survey data and the covid_stats data.'''
    # Select columns in covid cases data
    df_cases = covid_cases[["iso_code","date","total_cases_per_million","new_cases_smoothed_per_million","total_deaths_per_million","new_deaths_smoothed_per_million","median_age","aged_65_older"]]

    # Rename 'GID_0' as 'iso_code' in survey data
    survey_data.rename(columns={"GID_0": "iso_code"}, inplace=True)

    # Check differences in included countries between covid cases and survey data
    unique_countries = set(survey_data["iso_code"]).symmetric_difference(set(df_cases["iso_code"]))
    unique_countries_survey = set(survey_data["iso_code"]).intersection(unique_countries)
    unique_countries_cases = set(df_cases["iso_code"]).intersection(unique_countries)

    # Delete rows of countries that only occur in one data set
    df_survey = survey_data[~survey_data['iso_code'].isin(unique_countries_survey)]
    df_covid_cases = df_cases[~df_cases['iso_code'].isin(unique_countries_cases)]

    # Delete rows of dates in covid_cases that are before and after the survey dates
    df_covid = df_covid_cases[df_covid_cases['date'].isin(df_survey['date'])]
    
    # Join datasets on iso_code and date
    df_combined = pd.merge(df_survey,df_covid,on=["iso_code","date"])

    print('Merging corona stats completed.')
    return df_combined

def merge_mask_req(survey_data,mask_wearing_requirements):
    '''Merges survey data with mask wearing requirements data. Make sure you executed steps 1 prepare_mask_req, 2 dummies_mask_req, 3 dummies_public_mask_req, 4dummies_indoors_mask_req, 5 dummies_transport_mask_req and 6 data_types_mask_req from clean_data before running this function.'''
       # Check differences in included countries between covid cases and survey data
    unique_countries = set(survey_data["country_agg"]).symmetric_difference(set(mask_wearing_requirements["country"]))
    unique_countries_survey = set(survey_data["country_agg"]).intersection(unique_countries)
    unique_countries_masks = set(mask_wearing_requirements["country"]).intersection(unique_countries)

    # Change country names in mask wearing set to make them match to the survey data set
    mask_wearing_requirements["country"].replace({"Antigua and Barbuda": "Antigua","Myanmar (formerly Burma)": "Myanmar","Czechia (Czech Republic)": "Czech Republic","Palestine State": "Palestine"},inplace=True)

    # Check differences in included countries between covid cases and survey data
    unique_countries2 = set(survey_data["country_agg"]).symmetric_difference(set(mask_wearing_requirements["country"]))
    unique_countries_masks2 = set(mask_wearing_requirements["country"]).intersection(unique_countries2)

    # Delete rows of countries that only occur in one data set
    df_survey = survey_data[~survey_data['country_agg'].isin(unique_countries_survey)]
    df_masks = mask_wearing_requirements[~mask_wearing_requirements['country'].isin(unique_countries_masks2)]

    # Rename country column
    df_masks.rename(columns={"country":"country_agg"}, inplace=True)

    # Join datasets on iso_code and date
    df_combined = pd.merge(df_survey,df_masks,on=["country_agg"])

    print('Merging mask wearing requirements completed.')
    return df_combined

def create_hdi_columns(survey_data, dict_hdi, dict_hdi_levels):
    '''Uses the hdi dictionary and the hdi-levels dictionary to create a column in the survey dataframe with the hdi and the hdi-levels.Make sure you run rename_hdi_countries, create_hdi_dict and create_hdi_levels_dict first. '''
    
    # Create empty lists for hdi and hdi levels
    index = []
    levels = []
    
    # Get the hdi values for the countries in the regions dataframe and append it to the list.
    for i in range(len(survey_data)):  
        hd_idx = dict_hdi.get(survey_data.at[survey_data.index[i],"country_agg"],"NaN")
        index.append(hd_idx)
    print('Creating hdi list completed.')
    
    # Get the hdi index for the countries in the regions dataframe and append it to the list.
    for i in range(len(survey_data)):  
        hdi_lvls = dict_hdi_levels.get(survey_data.at[survey_data.index[i],"country_agg"],"NaN")
        levels.append(hdi_lvls)
    print('Creating hdi-level list completed.')
    
    # Fill the appended lists into their corresponding columns.
    survey_data["hdi"] = index
    survey_data["hdi_level"] = levels
    
    return survey_data


