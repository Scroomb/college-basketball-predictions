import pandas as pd
import re



def split_mo(df):
    dates = pd.DataFrame(df['DATE'].str.split('-').tolist(),
        columns=['Year','Month','Day'])
    df = pd.concat([df,dates],axis=1)

def clean_data(df):
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.loc[:,'TEAM'] = df.loc[:,'TEAM'].apply(lambda x: re.sub('\n','',x))
    df.loc[:,'MATCH'] = df.loc[:,'MATCH'].apply(lambda x: re.sub('\n','',x))

if __name__ == '__main__':
    yr_16_17 = pd.read_csv('../smarter-than-nate-silver/data/2016-2017_gamedata.csv')
    clean_data(yr_16_17)
