from py.animate import animate_play, animate_velocity, animate_acceleration
from py.movement import velocity, acceleration

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd

df = pd.read_csv('./data/merged_csv/0021500001.csv')

EVENT_NUM = 2

motion_fig = animate_play(df,EVENT_NUM,'first_figure')
velocity_fig = animate_velocity(df,EVENT_NUM)
acceleration_fig = animate_acceleration(df,EVENT_NUM)

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


    dbc.Row([  # start of second row

            dbc.Col([  # first column on second row
            html.H5('Court Visualization', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      figure=motion_fig),
            html.Hr(),
            ], width={'size': 4, 'offset': 0, 'order': 1}),  # width first column on second row

            dbc.Col([  # second column on second row
            html.H5('Movement Stats', className='text-center'),
            dcc.Graph(id='chrt-portfolio-velocity',
                      figure=velocity_fig),
            dcc.Graph(id='chrt-portfolio-acceleration',
                      figure=acceleration_fig),          
            html.Hr()
            ], width={'size': 6, 'offset': 0, 'order': 2}),  # width second column on second row

            dbc.Col([  # third column on second row
            html.H5('Play Description', className='text-center'),
            html.P(df[df['EVENT']==EVENT_NUM]['HOMEDESCRIPTION'].iloc[0],className='text-center'),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row
], fluid=True
)

#html.P((get_event_msg_type(df[df['EVENT']==2]['EVENTMSGTYPE'].iloc[0]),' by ', ''),className='text-center')

if __name__ == "__main__":
    app.run_server()