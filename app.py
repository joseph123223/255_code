from ast import In
from distutils.log import debug
from doctest import OutputChecker
from msilib.schema import Component
from turtle import color
from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('world_covid.csv')
df.sort_values('date',inplace=True)

Lastest_date = df['date'].max()
lastest_record = df[df['date'] == Lastest_date]

#top_comfirmed = lastest_record.sort_values('confirmed_cases',ascending = False)
#top10_states = top_comfirmed[:10]['countries_and_territories']
external_stylesheets = [dbc.themes.BOOTSTRAP]
pio.templates.default = "seaborn"

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(html.Div
            ([
                html.Br(),
                html.H1("World Covid-19 Data Analytics", style={'textAlign': 'center', "color": "#484891"}),
                html.P("World's Covid-19 data visualiztion results in 2020", style={'textAlign': 'center',"color": "#484891"})
            ])
        ))),
        dbc.Row(dbc.Col(
            html.Div([
                dcc.Dropdown(
                    df['countries_and_territories'].unique(),
                    id='countries_choose',
                    value = "United_States_of_America",
                    style={"width":"60%","margin": "auto"}
                ),
                html.Br(),
                html.Br()
            ])
        )),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    dcc.Graph(
                        id = 'the_graph3',
                        style={"width":"95%"}
                    )
                ])),
                dbc.Col(html.Div([
                    dcc.Graph(
                        id = 'the_graph_pie',
                        style={"width":"80%"}
                    ),
                    html.Br(),
                    html.Br()
                ])),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dcc.RadioItems(['Comfirmed Cases', 'Death cases'], 'Comfirmed Cases', inline=True, id='case_choose', labelStyle={'display': 'inline-block', 'marginLeft': '120px'}),
                        html.Br(),
                        dcc.RadioItems(['Total','Daily'], 'Total', inline=True, id='display_choose', labelStyle={'display': 'inline-block', 'marginLeft': '120px',"marginRight": "96px"}),
                        dcc.Graph(
                            id = 'the_graph',
                            style={"width":"100%"}
                        )
                    ])
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    dcc.Graph(
                        id = 'the_graph2',
                        style={"width":"99%"}
                    )
                ])),
                dbc.Col(html.Div([
                    dcc.Graph(
                        id = 'the_graph4',
                        style={"width":"99%"}
                    )
                ]))
            ]
        ),
    ]
)

#fig Comfirmed Cases
@app.callback(
    Output(component_id='the_graph', component_property = 'figure'),
    Input(component_id='countries_choose',component_property = 'value'),
    Input(component_id='case_choose',component_property = 'value'),
    Input(component_id='display_choose',component_property = 'value')
)
def update_graph(countries_choose,case_choose,display_choose):
    pio.templates.default = "seaborn"
    state = countries_choose
    cs = df[df["countries_and_territories"] == state]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if case_choose == "Comfirmed Cases":
        if display_choose == "Total":
            fig.add_trace(go.Scatter(x=cs.date, y=cs.confirmed_cases, name=state))
            fig.update_layout(title_text='<b>Comfirmed Cases over time 2020</b>', title_x=0.5, title_font_size = 22, title_font_color = "#484891")
        else:
            fig.add_trace(go.Scatter(x=cs.date, y=cs.daily_confirmed_cases, name=state))
            fig.update_layout(title_text='<b>Daily Comfirmed Cases 2020</b>', title_x=0.5, title_font_size = 22, title_font_color = "#467500")
        fig.update_yaxes(title_text="Number of Comfirmed Cases", secondary_y=False)
    else:
        if display_choose == "Total":
            fig.add_trace(go.Scatter(x=cs.date, y=cs.deaths, name=state))
            fig.update_layout(title_text='<b>Death Cases over time 2020</b>', title_x=0.5, title_font_size = 22, title_font_color = "#408080")
        else:
            fig.add_trace(go.Scatter(x=cs.date, y=cs.daily_deaths, name=state))
            fig.update_layout(title_text='<b>Daily Death Cases 2020</b>', title_x=0.5, title_font_size = 22, title_font_color = "#7E3D76")
        fig.update_yaxes(title_text="Number of Comfirmed Cases", secondary_y=False)
    return fig

#fig Comfirmed Cases - world map
@app.callback(
    Output(component_id='the_graph3', component_property = 'figure'),
    Input(component_id='countries_choose',component_property = 'value')
)
def update_graph(choose):
    state = choose
    pio.templates.default = "seaborn"
    cs = lastest_record[lastest_record["countries_and_territories"] == state]
    fig = px.choropleth(cs, locations="country_territory_code",
                    color= "confirmed_cases",
                    hover_name="countries_and_territories",
                    title='<b>Total Confirmed cases - World Map<b>',
                    projection = 'orthographic',
                    color_continuous_scale=px.colors.sequential.Oryel
    )
    fig.update_layout(
        title=dict(font=dict(size=18),x=0.5,xanchor='center'),
        margin=dict(l=60, r=60, t=50, b=50)
    )
    return fig

#fig Global Comfirmed Cases animation
@app.callback(
    Output(component_id='the_graph2', component_property = 'figure'),
    Input(component_id='countries_choose',component_property = 'value')
)
def update_graph(choose):
    pio.templates.default = "plotly"

    fig = px.scatter_geo(df,
        locations="country_territory_code", color="confirmed_cases",
        hover_name="countries_and_territories", size="confirmed_cases",
        animation_frame="date",
        projection="natural earth"
    )
    fig.update_layout(title_text='<b>Global Comfirmed Cases over time 2020</b>', title_x=0.5, title_font_color = "#484891")

    return fig

#fig month death cases
@app.callback(
    Output(component_id='the_graph4', component_property = 'figure'),
    Input(component_id='countries_choose',component_property = 'value')
)
def update_graph(choose):
    state = choose
    pio.templates.default = "plotly"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    cs = df[df["countries_and_territories"] == state]
    fig = px.histogram(cs,x=cs.date, y=cs.daily_deaths,  nbins = 12,  marginal="box", color_discrete_sequence=['indianred'])
    fig.update_layout(title_text='<b>Deaths Cases by Months</b>', title_x=0.5, bargap=0.1, title_font_color = "#484891")

    return fig

#fig pie chart
@app.callback(
    Output(component_id='the_graph_pie', component_property = 'figure'),
    Input(component_id='countries_choose',component_property = 'value')
)
def update_graph(choose):
    state = choose
    pio.templates.default = "seaborn"
    state_lastest_record = lastest_record[lastest_record["countries_and_territories"] == state]
    state_lastest_death = state_lastest_record['deaths']
    state_lastest_comfirmed = state_lastest_record['confirmed_cases']
    state_population = state_lastest_record['pop_data_2019']

    myvalues = [float(state_lastest_death),float(state_lastest_comfirmed),float(state_population)]
    mylabels = ["Death", "Confirmed cases", "Healthy"]
    fig = go.Figure(data=[go.Pie(labels=mylabels, values=myvalues)])
    fig.update_layout(
        title= "<b>Percentage - Pie Chart</b>",
        title_font_color = "#484891"
    )
    return fig

if __name__=="__main__":
    app.run_server(debug=True)