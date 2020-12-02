import pandas as pd

import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

# ------------------------------------------------------------

#dfs_country = functions.functions_data.get_data("dash_data/country/smooth/", "country")
#countries = pd.concat(dfs_country, ignore_index=True)
#countries = functions.functions_data.insert_month(countries)
countries = pd.read_csv("dash_data/countries_dash.csv.gzip", compression="gzip")
df = countries[countries["age_bucket"]=="overall"]
df = df[df["date"]=="2020-07-16"]
df = df.groupby(["country_agg", "GID_0","gender", "date"])[["rolling_total_responses","smoothed_pct_cli_weighted"]].mean()

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
                    {"label": "Number of responses", "value": "rolling_total_responses"},
                    {"label": "Individuals with COVID-like illness", "value": "smoothed_pct_cli_weighted"}],
                multi=False,
                value="rolling_total_responses",
                style={"width": "40%"}
                ),
    
    html.Div(id="ouput_container", children=[]),
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
def update_graph(option_slct1, option_slct2):
    print(option_slct1, option_slct2)
    print(type(option_slct1, option_slct2))
    
    container = "The user chose {} for the gender and to display {}".format(option_slct1, option_slct2)
    
    dff = df.copy
    dff = dff[dff["gender"]==option_slct1]
    dff = dff[option_slct2]
    
    #Plotly Express
    fig = px.choropleth(
        data_frame = dff,
        locations="GID_0",
        color=option_slct2,
        hover_name="country_agg",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    return container, fig

#-------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server()

