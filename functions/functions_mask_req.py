import pandas as pd

def merge_mask_requirements(survey_data,mask_wearing_requirements):

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

    # Make dummy variables out of the required column
    dummies = pd.get_dummies(mask_wearing_requirements['required'])
    mask_wearing_requirements = mask_wearing_requirements.join(dummies)

    # Rename dummy variables
    mask_wearing_requirements.rename(columns={"Full Country": "mask_required_full_country","No": "mask_not_required","No, But Recommends Masks": "mask_not_required_recommended","No, But Universal Mask Usage": "mask_not_required_universal","Parts of Country": "mask_required_part_country"}, inplace=True)

    # Make content of requirement_type column lower case
    mask_wearing_requirements["requirement_type"] = mask_wearing_requirements["requirement_type"].str.lower()

    # Create everywhere in public dummy variable
    everywhere_in_public = []
    everywhere = ["everywhere in public","everywhere in public where social distancing isn't possible","public transport + everywhere in public with more than 10 people","public transport + select states: everywhere","all crowded places + universal mask usage","all indoor public places + outdoor within 20 meters of others","public transport + everywhere in public where social distancing isn't possible","public transport, markets, supermarkets & crowded places","everywhere in public (major cities)"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in everywhere:
            everywhere_in_public.append(1)
        else:
            everywhere_in_public.append(0)

    mask_wearing_requirements["mask_everywhere_in_public"] = everywhere_in_public

    # Create public indoors variable
    public_indoors = []
    indoors = ["all indoor public places","public transport & stores","all indoor public places with multiple people","public transport + shops","all commercial establishments","public transport & shopping","supermarkets, banks & some indoor spaces","public roads & business employees","public transport + shopping","public transport + markets + most public places","public transportation, medical facilities, shops, and malls","certain public places","public transit, shops, and supermarkets","all indoor public places + outdoor within 20 meters of others","public transit, cinemas, churches, theaters, banks, and restaurants","public transport, markets, supermarkets & crowded places"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in indoors:
            public_indoors.append(1)
        else:
            public_indoors.append(0)
            
    mask_wearing_requirements["mask_public_indoors"] = public_indoors

    # create public transport variable
    public_transport = []
    transport= ["public transport","public transport & stores","public transport + shops","public transport & shopping","public roads & business employees","public transport + shoppingpublic transport + markets + most public places","public transportation, medical facilities, shops, and malls","public transport + everywhere in public with more than 10 people","public transit, shops, and supermarkets","public transport + select states: everywhere","public transit, cinemas, churches, theaters, banks, and restaurants","public transport + everywhere in public where social distancing isn't possible","public buses & at airports","public transport, markets, supermarkets & crowded places"]

    for j in range(len(mask_wearing_requirements)):
        if mask_wearing_requirements.at[mask_wearing_requirements.index[j],"requirement_type"] in transport:
            public_transport.append(1)
        else:
            public_transport.append(0)
            
    mask_wearing_requirements["mask_public_transport"] = public_transport

    # Drop required and requirement_type columns
    mask_wearing_requirements.drop(columns=["required","requirement_type"], axis=1, inplace=True)

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

