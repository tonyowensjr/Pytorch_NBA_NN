from constants import *

import argparse
import numpy as np
import pandas as pd
import requests
import time

pd.options.mode.chained_assignment = None

def scraper(start_year:int,end_year:int) -> list:
    """
    Retreive and prepare the data for the model
    args:
    start_year (int): the first year to get data from the model
    end_year (int): the final year to get data from the model
    """
    years = [x for x in np.arange(start_year,end_year) if x != 2020]
    all_years = []
    # iterate through each of the specified years
    for year in years:
        all_months = []
        # determine the basketball reference url for the given year and get the team records
        stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html"
        data_stats = requests.get(stats_url)
        stats = pd.read_html(data_stats.content)[0]
        stats.columns = stats.columns.droplevel(level=0)
        # define the months to iterate through
        months = ['october', 'november', 'december', 'january', 'february', 'march']

        # determine the url from realgm and get their stats
        ms_url = f"https://basketball.realgm.com/nba/team-stats/{year}/Averages/Team_Totals/Regular_Season"
        ms_data = requests.get(ms_url)
        ms_stats = pd.read_html(ms_data.content)[-1]
        # map the basketball reference team names to the realgm team names
        stats.Team = stats.Team.map(TEAM_TO_LOCATION)
        # merge the stats to create the stats dataframe for the year
        stats = ms_stats.merge(stats,left_on = ["Team"],right_on = ["Team"], how = "outer")
        print(year)
        # iterate through each month of the year skipping if there were no games in the month
        for month in months:
            try:
                time.sleep(5)
                # determine the url for the basketball reference schedules
                url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
                data = requests.get(url)
                sched = pd.read_html(data.content)[0]
                sched = sched.rename(columns = {"Visitor/Neutral" : "Away", "Home/Neutral" : "Home", "PTS" : "Away Pts", "PTS.1" : "Home Pts"})
                attempt = []
                # merge the stats and the schedules for each game
                for j in sched.index:
                    test = sched.loc[sched.index == j]
                    test.Home = test.Home.map(TEAM_TO_LOCATION)
                    test.Away = test.Away.map(TEAM_TO_LOCATION)
                    attempt.append(pd.merge(pd.merge(test,stats[stats['Team'].isin(test['Home'])].add_prefix('Home '),left_on='Home',right_on = 'Home Team'),stats[stats['Team'].isin(test['Away'])].add_prefix('Away '),left_on = 'Away', right_on = 'Away Team'))
                # add this month's dataframe to the rest of the months for that year
                all_months.append(pd.concat(attempt))
            except Exception:
                pass       
             # create a new dataframe for all of that year   
        full_sched = pd.concat(all_months).sort_values(by ='Date').reset_index(drop = True)
        all_years.append(full_sched)
    return all_years

def remove_day(row:str)->str:
    """
    Remove the day of the week in the date column.
    args: row (str): The original date
    returns (str): The date with the day of the week removed
    """
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