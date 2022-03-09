#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import requests

def LastSeasonDFCreator():
    Team = ['MCI','MUN','LIV','CHE','LEI','WHU','TOT','ARS','LEE','EVE','AVL','NEW','WOL','CRY','SOU','BHA','BUR','NOR','WAT','BRE']

    x16 = 20/16
    x17 = 20/17
    x18 = 20/18
    x19 = 20/19
    ### Current Season so far instead### 
    GF = [51,30*x18,50*x19,43,31*x18,34*x19,22*x17,32*x19,18*x18,21*x17,24*x18,19*x19,13*x18,27*x19,20*x19,17*x18,15*x16,8*x19,22*x17,21*x18]
    GA = [12,26*x18,16*x19,14,33*x18,25*x19,20*x17,23*x19,36*x18,29*x17,28*x18,42*x19,14*x18,27*x19,29*x19,18*x18,24*x16,42*x19,35*x17,25*x18]


    LastSeason = pd.DataFrame({'Team':Team,'GF':GF,'GA':GA})
    LastSeason['GF_std']=LastSeason['GF'].apply(lambda x: (x-np.mean(GF))/np.std(GF))
    LastSeason['GA_std']=LastSeason['GA'].apply(lambda x: (x-np.mean(GA))/np.std(GA))
    return LastSeason

def FixtureImport(teams):
    #Fixture Import
    url = 'https://fantasy.premierleague.com/api/fixtures/'
    r = requests.get(url)
    json = r.json()
    fixtures = pd.DataFrame(json)[['event','finished','team_h','team_h_score','team_a','team_a_score','stats']]

    fixtures.columns = ['Event','Fin','H','H_Score','A','A_Score','Stats']
    #fixtures = fixtures[np.isnan(fixtures['Event']).apply(lambda x: not x)]
    fixtures.loc[:,'H']=fixtures.loc[:,'H'].map(lambda x: teams.iloc[x-1]['short_name'])
    fixtures.loc[:,'A']=fixtures.loc[:,'A'].map(lambda x: teams.iloc[x-1]['short_name'])
    
    return fixtures

def FixtureImportxG(teams,GW):
    fixtures = FixtureImport(teams)
    #### CAN BE USED INSTEAD, USES xG ####
    test = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures#sched_11160_1'
    fixtures_xG = pd.read_html(test)[0][['Wk','Home','xG','Score','xG.1','Away']]
    fixtures_xG.columns = ['Event','H','H_Score','Res','A_Score','A']

    def finfunc(x, GW):
        if x['Event']>GW:# or np.isnan(x['H_Score']):
            return False
        else:
            return True

    team_to_short_map = {'Arsenal': 'ARS','Aston Villa':'AVL','Brighton':'BHA','Brentford':'BRE','Burnley':'BUR',
                        'Chelsea':'CHE','Crystal Palace':'CRY','Everton':'EVE','Leicester City':'LEI','Leeds United':'LEE',
                        'Liverpool':'LIV','Manchester City':'MCI','Manchester Utd':'MUN','Newcastle Utd':'NEW','Norwich City':'NOR',
                        'Southampton':'SOU','Tottenham':'TOT','Watford':'WAT','Wolves':'WOL','West Ham':'WHU',np.nan:'NaN'}    


    fixtures_xG['Fin']=fixtures_xG.apply(lambda x: finfunc(x, GW), axis=1)

    fixtures_xG.loc[:,'H']=fixtures_xG.loc[:,'H'].map(lambda x: team_to_short_map[x])
    fixtures_xG.loc[:,'A']=fixtures_xG.loc[:,'A'].map(lambda x: team_to_short_map[x])

    fixtures = fixtures_xG[fixtures_xG['Event']<GW].dropna('index').append(fixtures[fixtures['Event']>=GW]) # !!! overwriting 

    return fixtures
    
