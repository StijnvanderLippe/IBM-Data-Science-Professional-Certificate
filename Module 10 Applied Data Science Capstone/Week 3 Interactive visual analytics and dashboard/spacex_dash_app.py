# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

print(os.getcwd())

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
locations = ['All sites'] + spacex_df['Launch Site'].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(options=locations, placeholder='Select a Launch Site here', value='All sites', id='site-dropdown'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=min_payload, max=max_payload, value=[min_payload, max_payload], step=1000, id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'All sites':
        pie_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(pie_df, names='Launch Site', values='class', title='Number of succesful launches per launch site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Distribution of launches for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, selected_payload):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > selected_payload[0]) & (spacex_df['Payload Mass (kg)'] < selected_payload[1])]
    if selected_site == 'All sites':
        filtered_df = filtered_df
        title = 'Launch success by payload mass'
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        title = f'Launch success by payload mass for site {selected_site}'
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
