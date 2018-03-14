import pandas as pd
import re
import per
import matplotlib.pyplot as plt

def split_data(df):
    three_point = pd.DataFrame(df['3PM-A'].str.split('-').tolist(),
        columns=['3P','3PA']).astype('int64')
    field_goal = pd.DataFrame(df['FGM-A'].str.split('-').tolist(),
        columns=['FG','FGA']).astype('int64')
    free_throw = pd.DataFrame(df['FTM-A'].str.split('-').tolist(),
        columns=['FT','FTA']).astype('int64')
    time = pd.DataFrame(df['MIN'].str.split(':').tolist(),
        columns=['MINS','SECS']).astype('int64')
    time.drop(['SECS'],axis=1,inplace=True)
    df_out = pd.concat([df,three_point,field_goal,free_throw,time],axis=1)
    return df_out

def clean_data(df):
    df.drop(['Unnamed: 0'],axis=1,inplace=True)
    if '3PM-A' in df.columns and '3GM-A' in df.columns:
        df['3GM-A'] =df['3GM-A'].fillna(df[~df['3PM-A'].isnull()]['3PM-A'])
        df.drop(['3PM-A'],axis=1,inplace=True)
    df.loc[:,'TEAM'] = df.loc[:,'TEAM'].apply(lambda x: re.sub('\n','',x))
    df.loc[:,'MATCH'] = df.loc[:,'MATCH'].apply(lambda x: re.sub('\n','',x))
    df= df.rename(index=str,columns={'3GM-A':'3PM-A'})
    #df.dropna(inplace=True)
    df.reset_index()
    games = df['MATCH'].unique()
    drp_vals = []
    for x in games:
        if df[df['MATCH']==x]['TEAM'].nunique()==1:
            drp_vals.append(x)
    df_out = df[~df['MATCH'].isin(drp_vals)].reset_index()
    return df_out

def make_player(df):
    if 'Unnamed: 0' in df.columns:
        df.drop(['Unnamed: 0'],axis=1,inplace=True)
    if 'index' in df.columns:
        df.drop(['index'],axis=1,inplace=True)
    player_tot = df.groupby(['PLAYER','TEAM']).sum()
    player_tot.reset_index(inplace=True)
    player_tot.set_index(['PLAYER','TEAM'],inplace=True)
    games = df.groupby(['PLAYER','TEAM'])['MATCH'].count()
    player_tot = pd.concat([player_tot,games],axis=1)
    player_tot.rename(index=str, columns={'MATCH':'GAMES'}, inplace=True)
    player_tot = player_tot[player_tot['MINS']/player_tot['GAMES'] > 7.0]
    return player_tot

def get_clean_file(years):
    df = pd.read_csv('data/' + years + '_gamedata.csv')
    df = clean_data(df)
    df = split_data(df)
    df.to_csv('data/' + years + '_clean.csv')
    #return df

if __name__ == '__main__':
    # yr_16_17 = pd.read_csv('data/2016-2017_gamedata.csv')
    # yr_16_17 = clean_data(yr_16_17)
    # yr_16_17 = split_data(yr_16_17)
    #
    # yr_16_17.to_csv('data/16_17_clean.csv')
    year_list = ['2006-2007','2007-2008','2009-2010','2010-2011','2011-2012',
                '2012-2013','2013-2014','2014-2015','2015-2016','2016-2017',
                '2017-2018']
    for x in year_list:
       get_clean_file(x)

    # yr_16_17 = pd.read_csv('data/16_17_clean.csv')
    # yr_16_17.drop(['Unnamed: 0'],axis=1,inplace=True)
    # player_tot_16_17 = yr_16_17.groupby(['PLAYER','TEAM']).sum()
    # player_tot_16_17.drop(['SECS'],axis=1,inplace=True)
    # player_tot_16_17.reset_index(inplace=True)
    # player_tot_16_17.set_index(['PLAYER','TEAM'],inplace=True)
    # games = yr_16_17.groupby(['PLAYER','TEAM'])['MATCH'].count()
    # player_tot_16_17 = pd.concat([player_tot_16_17,games],axis=1)
    # player_tot_16_17.rename(index=str, columns={'MATCH':'GAMES'}, inplace=True)
    # player_tot_16_17 = player_tot_16_17[player_tot_16_17['MINS']/player_tot_16_17['GAMES'] > 7.0]

    # player_tot_16_17 = make_player(yr_16_17)

    # league_uPER = per.league_uPER(yr_16_17,
    # play_PER = []
    # for x in player_tot_16_17.index.values:
    #     play_PER.append([x[0],x[1],per.PER(yr_16_17,x[0],x[1])])
