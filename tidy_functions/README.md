List of functions

load_data.py
    load_survey_data(path, name)

clean_data.py
    delete_other_gender(df)
    deal_with_NaNs_masks(df)
    deal_with_NaNs_corona_stats(df_covid)
    prepare_mask_req(mask_wearing_requirements)
    dummies_mask_req(mask_wearing_requirements)
    dummies_public_mask_req(mask_wearing_requirements)
    dummies_indoors_mask_req(mask_wearing_requirements)
    dummies_transport_mask_req(mask_wearing_requirements)
    data_types_mask_req(mask_wearing_requirements)
    rename_hdi_countries(path,filename)
    create_hdi_dict(hdi_data)
    create_hdi_levels_dict(hdi_data)

merge_data.py
    merge_corona_stats(survey_data,covid_cases)
    merge_mask_req(survey_data,mask_wearing_requirements)
    create_hdi_columns(survey_data, dict_hdi, dict_hdi_levels)

feature_engineering.py
    insert_month(df)
    add_requirement_by_date(df_combined)