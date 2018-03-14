import pandas as pd
import re
import per
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def split_data(df):
    date = pd.DataFrame(df['DATE'].str.split('-').tolist(),
        columns=['YEAR','MONTH','DAY']).astype('int64')
    date.drop(['MONTH','DAY'],axis=1,inplace=True)
    three_point = pd.DataFrame(df['3PM-A'].str.split('-').tolist(),
        columns=['3P','3PA']).astype('int64')
    field_goal = pd.DataFrame(df['FGM-A'].str.split('-').tolist(),
        columns=['FG','FGA']).astype('int64')
    free_throw = pd.DataFrame(df['FTM-A'].str.split('-').tolist(),
        columns=['FT','FTA']).astype('int64')
    time = pd.DataFrame(df['MIN'].str.split(':').tolist(),
        columns=['MINS','SECS']).astype('int64')
    time.drop(['SECS'],axis=1,inplace=True)
    df_out = pd.concat([df,three_point,field_goal,free_throw,date,time],axis=1)
    return df_out

def clean_data(df):
    df.drop(['Unnamed: 0'],axis=1,inplace=True)
    if '3PM-A' in df.columns and '3GM-A' in df.columns:
        df['3GM-A'] =df['3GM-A'].fillna(df[~df['3PM-A'].isnull()]['3PM-A'])
        df.drop(['3PM-A'],axis=1,inplace=True)
    df.loc[:,'TEAM'] = df.loc[:,'TEAM'].apply(lambda x: re.sub('\n','',x))
    df.loc[:,'MATCH'] = df.loc[:,'MATCH'].apply(lambda x: re.sub('\n','',x))
    df= df.rename(index=str,columns={'3GM-A':'3PM-A'})
    df.reset_index()
    games = df['MATCH'].unique()
    drp_vals = []
    for x in games:
        if df[df['MATCH']==x]['TEAM'].nunique()==1:
            drp_vals.append(x)
    df_out = df[~df['MATCH'].isin(drp_vals)].reset_index()
    df_out.dropna(inplace=True)
    return df_out

def make_player(df,year):
    df.dropna(inplace=True)
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
    player_tot = player_tot[player_tot['GAMES']/df.groupby('TEAM')['MATCH'].nunique()>0.50]
    player_tot['YEAR']=year
    player_tot.set_index(['YEAR'],append=True,inplace=True)
    player_per = get_per_values(year)
    player_tot = pd.concat([player_tot,player_per],axis=1)
    return player_tot

def get_and_clean_file(years):
    df = pd.read_csv('data/' + years + '_gamedata.csv')
    df = clean_data(df)
    df = split_data(df)
    df.to_csv('data/' + years + '_clean.csv')
    #return df

def get_clean_file(years):
    df = pd.read_csv('data/' + years + '_clean.csv')
    df.dropna(inplace=True)
    return df

def get_per_values(years):
    df = pd.read_csv('data/' + years + '_PER.csv')
    df.dropna(inplace=True)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.set_index(['PLAYER','TEAM','YEAR'],inplace=True)
    return df

def corr_heat(df,year):
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(12, 12))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5},xticklabels=corr.index, yticklabels=corr.columns)
    plt.xticks(rotation=60, ha="right")
    plt.yticks(rotation=0)
    ax.set_title(year + " Correlation Matrix")
    plt.savefig( 'figs/' + year + '_Correlation_Matrix.png')

def make_teams(df,players):
    pl1 = players.reset_index()
    teams = pl1.groupby('TEAM').sum()
    t1 = teams.drop('PER',axis=1)
    for x in t1.columns:
        t1[x] = t1[x]/df.groupby(['TEAM'])['MATCH'].nunique()
    t1p = teams['PER']
    t1p = t1p/pl1.groupby('TEAM')['PLAYER'].count()
    team_out = pd.concat([t1,t1p],axis=1)
    team_out.drop(['MINS','GAMES'],axis=1,inplace=True)
    team_out.rename(index=str,columns={0:'PER'},inplace=True)
    return team_out

def make_per_files(year_list):
    for x in year_list:
        print(f'Getting PER for {x}')
        df = get_clean_file(x)
        df.dropna(inplace=True)
        players = make_player(df,x)

        league_pace = per.league_pace_fn(df)
        league_uPER = np.mean(per.league_uPER(df,players.index.values))

        play_PER = []
        for y in players.index.values:
            play_PER.append([y[0],y[1],y[2],
                per.PER(df,y[0],y[1],league_uPER,league_pace)])
        play_PER_df = pd.DataFrame(play_PER,columns=['PLAYER','TEAM','YEAR','PER'])
        play_PER_df.to_csv('data/'+x+'_PER.csv')
        print(f'PER generated for {x}')

def make_games(df,years):
    games = []
    for d in df['DATE'].unique():
        for g in df[df['DATE']==d]['MATCH'].unique():
            scores = df[df['MATCH']==g].groupby('TEAM')['PTS'].sum()
            games.append([g,d,scores[0]-scores[1]])
    games_df = pd.DataFrame(games,columns=['MATCH','DATE','PT_DIFF'])
    games_df.to_csv('data/' + years + '_games.csv')
    return games_df

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

if __name__ == '__main__':
    year_list = ['2006-2007','2007-2008','2008-2009','2009-2010','2010-2011',
                '2011-2012','2012-2013','2013-2014','2014-2015','2015-2016',
                '2016-2017','2017-2018']
    #year_list = ['2008-2009','2009-2010','2010-2011',
                # '2011-2012','2012-2013','2014-2015','2015-2016',
                # '2016-2017','2017-2018']
    years = '2006-2007'
    df = get_clean_file(years)
    df.dropna(inplace=True)
    games = make_games(df,years)
    all_data = make_data(games)

    # for years in year_list:
    #     df = get_clean_file(years)
    #     df.dropna(inplace=True)
    #     # players = make_player(df,years)
    #     # teams = make_teams(df,players)
    #     games = make_games(df,years)
