def create_df_masks(df):
    '''Function to create a data frame for data on masks.'''
    df_masks = df[["country_agg","GID_0","gender","age_bucket","smoothed_pct_cli","date","month","hdi","hdi_level"]]
    mask_names = df.columns[(df.columns.str.contains("mask") & (df.columns.str.contains("weighted")))]

    for i in mask_names:
        df_masks[str(i)] = df[str(i)]
    
    print('Created dataframe.')
    return df_masks

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

def delete_overall(df):
    ''' This function deletes the rows with 'other' and 'overall in the gender column and the rows with 'overall' in the age bucket column.'''
    df1 = df[df['gender']!='other']
    df2 = df1[df1['gender']!='overall']
    df3 = df2[df2['age_bucket']!='overall']
    print('Deleted other and overall.')
    return df3

def normalize_mask_data(df):
    df_normalized= df[["age_bucket","date","gender","hdi","hdi_level","month"]]
    df_normalized["country"] = df["country_agg"]
    df_normalized["country_id"] = df["GID_0"]
    df_normalized["pct_covid_like_illness"] = df.smoothed_pct_cli/100
    df_normalized["pct_wear_mask_all_time"] = df.smoothed_pct_wear_mask_all_time_weighted/100
    df_normalized["pct_wear_mask_most_time"] = df.smoothed_pct_wear_mask_most_time_weighted/100
    df_normalized["pct_wear_mask_half_time"] = df.smoothed_pct_wear_mask_half_time_weighted/100
    df_normalized["pct_wear_mask_some_time"] = df.smoothed_pct_wear_mask_some_time_weighted/100
    df_normalized["pct_wear_mask_none_time"] = df.smoothed_pct_wear_mask_none_time_weighted/100
    print('Normalized mask data.')
    return df_normalized