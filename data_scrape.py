import argparse
import time
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import re
import datetime
import requests
from constants import *

def scraper(start_year:int,end_year:int):
    years = [x for x in np.arange(start_year,end_year) if x != 2020]
    all_years = []
    for year in years:
        all_months = []
        stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html"
        data_stats = requests.get(stats_url)
        stats = pd.read_html(data_stats.content)[0]
        stats.columns = stats.columns.droplevel(level=0)
        months = ['october', 'november', 'december', 'january', 'february', 'march']
        month_abrv = ['december', 'january', 'february', 'march']
        month_nov = ['november','december', 'january', 'february', 'march']
        ms_url = f"https://basketball.realgm.com/nba/team-stats/{year}/Averages/Team_Totals/Regular_Season"
        ms_data = requests.get(ms_url)
        ms_stats = pd.read_html(ms_data.content)[-1]
        stats.Team = stats.Team.map(TEAM_TO_LOCATION)
        stats = ms_stats.merge(stats,left_on = ["Team"],right_on = ["Team"], how = "outer")
        # process for years w/ normal full year schedule 
        print(year)
        if (year != 2021) & (year != 2012) & (year != 2005) & (year != 2000) & (year != 2006):
            for month in months:
                time.sleep(5)
                url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
                data = requests.get(url)
    #             print(year,month)
                sched = pd.read_html(data.content)[0]
                sched = sched.rename(columns = {"Visitor/Neutral" : "Away", "Home/Neutral" : "Home", "PTS" : "Away Pts", "PTS.1" : "Home Pts"})
                attempt = []
                for j in sched.index:
                    test = sched.loc[sched.index == j]
                    test.Home = test.Home.map(TEAM_TO_LOCATION)
                    test.Away = test.Away.map(TEAM_TO_LOCATION)
                    attempt.append(pd.merge(pd.merge(test,stats[stats['Team'].isin(test['Home'])].add_prefix('Home '),left_on='Home',right_on = 'Home Team'),stats[stats['Team'].isin(test['Away'])].add_prefix('Away '),left_on = 'Away', right_on = 'Away Team'))
                all_months.append(pd.concat(attempt))
                full_sched = pd.concat(all_months).sort_values(by ='Date').reset_index(drop = True)
                all_years.append(full_sched)
        # same thing but omitting the missing months for the 2012 & 2021 season
        elif ((year == 2012) | (year == 2021)):
            for month in month_abrv:
                time.sleep(5)
                url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
                data = requests.get(url)
                sched = pd.read_html(data.content)[0]
                sched = sched.rename(columns = {"Visitor/Neutral" : "Away", "Home/Neutral" : "Home", "PTS" : "Away Pts", "PTS.1" : "Home Pts"})
                attempt = []
                for j in sched.index:
                    test = sched.loc[sched.index == j]
                    test.Home = test.Home.map(TEAM_TO_LOCATION)
                    test.Away = test.Away.map(TEAM_TO_LOCATION)
                    attempt.append(pd.merge(pd.merge(test,stats[stats['Team'].isin(test['Home'])].add_prefix('Home '),left_on='Home',right_on = 'Home Team'),stats[stats['Team'].isin(test['Away'])].add_prefix('Away '),left_on = 'Away', right_on = 'Away Team'))
                all_months.append(pd.concat(attempt))
                full_sched = pd.concat(all_months).sort_values(by ='Date').reset_index(drop = True)
                all_years.append(full_sched)
            # accounting for years in which the season began in NOV not OCT
        else:
            for month in month_nov:
                time.sleep(5)
                url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
                data = requests.get(url)
                sched = pd.read_html(data.content)[0]
                sched = sched.rename(columns = {"Visitor/Neutral" : "Away", "Home/Neutral" : "Home", "PTS" : "Away Pts", "PTS.1" : "Home Pts"})
                attempt = []
                for j in sched.index:
                    test = sched.loc[sched.index == j]
                    test.Home = test.Home.map(TEAM_TO_LOCATION)
                    test.Away = test.Away.map(TEAM_TO_LOCATION)
                    attempt.append(pd.merge(pd.merge(test,stats[stats['Team'].isin(test['Home'])].add_prefix('Home '),left_on='Home',right_on = 'Home Team'),stats[stats['Team'].isin(test['Away'])].add_prefix('Away '),left_on = 'Away', right_on = 'Away Team'))
                all_months.append(pd.concat(attempt))
                full_sched = pd.concat(all_months).sort_values(by ='Date').reset_index(drop = True)
                all_years.append(full_sched)
    return all_years

def remove_day(row):
    for string in ['Fri, ', 'Mon, ', 'Sat, ', 'Sun, ', 'Thu, ', 'Tue, ', 'Wed, ']:
        row = row.replace(string,'')
    return row
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_year', type=int, help="The first year in the data scraping interval", required=True)
    parser.add_argument('--end_year', type=int, help="The second year in the data scraping interval", required=True)
    args = parser.parse_args()
    start_year = args.start_year  
    end_year = args.end_year
    df = pd.concat(scraper(start_year,end_year))
    df.reset_index(drop = True,inplace = True)
    df['Target'] = df.apply(lambda x: 1 if x['Home Pts'] > x['Away Pts'] else 0, axis = 1)
    df['Date'] = pd.to_datetime(df.Date.apply(lambda x:remove_day(x)))
    df.insert(1,"Year",df.Date.dt.year)
    df.to_csv(f'nba_data_{start_year}-{end_year}.csv')
if __name__ == '__main__':
    main()