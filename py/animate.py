from matplotlib.axis import XAxis
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os


def animate_play(game_csv_path, event_num,figure_save_name):

    df=pd.read_csv(game_csv_path)
    df = df[df['EVENT']==event_num]

    df['MOMENT_NUM'] = np.divmod(np.arange(len(df)),11)[0]+1

    df['LOC_Z'] = df['LOC_Z']+1

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
        range_x=(0.0, 100.0),
        range_y=(0.0, 50.0),
        hover_data=player_hover_data,
        render_mode="webgl" if webgl else "svg",
        size='LOC_Z',
        **color_kwargs
    )

    # original code
    ball_fig = px.scatter(
        ball_df,
        x="LOC_X",
        y="LOC_Y",
        animation_frame="MOMENT_NUM",
        animation_group="PLAYER_ID",
        range_x=(0.0, 100.0),
        range_y=(0.0, 50.0),
        hover_data=ball_hover_data,
        size='LOC_Z',
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
    image_filename = 'index.jpg'
    plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

    fig.update_layout(
        xaxis = {                                     
                'showgrid': False
                },
        yaxis = {                              
            'showgrid': True
                },                                                                            
        images= [dict(
            source='data:image/jpg;base64,{}'.format(plotly_logo.decode()),
            xref="paper", yref="paper",
            x=0, y=1,
            sizex=1, sizey=1,
            xanchor="left",
            yanchor="top",
            sizing="stretch",
            layer="below")])
    fig.write_html('./plotly_figures/{}.html'.format(figure_save_name), auto_open=True)

animate_play('./data/motion_csv/0021500001.csv', 2, 'first_figure')
