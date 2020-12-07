import pandas as pd

def merge_corona_stats(survey_data,covid_cases):
    '''This function merges the survey data and the covid_stats data.'''
    # Select columns in covid cases data
    df_cases = covid_cases[["iso_code","date","total_cases_per_million","new_cases_smoothed_per_million","total_deaths_per_million","new_deaths_smoothed_per_million","median_age","aged_65_older"]]

    # Rename 'GID_0' as 'iso_code' in survey data
    survey_data['iso_code']=survey_data['GID_0']
    survey_data.drop(columns='GID_0', axis=1, inplace=True)

    # Check differences in included countries between covid cases and survey data
    unique_countries = set(survey_data["iso_code"]).symmetric_difference(set(df_cases["iso_code"]))
    unique_countries_survey = set(survey_data["iso_code"]).intersection(unique_countries)
    unique_countries_cases = set(df_cases["iso_code"]).intersection(unique_countries)

    # Delete rows of countries that only occur in one data set
    df_survey = survey_data[~survey_data['iso_code'].isin(unique_countries_survey)]
    df_covid_cases = df_cases[~df_cases['iso_code'].isin(unique_countries_cases)]

    # Delete rows of dates in covid_cases that are before and after the survey dates
    df_covid = df_covid_cases[df_covid_cases['date'].isin(df_survey['date'])]
    
    # Change negative numbers of new cases and deaths per million to 0
    df_covid.loc[df_covid["new_cases_smoothed_per_million"] < 0, "new_cases_smoothed_per_million"] = 0
    df_covid.loc[df_covid["new_deaths_smoothed_per_million"] < 0, "new_deaths_smoothed_per_million"] = 0
    
    # Join datasets on iso_code and date
    df_combined = pd.merge(df_survey,df_covid,on=["iso_code","date"])

    print('Merging corona stats completed.')
    return df_combined