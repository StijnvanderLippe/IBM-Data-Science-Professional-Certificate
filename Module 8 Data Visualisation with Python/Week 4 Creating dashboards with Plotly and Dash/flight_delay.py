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

app.layout = html.Div([html.H1('Flight delay time statistics', style={'textAlign': 'center', 'font-size': 50}),
                    html.Div(dcc.Input(id='input-year', value='2010', type='numeric', style={'height': '50px', 'font-size': 35})),
                    html.Div([dcc.Graph(id='carrier-delay-plot'), dcc.Graph(id='weather-delay-plot')], style={'display': 'flex'}),
                    html.Div([dcc.Graph(id='NAS-delay-plot'), dcc.Graph(id='security-delay-plot')], style={'display': 'flex'}),
                    html.Div(dcc.Graph(id='aircraft-delay-plot'), style={'width': '65%'})]
)


def get_df(input_year):
    df_year_filtered = airline_data[airline_data['Year'] == int(input_year)]
    df = df_year_filtered.groupby(['Month', 'Reporting_Airline']).mean(numeric_only=True)[['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']].reset_index()
    return df


@app.callback([Output('carrier-delay-plot', 'figure'),
            Output('weather-delay-plot', 'figure'),
            Output('NAS-delay-plot', 'figure'),
            Output('security-delay-plot', 'figure'),
            Output('aircraft-delay-plot', 'figure')],
            Input('input-year', 'value'))
def update_plots(input_year):
    df = get_df(input_year)

    fig_carrier = px.line(df, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrier delay time (minutes) by airline')
    fig_weather = px.line(df, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
    fig_NAS = px.line(df, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
    fig_security = px.line(df, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
    fig_aircraft = px.line(df, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')

    return fig_carrier, fig_weather, fig_NAS, fig_security, fig_aircraft


if __name__ == '__main__':
    app.run_server()