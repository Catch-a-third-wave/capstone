import pandas as pd

def insert_month(df):
    '''Changes object date to datetime object date and creates a column with month. Apply after merging the corona-stats datafile with the survey data.'''
    df['date'] = pd.to_datetime(df.loc[:,'date'])
    df["month"]=pd.DatetimeIndex(df['date']).month
    print('Month column created.')
    return df
    
def add_requirement_by_date(df_combined):
    '''Adds columns with prefix 'cur_' indicating current requirements at the date of the survey and the COVID-19 cases per country. Make sure you executed steps 1 prepare_mask_req, 2 dummies_mask_req, 3 dummies_public_mask_req, 4dummies_indoors_mask_req, 5 dummies_transport_mask_req and 6 data_types_mask_req from clean_data and merge_mask_req from merge_data before running this function.'''
    cur_mask_recommended = []
    cur_mask_required_full_country = []
    cur_mask_not_required = []
    cur_mask_not_required_recommended = []
    cur_mask_not_required_universal = []
    cur_mask_required_part_country = []
    cur_mask_everywhere_in_public = []
    cur_mask_public_indoors = []
    cur_mask_public_transport = []

    requirements = ["mask_recommended","mask_required_full_country","mask_not_required","mask_not_required_recommended","mask_not_required_universal","mask_required_part_country","mask_everywhere_in_public","mask_public_indoors","mask_public_transport"]

    current_requirements = [cur_mask_recommended,cur_mask_required_full_country,cur_mask_not_required,cur_mask_not_required_recommended,cur_mask_not_required_universal,cur_mask_required_part_country,cur_mask_everywhere_in_public,
    cur_mask_public_indoors,cur_mask_public_transport]

    for i in range(len(requirements)):
        for j in range(len(df_combined)):
            if df_combined.at[df_combined.index[j],'mask_requirement_date'] > df_combined.at[df_combined.index[j],'date']:
                if df_combined.at[df_combined.index[j],requirements[i]] == 1:
                    current = 0
                    current_requirements[i].append(current)
                else:
                    current_requirements[i].append(df_combined.at[df_combined.index[j],requirements[i]])
            else:
                current_requirements[i].append(df_combined.at[df_combined.index[j],requirements[i]])
                
    df_combined["cur_mask_recommended"] = cur_mask_recommended
    df_combined["cur_mask_required_full_country"] = cur_mask_required_full_country
    df_combined["cur_mask_not_required"] = cur_mask_not_required
    df_combined["cur_mask_not_required_recommended"] = cur_mask_not_required_recommended
    df_combined["cur_mask_not_required_universal"] = cur_mask_not_required_universal
    df_combined["cur_mask_required_part_country"] = cur_mask_required_part_country
    df_combined["cur_mask_everywhere_in_public"] = cur_mask_everywhere_in_public
    df_combined["cur_mask_public_indoors"] = cur_mask_public_indoors
    df_combined["cur_mask_public_transport"] = cur_mask_public_transport

    print('Feature engineering completed.')
    return df_combined