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
    
    dcc.Dropdown(id="data",
                options=[
                    {"label": "Total cases per million", "value": "total_cases_per_million"},
                    {"label": "Total deaths per million", "value": "total_deaths_per_million"},
                    {"label": "Median Age", "value": "median_age"},
                    {"label": "Human Development Index", "value": "hdi"}],
                multi=False,
                value="total_cases_per_million",
                style={"width": "40%"}
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
        locations="iso_code",
        color="amount",
        hover_name="country_agg",
        animation_frame = "date",
        projection = "natural earth",
        color_continuous_scale=["white", "#00c5ff", "#00287f", "#00151f"]
    )
    
    return container, fig

#-------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server()

