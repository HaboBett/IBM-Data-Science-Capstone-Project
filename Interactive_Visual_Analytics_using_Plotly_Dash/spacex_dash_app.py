# Import required libraries
import pandas as pd
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
payload = sorted(set(spacex_df['Payload Mass (kg)']))
# Create a dash application
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.COSMO])

# Create an app layout
app.layout = html.Div(children=[html.H1([html.B('SpaceX Launch Records Dashboard')],
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dbc.Label([html.B('Select Launch Site(s):')]),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                             placeholder='Select site',
                                             value='ALL',
                                             searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                dbc.Label([html.B("Payload range (Kg):")]),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={mark: {'label': mark, 'style': {'fontWeight': 'bold'}}
                                                       for mark in range(0, 10000, 2500)
                                                }

                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ], style={'backgroundColor':'#FAF0DC'})

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, names='Launch Site', values='class', title='<b>Launch success rate by Launch Site</b>', hover_name='Launch Site')
        fig.layout.paper_bgcolor='#FAF0DC'
        fig.layout.plot_bgcolor='#FAF0DC'
        return fig
    else:
        new_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['class'], as_index=False).size().rename(columns={'size':'Launches'})
        fig = px.pie(new_df, names='class', values='Launches', title=f'<b>Proportion of successful and failed launches in {entered_site}</b>')
        fig.layout.paper_bgcolor='#FAF0DC'
        fig.layout.plot_bgcolor='#FAF0DC'
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id= 'success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(site, val_range):
    if site == 'ALL':
        scatter_df = spacex_df[spacex_df['Payload Mass (kg)'].isin(list(range(val_range[0], val_range[1] + 1)))]
        fig = px.scatter(scatter_df, x='Payload Mass (kg)', y='class', color='Booster Version', title='<b>Correlation between Payload mass and Success</b>', size=[30]*len(scatter_df), size_max=15, hover_name='Booster Version')
        fig.layout.paper_bgcolor='#FAF0DC'
        fig.layout.plot_bgcolor='#FAF0DC'
        return fig
    else:
        scatter_df = spacex_df[(spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'].isin(list(range(val_range[0], val_range[1] + 1))))]
        fig = px.scatter(scatter_df, x='Payload Mass (kg)', y='class', color='Booster Version', title=f'<b>Correlation between Payload mass and Success in {site}</b>', size=[30]*len(scatter_df), size_max=15, hover_name='Booster Version')
        fig.layout.paper_bgcolor='#FAF0DC'
        fig.layout.plot_bgcolor='#FAF0DC'
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
