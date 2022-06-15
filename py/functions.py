import json
import numpy as np
import pandas as pd
import os

import warnings
warnings.filterwarnings('ignore')

def json_2_csv(game_path):

    #LOAD JSON DATA
    data = json.load(open(game_path))

    game_id = data['gameid']

    full_df=[]

    for event in range(len(data['events'])):

        moments = data['events'][event]['moments']

        lengths = np.array([len(x[5]) for x in moments])

        if len(lengths)==0:
            continue
        if np.all(lengths == lengths[0])==False:
            continue

        game_clock = np.array([moment[2] for moment in moments])
        shot_clock = np.array([moment[3] for moment in moments])

        motion = np.array([np.array(moment[5]) for moment in moments])

        motion=np.reshape(motion,newshape=(motion.shape[0]*motion.shape[1],5))

        event_col = np.full(shape=(len(motion),1),fill_value=(event+1))
        # game_clock_arr = np.full(shape=(len(motion),1),fill_value=(game_clock))
        game_clock = np.reshape(np.repeat(game_clock,11),newshape=(-1,1))
        # shot_clock_arr = np.full(shape=(len(motion),1),fill_value=(shot_clock))
        shot_clock = np.reshape(np.repeat(shot_clock,11),newshape=(-1,1))

        df = np.hstack((event_col,motion,game_clock,shot_clock))
        
        full_df.append(df)

    #Regular python list to array
    full_df=np.array(full_df)
    #Stack all the columns into one big 2d array
    full_df = np.vstack(full_df)

    #Convert to DataFrame
    full_df=pd.DataFrame(full_df,columns=['EVENT','TEAM_ID','PLAYER_ID','LOC_X','LOC_Y','LOC_Z','GAME_CLOCK','SHOT_CLOCK'])

    return full_df, game_id

def save_DataFrame(DataFrame,file_path):
    pd.DataFrame.to_csv(DataFrame,file_path)

def bulk_conversion(games_json_path, save_path):

    for filename in os.listdir(games_json_path):
        new_name = filename.replace('.json','.csv')
        print('Converting ', filename, ' to ', new_name)
        df,game_id = json_2_csv(games_json_path+filename)
        save_DataFrame(df, save_path+game_id+'.csv')

bulk_conversion('./data/json/','./data/motion_csv/')