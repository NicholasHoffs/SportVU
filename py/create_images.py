import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def make_image(x,y, outputname, size=(1, 1), dpi=80):
    print(outputname)
    ax = plt.subplot()
    ax.plot(x,y)
    plt.axis('off')
    plt.savefig("./data/images/{}.png".format(outputname), bbox_inches='tight')
    plt.clf()

def create_images(game_data_path):
    
    for root, dirs, files in os.walk(game_data_path):
        for filename in files:
            orig = filename.replace('.csv','')
            filename = os.path.join(root, filename)
            df = pd.read_csv(filename)

            df = df[df['PLAYER1_ID']==df['PLAYER_ID']]
            df = df[df['EVENTMSGTYPE']==2]

            df.groupby('EVENT').apply(lambda x: make_image(x['LOC_X'],x['LOC_Y'],'{}-{}'.format(orig,int(x['EVENT'].values[0]))))

create_images('./data/merged_csv/')