def getOffensiveSkillSep(team_name, fix_df,LastSeason_df,where='H'):
    factor = 0.7

    fixes_temp = fix_df[fix_df['Fin']==True]
    fixes = fixes_temp[fixes_temp[where]==team_name] #Only H or A
    all_fixes = fixes_temp[(fixes_temp['H']==team_name) | (fixes_temp['A']==team_name)] #Both H and A

    other_team = fixes['A'] if where=='H' else fixes['H']
    ls_against = LastSeason_df.set_index('Team').loc[other_team]['GA_std']
    #Do the same for all:
    other_team_all = np.where(all_fixes['H']!=team_name, all_fixes['H'],all_fixes['A'])
    ls_against_all = LastSeason_df.set_index('Team').loc[other_team_all]['GA_std']


    used_nr = 7
    weights = np.append(np.exp(factor*np.linspace(-40,-1,40)/15),[1])

    #Stuff after + adds last used_nr games regardless of H and A to really focus on recent form
    weighted_difficulty = 0.5*(np.average(ls_against.values[-used_nr:], weights=weights[-used_nr:])+np.average(ls_against_all.values[-used_nr:],weights=weights[-used_nr:]))
    #Also changed to all_fixes:
    used_nr2 = len(all_fixes)
    GoalsSoFar = np.where(all_fixes['H']==team_name, all_fixes['H_Score'],all_fixes['A_Score'])[-used_nr2:] @ weights[-used_nr2:]
    ScaledGoals = GoalsSoFar * (1/(weighted_difficulty-LastSeason_df['GA_std'].min())) #weighted_diff was first sumOfDiff
    return ScaledGoals

def getDefensiveSkillSep(team_name, fix_df,LastSeason_df, where='H'):
    factor = 0.7
    fixes_temp = fix_df[fix_df['Fin']==True]
    fixes = fixes_temp[fixes_temp[where]==team_name]
    all_fixes = fixes_temp[(fixes_temp['H']==team_name) | (fixes_temp['A']==team_name)] #Both H and A
    
    other_team = fixes['A'] if where=='H' else fixes['H']
    ls_for = LastSeason_df.set_index('Team').loc[other_team]['GF_std']
    #Do the same for all:
    other_team_all = np.where(all_fixes['H']!=team_name, all_fixes['H'],all_fixes['A'])
    ls_for_all = LastSeason_df.set_index('Team').loc[other_team_all]['GF_std']
    
    used_nr = 7
    weights = np.append(np.exp(factor*np.linspace(-40,-1,40)/15),[1])
    
    weighted_difficulty = 0.5*(np.average(ls_for.values[-used_nr:], weights=weights[-used_nr:])+np.average(ls_for_all.values[-used_nr:],weights=weights[-used_nr:]))
    
    used_nr2 = len(all_fixes)
    GoalsAgainstSoFar = np.where(all_fixes['H']!=team_name, all_fixes['H_Score'],all_fixes['A_Score'])[-used_nr2:] @ weights[-used_nr2:]
    ScaledGA = GoalsAgainstSoFar * (1/(weighted_difficulty-LastSeason_df['GF_std'].min()))
    return ScaledGA

def get_fixture(team, fixtures, event, dgw=0): #0  means no dgw, 1 means first game, 2 means 2nd
    
    if dgw!=0:
        possible = np.append(np.where(fixtures[(fixtures['Event']==event)]['H'].values == team),
                        np.where(fixtures[(fixtures['Event']==event)]['A'].values == team))
    if dgw!=2 or (dgw==2 and team not in fixtures[(fixtures['Event']==event)]['A'].values):  
        if team in fixtures[(fixtures['Event']==event)]['H'].values:
            if dgw==0:
                return fixtures[(fixtures['Event']==event)].set_index('H').loc[team]['A'] + ' (H)'
            else:
                opp=fixtures[(fixtures['Event']==event)].set_index('H').loc[team]['A']

                if type(opp)==pd.core.series.Series:
                    return opp[dgw-1] + ' (H)'
                else:
                    return opp + ' (H)'
    if team in fixtures[(fixtures['Event']==event)]['A'].values:
        if dgw==0:
            return fixtures[(fixtures['Event']==event)].set_index('A').loc[team]['H'] + ' (A)'
        else:
            opp = fixtures[(fixtures['Event']==event)].set_index('A').loc[team]['H']
            if type(opp)==pd.core.series.Series:
                return opp[dgw-1] + ' (A)'
            else:
                return opp + ' (A)'
                
    else:
        return 'NAN'
    
