import pandas as pd

import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
server = app.server

# ------------------------------------------------------------

#dfs_country = functions.functions_data.get_data("dash_data/country/smooth/", "country")
#countries = pd.concat(dfs_country, ignore_index=True)
#countries = functions.functions_data.insert_month(countries)
df = pd.read_csv("dash_data/countries_dash.csv.gzip", compression="gzip")

#--------------------------------------------------------------------------------
#App layout
app.layout = html.Div([
    
    html.H1("Corona Pandemic over Time", style={"text-align": "centre"}),
    
    dcc.Dropdown(id="slct_gender",
                options=[
                    {"label": "Overall", "value": "overall"},
                    {"label": "Female", "value": "female"},
                    {"label": "Male", "value": "male"}],
                multi=False,
                value="overall",
                style={"width": "40%"}
                ),
    
    dcc.Dropdown(id="data",
                options=[
                    {"label": "Total cases per million", "value": "total_cases_per_million"},
                    {"label": "Total deaths per million", "value": "total_deaths_per_million"},
                    {"label": "Median Age", "value": "median_age"},
                    {"label": "Human Development Index", "value": "hdi"},
                    {"label": "Total number of responses", "value": "rolling_total_responses"},
                    {"label": "Percentage of people with COVID-like illness", "value": "smoothed_pct_cli_weighted"},
                    {"label": "Percentage of people working outside their own home", "value": "smoothed_pct_worked_outside_home_weighted"},
                    {"label": "Percentage of people leaving their house for groceries/pharmacy", "value": "smoothed_pct_grocery_outside_home_weighted"},
                    {"label": "Percentage of people eating meals outside their own home", "value": "smoothed_pct_ate_outside_home_weighted"},
                    {"label": "Percentage of people spending time with non-household members", "value": "smoothed_pct_spent_time_with_non_hh_weighted"},
                    {"label": "Percentage of people attending public events", "value": "smoothed_pct_attended_public_event_weighted"},
                    {"label": "Percentage of people using public transport", "value": "smoothed_pct_used_public_transit_weighted"},
                    {"label": "Percentage of people in direct contact with non-household members", "value": "smoothed_pct_direct_contact_with_non_hh_weighted"},
                    {"label": "Percentage of people who haven't been in public in 7 days", "value": "smoothed_pct_no_public_weighted"},
                    {"label": "Percentage of people wearing masks all the time", "value": "smoothed_pct_wear_mask_all_time_weighted"},
                    {"label": "Percentage of people wearing masks most of the time", "value": "smoothed_pct_wear_mask_most_time_weighted"},
                    {"label": "Percentage of people wearing masks half of the time", "value": "smoothed_pct_wear_mask_half_time_weighted"},
                    {"label": "Percentage of people wearing masks some times", "value": "smoothed_pct_wear_mask_some_time_weighted"},
                    {"label": "Percentage of people never wearing masks", "value": "smoothed_pct_wear_mask_none_time_weighted"}],

                multi=False,
                value="total_cases_per_million",
                style={"width": "40%"}
                ),
    
    html.Div(id="output_container", children=[]),
    html.Br(),
    
    dcc.Graph(id="my_covid_map", figure={}, style={"width": "150vh", "height": "90vh"})
    
])



#----------------------------------------------------------------------------
#Connect the plotly graphs with Dash Components

@app.callback(
    [Output(component_id = "output_container", component_property="children"),
    Output(component_id = "my_covid_map", component_property="figure")],
    [Input(component_id = "slct_gender", component_property="value"),
    Input(component_id = "data", component_property="value")]
)
def update_graph(ddgender, option):
    print(ddgender, option)
    #print(type(option_slct1, option_slct2))
    
    container = "The user chose to display {} for {} gender".format(option, ddgender)
    
    dff = df[(df["data_cat"]==option) & (df["gender"]==ddgender)]
    
    ranges = {
        "total_cases_per_million": [0, 63500],   
        "total_deaths_per_million": [0, 1070],
        "rolling_total_responses": [50,120000],
        "smoothed_pct_cli_weighted": [0, 62],
        "smoothed_pct_worked_outside_home_weighted": [0, 90],
        "smoothed_pct_grocery_outside_home_weighted": [0, 93],
        "smoothed_pct_ate_outside_home_weighted": [0, 86],
        "smoothed_pct_spent_time_with_non_hh_weighted": [0, 83],
        "smoothed_pct_attended_public_event_weighted": [0, 74],
        "smoothed_pct_used_public_transit_weighted": [0, 80],
        "smoothed_pct_direct_contact_with_non_hh_weighted": [0, 90],
        "smoothed_pct_no_public_weighted": [0, 67],
        "smoothed_pct_wear_mask_all_time_weighted": [0, 96],
        "smoothed_pct_wear_mask_most_time_weighted": [0, 52],
        "smoothed_pct_wear_mask_half_time_weighted": [0, 42],
        "smoothed_pct_wear_mask_some_time_weighted": [0, 46],
        "smoothed_pct_wear_mask_none_time_weighted": [0, 94]
        }


    #Plotly Express
    fig = px.choropleth(
        data_frame = dff,
        locations="iso_code",
        color="amount",
        range_color=ranges.get(option),
        hover_name="country_agg",
        hover_data=["date", "data_cat", "amount"],
        animation_frame = "date",
        projection = "natural earth",
        color_continuous_scale=["white", "#00c5ff", "#00287f", "#00151f"]
    )
    
    return container, fig

#-------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server()

