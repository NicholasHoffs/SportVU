import pandas as pd
import numpy as np

import json
import os

from court_convert import half_full_to_half, full_to_half_full

def save_DataFrame(DataFrame,file_path):
    pd.DataFrame.to_csv(DataFrame,file_path,index=False)

def conversion(game_path):

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
        game_clock = np.reshape(np.repeat(game_clock,11),newshape=(-1,1))
        shot_clock = np.reshape(np.repeat(shot_clock,11),newshape=(-1,1))

        df = np.hstack((event_col,motion,game_clock,shot_clock))
        
        full_df.append(df)

    #Regular python list to array
    full_df=np.array(full_df)
    #Stack all the columns into one big 2d array
    full_df = np.vstack(full_df)

    #Convert to DataFrame
    full_df=pd.DataFrame(full_df,columns=['EVENT','TEAM_ID','PLAYER_ID','LOC_X','LOC_Y','LOC_Z','GAME_CLOCK','SHOT_CLOCK'])

    # full_df = full_to_half_full(full_df)
    # full_df = half_full_to_half(full_df)

    return full_df, game_id

def merge(motion_path, pbp_path):
    motion_df = pd.read_csv(motion_path)
    pbp_df = pd.read_csv(pbp_path)

    pbp_df.rename(columns={'EVENTNUM':'EVENT'}, inplace=True)
    pbp_df = pbp_df[['EVENT','EVENTMSGTYPE','EVENTMSGACTIONTYPE','PLAYER1_ID','PLAYER1_NAME','HOMEDESCRIPTION','VISITORDESCRIPTION']]

    df=pd.merge(motion_df,pbp_df,how='inner',on='EVENT')

    return df

def bulk_conversion(games_json_path, save_path):

    for filename in os.listdir(games_json_path):
        new_name = filename.replace('.json','.csv')
        print('Converting ', filename, ' to ', new_name)
        df,game_id = conversion(games_json_path+filename)
        save_DataFrame(df, save_path+game_id+'.csv')

def bulk_merge(motion_paths, pbp_paths, save_path):
    count=1
    
    _, _, files = next(os.walk(motion_paths))
    file_count = len(files)
    for motion_name in os.listdir(motion_paths):
        for pbp_name in os.listdir(pbp_paths):
            if motion_name==pbp_name:
                print('Merging ', motion_name, '--- {} out of {}'.format(count, file_count))
                save_DataFrame(merge(motion_paths+'/'+motion_name,pbp_paths+'/'+pbp_name),save_path+motion_name)
                count += 1
                print('Done.')

# bulk_conversion('./data/json/', './data/motion_csv/')
bulk_merge('./data/motion_csv/', './data/pbp/', './data/merged_csv/')