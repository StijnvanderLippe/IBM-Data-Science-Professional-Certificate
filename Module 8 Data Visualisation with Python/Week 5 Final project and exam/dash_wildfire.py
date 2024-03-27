# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')
# Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

regions_list = df['Region'].unique()
years_list = list(range(2005, 2021))

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div([html.H1('Australia Wildfire Dashboard', style={'textAlign': 'center', 'font-size': 50}),
                       html.Div([html.H2('Select Region:'), 
                                 dcc.RadioItems(regions_list, value=regions_list[0], id='input-region', inline=True), 
                                 html.H2('Select Year:'), 
                                 dcc.Dropdown(years_list, value=years_list[0], id='input-year')]),
                       html.Div([dcc.Graph(id='pie-plot'), 
                                 dcc.Graph(id='bar-plot')], 
                                 style={'display': 'flex'})
                       ])


@app.callback([Output('pie-plot', 'figure'),
               Output('bar-plot', 'figure')],
               [Input('input-region', 'value'),
                Input('input-year', 'value')])
def update_plots(input_region, input_year):
    df_pie = df[(df['Year'] == input_year) & (df['Region'] == input_region)].groupby('Month')['Estimated_fire_area'].mean().reset_index()
    df_bar = df[(df['Year'] == input_year) & (df['Region'] == input_region)].groupby('Month')['Count'].sum()

    fig_pie = px.pie(df_pie, names='Month', values='Estimated_fire_area', title=f'{input_region}: Monthly Average Estimated Fire Area in Year {input_year}')
    fig_bar = px.bar(df_bar, title=f'{input_region}: Average Count of Pixels for Presumed Vegetation Fires in Year {input_year}')

    return fig_pie, fig_bar

if __name__ == '__main__':
    app.run_server()