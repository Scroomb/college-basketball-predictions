import numpy as np
import pandas as pd
import scipy.stats as scs
import matplotlib.pyplot as plt

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

def get_per_values(years):
    df = pd.read_csv('data/' + years + '_PER.csv')
    df.dropna(inplace=True)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.set_index(['PLAYER','TEAM','YEAR'],inplace=True)
    return df

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

def get_per(df,years):
    players = make_player(df,years)
    teams = make_teams(df,players)
    return teams.loc[:,'PER']

def make_histograms(dfs):
    n_plts = int(len(dfs)/2)
    if n_plts %2 ==1:
        n_plts +=1
    fig,axs = plt.subplots(n_plts,2,figsize=(20,10))
    for n, ax in zip(dfs,axs.flatten()):
        n[0].plot(kind='hist',ax=ax)
        n[0].plot(kind='kde',ax=ax,secondary_y=True)
        ax.set_title(n[1])
    plt.suptitle('Yearly PER Distributions', size=14, y = 1.08)
    plt.tight_layout()
    plt.show()

def gen_ks_test(df):
    return scs.kstest(df.values,comp)

def check_normality(dfs):
    df_ks_vals = []
    for d in dfs:
        ks_val = gen_ks_test(d[0])
        df_ks_vals.append((d[1],ks_val))
    return df_ks_vals

if __name__ == '__main__':
    year_list = ['2006-2007','2007-2008','2008-2009','2009-2010','2010-2011',
                '2011-2012','2012-2013','2013-2014','2014-2015','2015-2016',
                '2016-2017','2017-2018']

    df1 = pd.read_csv('data/2006-2007_clean.csv')
    df2 = pd.read_csv('data/2007-2008_clean.csv')
    df3 = pd.read_csv('data/2008-2009_clean.csv')
    df4 = pd.read_csv('data/2009-2010_clean.csv')
    df5 = pd.read_csv('data/2010-2011_clean.csv')
    df6 = pd.read_csv('data/2011-2012_clean.csv')
    df7 = pd.read_csv('data/2012-2013_clean.csv')
    df8 = pd.read_csv('data/2013-2014_clean.csv')
    df9 = pd.read_csv('data/2014-2015_clean.csv')
    df10 = pd.read_csv('data/2015-2016_clean.csv')
    df11 = pd.read_csv('data/2016-2017_clean.csv')
    df12 = pd.read_csv('data/2017-2018_clean.csv')

    df1_per = get_per(df1,'2006-2007')
    df2_per = get_per(df2,'2007-2008')
    df3_per = get_per(df3,'2008-2009')
    df4_per = get_per(df4,'2009-2010')
    df5_per = get_per(df5,'2010-2011')
    df6_per = get_per(df6,'2011-2012')
    df7_per = get_per(df7,'2012-2013')
    df8_per = get_per(df8,'2013-2014')
    df9_per = get_per(df9,'2014-2015')
    df10_per = get_per(df10,'2015-2016')
    df11_per = get_per(df11,'2016-2017')
    df12_per = get_per(df12,'2017-2018')

    dfs = [(df1_per,'2006-2007'),(df2_per,'2007-2008'),(df3_per,'2008-2009'),
            (df4_per,'2009-2010'),(df5_per,'2010-2011'),(df6_per,'2011-2012'),
            (df7_per,'2012-2013'),(df8_per,'2013-2014'),(df9_per,'2014-2015'),
            (df10_per,'2015-2016'),(df11_per,'2016-2017'),(df12_per,'2017-2018')]

    make_histograms(dfs)
    #KS Test, null hypothesis is distributions are equal.  Comparing data to normal.
    #ks_vals = check_normality(dfs)
    #p_values < 0.05 reject null, thus non non-normal,
    #Use Kruskal-Wallis H-test to compare
    #Null hypothesis that the population median of all of the groups are equal.






    # Mann–Whitney U test (also called the Mann–Whitney–Wilcoxon (MWW), Wilcoxon
    # rank-sum test, or Wilcoxon–Mann–Whitney test) is a nonparametric test of the
    # null hypothesis that it is equally likely that a randomly selected value from
    # one sample will be less than or greater than a randomly selected value from a
    # second sample.  The alternative hypothesis is that

    #scs.mannwhitneyu(df1_per.values,df11_per.values,alternative='less')
    #MannwhitneyuResult(statistic=54985.0, pvalue=0.04323639531512454)
    #since p_value (0.043) is less than alpha of 0.05 we will reject our null hypothes is that it
    #equally likely a randomly selected mean PER from 2006-2007 will be less than a
    #randomly selected mean PER from 2016-2017.  Thus the mean PER from 2006-2007 tends to be
    #less than the mean PER from 2016-2017.  AKA mean PER has generally increased from 2006-2007
    #to 2016-2017.
