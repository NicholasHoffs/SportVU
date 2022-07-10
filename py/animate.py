from matplotlib.axis import XAxis
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

from py.movement import velocity, acceleration

def animate_play(df, event_num):

    df = df[df['EVENT']==event_num]

    length = len(df)

    df.loc[:,'MOMENT_NUM'] = np.divmod(np.arange(length),11)[0]+1

    df.loc[:,'LOC_Z'] = df['LOC_Z']+1


    player_df = df[df['PLAYER_ID']!=-1]
    ball_df = df[df['PLAYER_ID']==-1]

    player_hover_data = ["LOC_X", "LOC_Y"]
    ball_hover_data = ["TEAM_ID", "PLAYER_ID"]
    webgl = None
    color_kwargs = {}

    # original code
    player_fig = px.scatter(
        player_df,
        x="LOC_X",
        y="LOC_Y",
        animation_frame="MOMENT_NUM",
        animation_group="PLAYER_ID",
        range_x=(-250,250),
        range_y=(-47.5, 422.5),
        hover_data=player_hover_data,
        render_mode="webgl" if webgl else "svg",
        size='LOC_Z',
        width=625, height=587.5,
        **color_kwargs
    )

    player_fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

    # original code
    ball_fig = px.scatter(
        ball_df,
        x="LOC_X",
        y="LOC_Y",
        animation_frame="MOMENT_NUM",
        animation_group="PLAYER_ID",
        range_x=(-250,250),
        range_y=(-47.5, 422.5),
        hover_data=ball_hover_data,
        size='LOC_Z',
        width=625, height=587.5,
        **color_kwargs
    )



    # build frames to be animated from two source figures.  Each frame has 2 traces
    frames = [
        go.Frame(data=f.data + player_fig.frames[i].data, name=f.name)
        for i, f in enumerate(ball_fig.frames)
    ]

    # increase duration as contour takes a while to redraw
    # increase duration as contour takes a while to redraw
    updmenus = [{"args": [None, {"frame": {"duration": 2000}}],"label": "&#9654;","method": "animate",},
                {'args': [[None], {'frame': {'duration': 0}, 'mode': 'immediate', 'fromcurrent': True, }],
                    'label': '&#9724;', 'method': 'animate'} ]

    # now can animate...
    fig=go.Figure(data=frames[0].data, frames=frames, layout=player_fig.layout).update_layout(
        updatemenus=[{"buttons":updmenus}]
    )

    import base64
    #set a local image as a background
    image_filename = 'court.png'
    plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

    fig.update_layout(
        xaxis = {                                     
                'showgrid': False,
                'showticklabels': False,
                'visible': False
                },
        yaxis = {                              
                'showgrid': False,
                'showticklabels': False,
                'visible': False
                },                                                                            
        images= [dict(
            source='data:image/png;base64,{}'.format(plotly_logo.decode()),
            xref="paper", yref="paper",
            x=0, y=1,
            xanchor="left",
            sizex=1,sizey=1,
            yanchor="top",
            sizing="stretch",
            layer="below")]
            )
    return fig

def animate_velocity(df, event_num):
    df = df[df['EVENT']==event_num]
    df = df[df['PLAYER_ID']==-1]

    vel = velocity(df['LOC_X'], df['LOC_Y'])

    fig = px.line(vel, height=250)

    return fig

def animate_acceleration(df, event_num):
    df = df[df['EVENT']==event_num]
    df = df[df['PLAYER_ID']==-1]

    acc = acceleration(df['LOC_X'], df['LOC_Y'])

    fig = px.line(acc, height=250)

    return fig