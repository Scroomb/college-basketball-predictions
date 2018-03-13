
def VOP_fn(df):
    lg_PTS = df['PTS'].sum()
    lg_FGA = df['FGA'].sum()
    lg_ORB = df['OFF'].sum()
    lg_TOV = df['TO'].sum()
    lg_FTA = df['FTA'].sum()
    return lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)

def DRB_fn(df):
    lg_TRB = df['TOT'].sum()
    lg_ORB = df['OFF'].sum()
    return (lg_TRB - lg_ORB) / lg_TRB

def factor_fn(df):
    lg_AST = df['A'].sum()
    lg_FG = df['FG'].sum()
    lg_FT = df['FT'].sum()
    return (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))

def poss_fn(df,team):
    FGA = df[df['TEAM']==team]['FGA'].sum()
    FTA = df[df['TEAM']==team]['FTA'].sum()
    ORB = df[df['TEAM']==team]['OFF'].sum()
    TOV = df[df['TEAM']==team]['TO'].sum()
    opp = df[(df['MATCH'].str.contains(team)) & (df['TEAM']!=team)]
    op_FGA = opp['FGA'].sum()
    op_FTA = opp['FTA'].sum()
    op_ORB = opp['OFF'].sum()
    op_TOV = opp['TO'].sum()
    poss = 0.5 * (FGA + 0.475 * FTA - ORB + TOV) + 0.5 * (op_FGA + 0.475 * op_FTA - op_ORB + op_TOV)
    return poss

def uPER(df,player):
    team = df[df['PLAYER']==player]['TEAM'].values[0]
    VOP = VOP_fn(df)
    DRB = DRB_fn(df)
    factor = factor_fn(df)
    MP = df[df['PLAYER']==player]['MINS'].sum()
    _3P = df[df['PLAYER']==player]['3P'].sum()
    AST = df[df['PLAYER']==player]['A'].sum()
    FT = df[df['PLAYER']==player]['FT'].sum()
    FTA = df[df['PLAYER']==player]['FTA'].sum()
    TOV = df[df['PLAYER']==player]['TO'].sum()
    FGA = df[df['PLAYER']==player]['FGA'].sum()
    FG = df[df['PLAYER']==player]['FG'].sum()
    TRB = df[df['PLAYER']==player]['TOT'].sum()
    ORB = df[df['PLAYER']==player]['OFF'].sum()
    STL = df[df['PLAYER']==player]['STL'].sum()
    BLK = df[df['PLAYER']==player]['BLK'].sum()
    PF = df[df['PLAYER']==player]['PF'].sum()
    team_AST = df[df['TEAM']==team]['A'].sum()
    team_FG = df[df['TEAM']==team]['FG'].sum()
    lg_FT = df['FT'].sum()
    lg_PF = df['PF'].sum()
    lg_FTA = df['FTA'].sum()

    uPER = (1 / MP)*(_3P + (2/3) * AST + (2 - factor * (team_AST / team_FG)) * FG +
    (FT *0.5 * (1 + (1 - (team_AST / team_FG)) + (2/3) * (team_AST / team_FG))) -
    VOP * TOV - VOP * DRB * (FGA - FG) - VOP * 0.44 * (0.44 + (0.56 * DRB)) *
    (FTA - FT) + VOP * (1 - DRB) * (TRB - ORB) + VOP * DRB * ORB + VOP * STL +
    VOP * DRB * BLK - PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP) )

    return uPER

if __name__=='__main__':
