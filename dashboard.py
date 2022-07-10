from py.animate import animate_play, animate_velocity, animate_acceleration
from py.movement import velocity, acceleration

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd

df = pd.read_csv('./data/merged_csv/0021500001.csv')
df=df[df['EVENT']==3.0]
EVENT_NUM = 3

motion_fig = animate_play(df,EVENT_NUM)
velocity_fig = animate_velocity(df,EVENT_NUM)
acceleration_fig = animate_acceleration(df,EVENT_NUM)

url = 'https://cdn.nba.com/headshots/nba/latest/1040x760/201143.png'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

event_msg_type = ['Field Goal Made',
                  'Field Goal Missed',
                  'Free Throw Attempt',
                  'Rebound',
                  'Turnover',
                  'Foul',
                  'Violation',
                  'Substitution',
                  'Timeout',
                  'Jump Ball',
                  'Ejection',
                  'Start of Period',
                  'End of Period'
                  ]

def get_event_msg_type(event_msg_type_num):
    return event_msg_type[event_msg_type_num-1]

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2('SportVU Visualization', className='text-center text-primary, mb-3'))),

    dbc.Row([

            dbc.Col([  

                html.H5('Court Visualization', className='text-center'),
                dcc.Graph(id='chrt-portfolio-main',
                        figure=motion_fig),
                html.Hr(),

            ], width={'size': 4, 'offset': 0, 'order': 1}, style={"height":"100%"}),  

            dbc.Col([

                html.H5('Movement Stats', className='text-center'),
                html.H6('Velocity'),
                dcc.Graph(id='chrt-portfolio-velocity',
                        figure=velocity_fig),
                html.H6('Acceleration'),
                dcc.Graph(id='chrt-portfolio-acceleration',
                        figure=acceleration_fig),        

                html.Hr()

            ], width={'size': 6, 'offset': 0, 'order': 2},style={"height":"100%"}), 

            dbc.Col([  

                html.H5('Play Description', className='text-center'),

                html.Img(
                src="https://cdn.nba.com/headshots/nba/latest/1040x760/{}.png".format(df['PLAYER1_ID'].iloc[0]),
                width=208,height=152,
                style={
                    'height': '50%',
                    'width': '50%'
                }),

                html.P(df['HOMEDESCRIPTION'].iloc[0],className='text-center'),
                html.Hr()

            ], width={'size': 2, 'offset': 0, 'order': 3}, style={'textAlign': 'center',"height":"100%"}),  
        ]),  
], fluid=True,style={"height": "100vh"}, className='container-fluid'
)

#html.P((get_event_msg_type(df[df['EVENT']==2]['EVENTMSGTYPE'].iloc[0]),' by ', ''),className='text-center')

if __name__ == "__main__":
    app.run_server()