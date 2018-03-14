import pandas as pd
import re
import per
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import eda

def make_data(df):
    col_h =['H_index', 'HOME', 'H_A', 'H_BLK', 'H_DEF', 'H_OFF', 'H_PF', 'H_PTS',
    'H_STL', 'H_TO', 'H_TOT', 'H_3P', 'H_3PA', 'H_FG', 'H_FGA', 'H_FT', 'H_FTA', 'H_PER']
    col_a = ['A_index', 'AWAY', 'A_A', 'A_BLK', 'A_DEF', 'A_OFF', 'A_PF', 'A_PTS',
    'A_STL', 'A_TO', 'A_TOT', 'A_3P', 'A_3PA', 'A_FG', 'A_FGA', 'A_FT', 'A_FTA', 'A_PER']
    cols = ['index', 'TEAM', 'A', 'BLK', 'DEF', 'OFF', 'PF', 'PTS', 'STL', 'TO',
           'TOT', '3P', '3PA', 'FG', 'FGA', 'FT', 'FTA', 'PER']

    cnvt_dict_h = dict(zip(cols,col_h))
    cnvt_dict_a = dict(zip(cols,col_a))
    out_cols = ['MATCH', 'DATE', 'PT DIFF', 'HOME', 'AWAY', 'H_index', 'H_A', 'H_BLK',
           'H_DEF', 'H_OFF', 'H_PF', 'H_PTS', 'H_STL', 'H_TO', 'H_TOT', 'H_3P',
           'H_3PA', 'H_FG', 'H_FGA', 'H_FT', 'H_FTA', 'H_PER', 'A_index', 'A_A',
           'A_BLK', 'A_DEF', 'A_OFF', 'A_PF', 'A_PTS', 'A_STL', 'A_TO', 'A_TOT',
           'A_3P', 'A_3PA', 'A_FG', 'A_FGA', 'A_FT', 'A_FTA', 'A_PER']
    all_data = pd.DataFrame(columns=out_cols)
    for m in df['MATCH']:
        hm_aw = df[df['MATCH']==m][['HOME','AWAY']].values
        home = t1[t1['TEAM']==hm_aw[0][0]].reset_index()
        home.rename(index=str,columns=cnvt_dict_h,inplace=True)
        away = t1[t1['TEAM']==hm_aw[0][1]].reset_index()
        away.rename(index=str,columns=cnvt_dict_a,inplace=True)
        hm_aw_stats = home.join(away,how='outer')
        out = df[df['MATCH']==m]
        for key,value in hm_aw_stats.iteritems():
            out.loc[:,key]=value.values[0]
        all_data = pd.concat([all_data,out])
    return all_data
