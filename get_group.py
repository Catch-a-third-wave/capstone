# File with functions to generate various sub dataframes
# Returns a list of dataframes

def group_asia(df):
    asia_w_names = ['Armenia', 'Azerbaijan', 'Israel', 'Jordan', 'Kuwait', 'Lebanon', 'Oman', 'Iraq', 
                    'Qatar', 'Saudi Arabia', 'United Arab Emirates', 'Yemen']
    asia_c_names = ['Kazakhstan', 'Kyrgyzstan', 'Uzbekistan']
    asia_s_names = ['Bangladesh','India', 'Nepal', 'Afghanistan', 'Pakistan', 'Sri Lanka']
    asia_e_names = ['Hong Kong', 'Japan', 'South Korea', 'Taiwan']
    asia_se_names = ['Cambodia','Indonesia', 'Laos','Malaysia', 'Myanmar', 'Singapore', 'Thailand', 
                    'Vietnam']

    asia_w = df.loc[df["country_agg"].isin(asia_w_names)]
    asia_c = df.loc[df["country_agg"].isin(asia_c_names)]
    asia_s = df.loc[df["country_agg"].isin(asia_s_names)]
    asia_e = df.loc[df["country_agg"].isin(asia_e_names)]
    asia_se = df.loc[df["country_agg"].isin(asia_se_names)]

    asia = [asia_w, asia_c, asia_s, asia_e, asia_se]
    
    return asia

def group_oceania(df):
    ceania_names = ["New Zealand", "Australia"]
    oceania = countries.loc[countries["country_agg"].isin(oceania_names)] 

    return oceania


def group_europe(df):
    europe_sc_names = ["Denmark", "Finland", "Norway", "Sweden"]
    europe_w_names = ["Austria", "Belgium", "France", "Germany", "Ireland", "Netherlands", 
                    "Switzerland", "United Kingdom"]
    europe_s_names = ["Italy", "Portugal", "Spain", "Andorra"]
    europe_se_names = ["Albania", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Greece", "Romania", 
                        "Serbia", "Slovenia", "Turkey"]
    europe_e_names = ["Belarus", "Czech Republic", "Hungary", "Moldova", "Poland", "Russia", 
                        "Slovakia", "Ukraine"]
    
    europe_sc = df.loc[df["country_agg"].isin(europe_sc_names)]
    europe_w = df.loc[df["country_agg"].isin(europe_w_names)]
    europe_s = df.loc[df["country_agg"].isin(europe_s_names)]
    europe_se = df.loc[df["country_agg"].isin(europe_se_names)]
    europe_e = df.loc[df["country_agg"].isin(europe_e_names)]

    europe = [europe_sc, europe_w, europe_s, europe_se, europe_e]

    return europe


def group_africa(df):
    africa_e_names = ['Ethiopia', 'Kenya', 'Madagascar', 'Mozambique', 'Tanzania']
    africa_m_names = ['Angola', 'Cameroon','Democratic Republic of the Congo']
    africa_n_names = ['Algeria', 'Egypt', 'Libya','Morocco', 'Tunisia', 'Sudan']
    africa_s_names = ['South Africa']
    africa_w_names = ['Benin', 'Burkina Faso', "Côte d'Ivoire", 'Ghana', 'Guinea', 'Mali', 
                    'Mauritania', 'Nigeria', 'Senegal']
    
    africa_e = df.loc[df["country_agg"].isin(africa_e_names)]
    africa_m = df.loc[df["country_agg"].isin(africa_m_names)]
    africa_n = df.loc[df["country_agg"].isin(africa_n_names)]
    africa_s = df.loc[df["country_agg"].isin(africa_s_names)]
    africa_w = df.loc[df["country_agg"].isin(africa_c_names)]

    africa = [africa_e, africa_m, africa_n, africa_s, africa_w]

    return africa


def group_americas(df):
    america_n_names = ["Canada"]
    america_ce_names = ["Costa Rica", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", 
                        "Panama"]
    america_c_names = ["Dominican Republic", "Haiti"]
    america_s_names = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", 
                        "Peru", "Uruguay", "Venezuela"]
    
    america_n = df.loc[df["country_agg"].isin(america_n_names)]
    america_ce = df.loc[df["country_agg"].isin(america_ce_names)]
    america_c = df.loc[df["country_agg"].isin(america_c_names)]
    america_s = df.loc[df["country_agg"].isin(america_s_names)]

    america = [america_n, america_ce, america_c, america_s]

    return america


def group_hdi(df):
    hdi_low = df[df["hdi_level"] == "low"]
    hdi_medium = df[df["hdi_level"] == "medium"]
    hdi_high = df[df["hdi_level"] == "high"]
    hdi_very_high = df[df["hdi_level"]== "very high"]
    
    hdi = [hdi_low, hdi_medium, hdi_high, hdi_very_high]
    
    return hdi