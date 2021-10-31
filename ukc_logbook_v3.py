'''imports all csv files in the source directory and concatenates them, saving
   output (if need be) in the sink directory and plotting figures as submitted.

   This version works nicely for Trad climbs
''' 

import pandas as pd
import numpy as np
import glob
import os
import plotly.express as px

from datetime import datetime

'''settings and assignments'''
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
cwd = os.getcwd()               # current working directory
sink = cwd + '/Output/'
source = cwd
f = 'ukc_logbook.csv'

def preps(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df = df.drop(['Climb name', 'Date', 'Crag name', 'Partner(s)', 'Notes'],
                     axis=1)

    '''just keep the text before the space in Grade'''
    df['Grade'] = df['Grade'].apply(lambda x: x[0:x.find(' ')])
    # 1. I'd like to create a 2nd chart using the tech grade for Trad next
    '''only want clean lead climbs'''
    df1 = df[df['Style'].isin(['Lead O/S','Lead rpt','Lead β','Lead',
                              'AltLd O/S','AltLd rpt','AltLd β','AltLd',
                              'Sent O/S','Sent rpt','Sent β','Sent','Sent x'])]

    '''show which Lead styles have been dropped'''
    df2  = df[~df['Style'].isin(['Lead O/S','Lead rpt','Lead β','Lead',
                              'AltLd O/S','AltLd rpt','AltLd β','AltLd',
                              'Sent O/S','Sent rpt','Sent β','Sent','Sent x'])]
    styles = sorted(set(df2['Style']))
    print('Check I was right to drop these, as not clean leads: \n')
    print(styles)

    '''categorise climbs'''
    df1 = df1.assign(Climb_type = df1['Grade'])
    df1['Grade filter'] = df1['Grade'].str[0]
    df1.loc[df1['Grade filter'] == 'f', 'Climb_type'] = 'Boulder'
    df1.loc[df1['Grade filter'].str.contains(
        '1|2|3|4|5|6|7|8|9'), 'Climb_type'] = 'Sport'
    df1.loc[df1['Grade filter'].str.contains(
        'M|D|S|H|V|E'), 'Climb_type'] = 'Trad'

    '''check there's nothing left behind'''
    df3 = df1[~df1['Climb_type'].isin(['Trad','Sport','Boulder'])]
    print('Investigate if any data is returned in the following df:')
    print(df3)

    '''don't need Style or Grade Filter anymore'''
    df1 = df1.drop(['Style', 'Grade filter'], axis=1)
    return df1

def counts_climbs(df, years):
    '''count number of leads for each grade for each year and then combine
       them back into a single dataframe which is returned'''
    df4 = pd.DataFrame()
    for y in years:
        '''filter df for one year'''
        dfy = df.loc[df['Year'] == y]
        count = dfy['Grade'].value_counts()             # (count is a series)
        count.rename('Count', inplace=True)
        count_n = dfy['Grade'].value_counts(normalize=True)# count_n (n'lised)
        count_n.rename('Count', inplace=True)
        df2 = pd.DataFrame(count)                       # make a new dataframe
        df2 = df2.assign(Year = y, Chart = 'Count')     # add year back in
        df3 = pd.DataFrame(count_n)
        df3 = df3.assign(Year = y, Chart = 'Percent')
        df3['Count'] = df3['Count'] * 100
        df4 = pd.concat([df4, df3, df2])                # concat into one df

    '''make sure all grades appear in the first year, so that chart
       displays correctly.  I do this by creating a dataframe with zero
       values for the first year in the data.'''
    min_year = min(years)
    grades = set(df4.index)
    no_grades = len(grades)
    counts = [0] * (2*no_grades)                    # data for Count column
    yrs = [min_year] * (2*no_grades)                # data for Year column
    chrt1 = ['Count'] * (no_grades)                 
    chrt2 = ['Percent'] * (no_grades)               
    chrt = chrt1 + chrt2                            # data for Chart column
    idx = list(set(df4.index))
    idx2 = idx + idx                                # data for index
    df_new = pd.DataFrame({'Count': counts,
                           'Year': yrs,
                           'Chart': chrt},
                          index = idx2)
    df4 = df4.append(df_new)
    return df4

def orders_trad(df):
    '''order Trad grades on difficulty'''
    df['Order'] = 0
    df.loc['D', 'Order'] = 1
    df.loc['VD', 'Order'] = 2
    df.loc['HVD', 'Order'] = 3
    df.loc['S', 'Order'] = 4
    df.loc['HS', 'Order'] = 5
    df.loc['VS', 'Order'] = 6
    df.loc['HVS', 'Order'] = 7
    df.loc['E1', 'Order'] = 8
    df.loc['E2', 'Order'] = 9
    df.loc['E3', 'Order'] = 10
    df.loc['E4', 'Order'] = 11
    df.loc['E5', 'Order'] = 12
    df.loc['E6', 'Order'] = 13
    df.loc['E7', 'Order'] = 14
    df.loc['E8', 'Order'] = 15
    df.loc['E9', 'Order'] = 16
    df = df.dropna()          # drops grades that don't appear in logbook

    '''plot uses data as it is in dataframe, so sorting it now'''
    df = df.sort_values(by=['Year','Chart','Order'])
    return df

def orders_sport(df):
    '''order Sport grades on difficulty'''
    df['Order'] = 0
    df.loc['1', 'Order'] = 1
    df.loc['2a', 'Order'] = 2
    df.loc['2b', 'Order'] = 3
    df.loc['2c', 'Order'] = 4
    df.loc['3a', 'Order'] = 5
    df.loc['3b', 'Order'] = 6
    df.loc['3c', 'Order'] = 7
    df.loc['4a', 'Order'] = 8
    df.loc['4b', 'Order'] = 9
    df.loc['4c', 'Order'] = 10
    df.loc['5a', 'Order'] = 11
    df.loc['5b', 'Order'] = 12
    df.loc['5c', 'Order'] = 13
    df.loc['6a', 'Order'] = 14
    df.loc['6a+', 'Order'] = 15
    df.loc['6b', 'Order'] = 16
    df.loc['6b+', 'Order'] = 17
    df.loc['6c', 'Order'] = 18
    df.loc['6c+', 'Order'] = 19
    df.loc['7a', 'Order'] = 20
    df.loc['7a+', 'Order'] = 21
    df.loc['7b', 'Order'] = 22
    df.loc['7b+', 'Order'] = 23
    df.loc['7c', 'Order'] = 24
    df.loc['7c+', 'Order'] = 25
    df = df.dropna()          # drops grades that don't appear in logbook

    '''plot uses data as it is in dataframe, so sorting it now'''
    df = df.sort_values(by=['Year','Chart','Order'])
    return df

def orders_boulder(df):
    '''order Boulder grades on difficulty'''
    df['Order'] = 0
    df.loc['f1', 'Order'] = 1
    df.loc['f1+', 'Order'] = 2
    df.loc['f2', 'Order'] = 3
    df.loc['f2+', 'Order'] = 4
    df.loc['f3', 'Order'] = 5
    df.loc['f3+', 'Order'] = 6
    df.loc['f4', 'Order'] = 7
    df.loc['f4+', 'Order'] = 8
    df.loc['f5', 'Order'] = 9
    df.loc['f5+', 'Order'] = 10
    df.loc['f6A', 'Order'] = 11
    df.loc['f6A+', 'Order'] = 12
    df.loc['f6B', 'Order'] = 13
    df.loc['f6B+', 'Order'] = 14
    df.loc['f6C', 'Order'] = 15
    df.loc['f6C+', 'Order'] = 16
    df.loc['f7A', 'Order'] = 17
    df.loc['f7A+', 'Order'] = 18
    df.loc['f7B', 'Order'] = 19
    df.loc['f7B+', 'Order'] = 20
    df.loc['f7C', 'Order'] = 21
    df.loc['f7C+', 'Order'] = 22
    df = df.dropna()          # drops grades that don't appear in logbook

    '''plot uses data as it is in dataframe, so sorting it now'''
    df = df.sort_values(by=['Year','Chart','Order'])
    return df

def plot_data(df, g_title, years):    
    '''need max and min year for the chart'''
    mx = max(years) + 0.5
    mn = min(years) - 0.5
    fig = px.bar(df,
                 x='Year',
                 y='Count',
                 color=df.index,
                 color_discrete_sequence= px.colors.sequential.Plasma_r,
                 # use color_continuous_scale if plotting numbers not strings
                 facet_col='Chart',
                 facet_col_spacing=0.1,
                 hover_data=[df.index],
                 title=f'<b>{g_title}</b>')
    fig.update_layout(
        title={
            'x':0.5,
            'xanchor': 'center'})
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    #the lambda function takes the text to the RHS of the =
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.update_xaxes(tick0=1, dtick=1, range=(mn, mx), showticklabels=True)
    fig.show()


'''read in file and prep data'''
df = pd.read_csv(f)
df1 = preps(df)

'''create trad dataframe'''
df_trad = df1.loc[df1['Climb_type'] == 'Trad']
t_years = set(df_trad['Year'])     # extracts years for the for loop
df_trad = counts_climbs(df_trad, t_years)
df_trad = orders_trad(df_trad)

'''create sport dataframe'''
df_sport = df1.loc[df1['Climb_type'] == 'Sport']
s_years = set(df_sport['Year'])     # extracts years for the for loop
df_sport = counts_climbs(df_sport, s_years)
df_sport = orders_sport(df_sport)

'''create boulder dataframe'''
df_boulder = df1.loc[df1['Climb_type'] == 'Boulder']
b_years = set(df_boulder['Year'])     # extracts years for the for loop
df_boulder = counts_climbs(df_boulder, b_years)
df_boulder = orders_boulder(df_boulder)

'''plot charts'''
plot_data(df_trad, 'Trad Climbs Led', t_years)
plot_data(df_sport, 'Sport Climbs Led', s_years)
plot_data(df_boulder, 'Boulders Sent', b_years)