def FixTableCreator(teams, fixtures,DGWS=[21,22]):
    
    fixture_table_off_sep = teams.copy().sort_values('Offensive',ascending=False)[['name','short_name']]
    fixture_table_def_sep = teams.copy().sort_values('Defensive',ascending=True)[['name','short_name']]

    for i in range(int(fixtures[fixtures['Fin']==False]['Event'].min()),int(fixtures[fixtures['Fin']==False]['Event'].max())+1):
        if i in DGWS:
            fixture_table_off_sep['GW'+str(i)] = fixture_table_off_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i, dgw=1))
            fixture_table_def_sep['GW'+str(i)] = fixture_table_def_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i, dgw=1))
        else:
            fixture_table_off_sep['GW'+str(i)] = fixture_table_off_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i, dgw=0))
            fixture_table_def_sep['GW'+str(i)] = fixture_table_def_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i, dgw=0))

        if i in DGWS:
            fixture_table_off_sep['GW'+str(i)+'_2'] = fixture_table_off_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i, dgw=2))
            fixture_table_def_sep['GW'+str(i)+'_2'] = fixture_table_def_sep['short_name'].map(lambda x: get_fixture(x, fixtures, i,dgw=2))

            for j in range(len(fixture_table_off_sep['GW'+str(i)+'_2'])):
                if fixture_table_off_sep['GW'+str(i)+'_2'].iloc[j]==fixture_table_off_sep['GW'+str(i)].iloc[j]:
                    fixture_table_off_sep['GW'+str(i)+'_2'].iloc[j]='NAN'
                if fixture_table_def_sep['GW'+str(i)+'_2'].iloc[j]==fixture_table_def_sep['GW'+str(i)].iloc[j]:
                    fixture_table_def_sep['GW'+str(i)+'_2'].iloc[j]='NAN'
    return fixture_table_off_sep, fixture_table_def_sep
                    


def get_skill(teams,which, team_and_where):
    team = team_and_where[:3]
    where = team_and_where[-2:-1]
    #Switch because we are looking up the opponents skill, while H and A indicating if team we are looking up is home/away
    # Not whether opponent is home or away
    if where=='H':
        where='A'
    else:
        where ='H'
    if team=='NAN':
        return np.nan
    else:
        if which == 'Offensive':
            return teams.set_index('short_name')[where+'_Off'][team]
        else:
            return teams.set_index('short_name')[where+'_Def'][team]
        
def FixTableFDRCreator(teams,fixtures,fixture_table_off_sep, fixture_table_def_sep,DGWS):     
    fix_table_off_sep_fdr = fixture_table_off_sep.copy()
    fix_table_def_sep_fdr = fixture_table_def_sep.copy()
    for i in range(int(fixtures[fixtures['Fin']==False]['Event'].min()),int(fixtures[fixtures['Fin']==False]['Event'].max())+1):

        fix_table_off_sep_fdr['GW'+str(i)] = fixture_table_off_sep['GW'+str(i)].map(lambda x: get_skill(teams,'Defensive',x))
        fix_table_def_sep_fdr['GW'+str(i)] = fixture_table_def_sep['GW'+str(i)].map(lambda x: get_skill(teams,'Offensive',x))
        if i in DGWS:
            fix_table_off_sep_fdr['GW'+str(i)+'_2'] = fixture_table_off_sep['GW'+str(i)+'_2'].map(lambda x: get_skill(teams,'Defensive',x))
            fix_table_def_sep_fdr['GW'+str(i)+'_2'] = fixture_table_def_sep['GW'+str(i)+'_2'].map(lambda x: get_skill(teams,'Offensive',x))


    fix_table_off_sep_fdr=fix_table_off_sep_fdr.drop('name',axis=1).set_index('short_name')
    fix_table_def_sep_fdr=fix_table_def_sep_fdr.drop('name',axis=1).set_index('short_name')
    
    return fix_table_off_sep_fdr, fix_table_def_sep_fdr


def AllInOneFDR(teams, GW, DGWS):
    LS = LastSeasonDFCreator()
    fix_xG = FixtureImportxG(teams,GW)
    teams['H_Off']=round(teams['short_name'].map(lambda x: getOffensiveSkillSep(x,fix_xG,LS, where='H')),2)
    teams['H_Def']=round(teams['short_name'].map(lambda x: getDefensiveSkillSep(x,fix_xG,LS, where='H')),2)
    teams['A_Off']=round(teams['short_name'].map(lambda x: getOffensiveSkillSep(x,fix_xG,LS, where='A')),2)
    teams['A_Def']=round(teams['short_name'].map(lambda x: getDefensiveSkillSep(x,fix_xG,LS, where='A')),2)
    teams['Offensive'] = teams['H_Off']+teams['A_Off']
    teams['Defensive'] = teams['H_Def']+teams['A_Def']
    fix_off, fix_def = FixTableCreator(teams,fix_xG,DGWS)
    fix_off_fdr, fix_def_fdr = FixTableFDRCreator(teams,fix_xG,fix_off,fix_def,DGWS)
    
    return fix_off,fix_def, fix_off_fdr, fix_def_fdr, teams

