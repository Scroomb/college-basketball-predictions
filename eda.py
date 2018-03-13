import pandas as pd
import re


def split_data(df):
    dates = pd.DataFrame(df['DATE'].str.split('-').tolist(),
        columns=['Year','Month','Day'])
    three_point = pd.DataFrame(df['3PM-A'].str.split('-').tolist(),
        columns=['3P','3PA']).astype('int64')
    field_goal = pd.DataFrame(df['FGM-A'].str.split('-').tolist(),
        columns=['FG','FGA']).astype('int64')
    free_throw = pd.DataFrame(df['FTM-A'].str.split('-').tolist(),
        columns=['FT','FTA']).astype('int64')
    time = pd.DataFrame(df['MIN'].str.split(':').tolist(),
        columns=['MINS','SECS']).astype('int64')
    #df = pd.concat([df,dates],axis=1)
    df_out = pd.concat([df,three_point,field_goal,free_throw,time],axis=1)
    return df_out

def clean_data(df):
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.loc[:,'TEAM'] = df.loc[:,'TEAM'].apply(lambda x: re.sub('\n','',x))
    df.loc[:,'MATCH'] = df.loc[:,'MATCH'].apply(lambda x: re.sub('\n','',x))
    games = df['MATCH'].unique()
    drp_vals = []
    for x in games:
        if df[df['MATCH']==x]['TEAM'].nunique()==1:
            drp_vals.append(x)
    return df[~df['MATCH'].isin(drp_vals)]
if __name__ == '__main__':
    yr_16_17 = pd.read_csv('../smarter-than-nate-silver/data/2016-2017_gamedata.csv')
    yr_16_17 = clean_data(yr_16_17)
    yr_16_17 = split_data(yr_16_17)
