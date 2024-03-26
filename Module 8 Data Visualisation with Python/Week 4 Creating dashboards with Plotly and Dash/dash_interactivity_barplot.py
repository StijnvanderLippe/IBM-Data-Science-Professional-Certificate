# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into the pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Create a dash application
app = dash.Dash(__name__)


app.layout = html.Div([html.H1('Total number of flights to the destination state split by reporting airline',
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                html.Div(['Input year: ', dcc.Input(id='input-year', value='2010', type='number', style={'height': '50px', 'font-size': 35})],
                style={'font-size': 40}),
                html.Div(['Graph', dcc.Graph(id='bar-plot')])
                ])

@app.callback(Output('bar-plot', 'figure'),
              Input('input-year', 'value'))
def update_plot(input_year):
    df_plot = airline_data[airline_data['Year'] == int(input_year)].groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    fig = px.bar(df_plot, x='DestState', y='Flights', color='Reporting_Airline', title='Total number of flights to the destination state split by reporting airline')
    return fig

if __name__ == '__main__':
    app.run_server()
