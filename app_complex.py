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
df = pd.read_csv("dash_data/countries_dash2.csv.gzip", compression="gzip")

#--------------------------------------------------------------------------------
#App layout
app.layout = html.Div([
    
    html.H1("Dashboard for Capstone", style={"text-align": "centre"}),
    
    dcc.Dropdown(id="slct_gender",
                options=[
                    {"label": "Overall", "value": "overall"},
                    {"label": "Female", "value": "female"},
                    {"label": "Male", "value": "male"}],
                multi=False,
                value="overall",
                style={"width": "40%"}
                ),

    dcc.Dropdown(id="slct_age",
                options=[
                    {"label": "Overall", "value": "overall"},
                    {"label": "18-34", "value": "18-34"},
                    {"label": "35-54", "value": "35-54"},
                    {"label": "55+", "value": "55+"}],
                multi=False,
                value="overall",
                style={"width": "40%"}
                ),
    
    dcc.Dropdown(id="data",
                options=[
                    {"label": "Number of responses", "value": "rolling_total_responses"},
                    {"label": "Individuals with COVID-like illness", "value": "smoothed_pct_cli_weighted"},
                    {"label": "Individuals working outside their own home", "value": "smoothed_pct_worked_outside_home_weighted"},
                    {"label": "People going to the grocery store or pharmacy", "value": "smoothed_pct_grocery_outside_home_weighted"},
                    {"label": "People leaving their own home for meals", "value": "smoothed_pct_ate_outside_home_weighted"},
                    {"label": "People spending time with other households", "value": "smoothed_pct_spent_time_with_non_hh_weighted"},
                    {"label": "People attending public events", "value": "smoothed_pct_attended_public_event_weighted"},
                    {"label": "People using public transport", "value": "smoothed_pct_used_public_transit_weighted"},
                    {"label": "People having direct contact with other households", "value": "smoothed_pct_direct_contact_with_non_hh_weighted"},
                    {"label": "People having no public contact in the last 7 days", "value": "smoothed_pct_no_public_weighted"},
                    {"label": "People wearing masks all the time", "value": "smoothed_pct_wear_mask_all_time_weighted"},
                    {"label": "People wearing masks most of the time", "value": "smoothed_pct_wear_mask_most_time_weighted"},
                    {"label": "People wearing masks half of the time", "value": "smoothed_pct_wear_mask_half_time_weighted"},
                    {"label": "People wearing masks some times", "value": "smoothed_pct_wear_mask_some_time_weighted"},
                    {"label": "People never wearing masks", "value": "smoothed_pct_wear_mask_none_time_weighted"}],
                multi=False,
                value="rolling_total_responses",
                style={"width": "60%"}
                ),
    
    html.Div(id="output_container", children=[]),
    html.Br(),
    
    dcc.Graph(id="my_covid_map", figure={})
    
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
    
    container = "The user chose {} for the gender and to display {}".format(ddgender, option)
    
    dff = df[(df["data_cat"]==option) & (df["gender"]==ddgender)]
    
    #Plotly Express
    fig = px.choropleth(
        data_frame = dff,
        locations="GID_0",
        color="amount",
        hover_name="country_agg",
        color_continuous_scale=px.colors.sequential.BuPu
    )
    
    return container, fig

#-------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server()

