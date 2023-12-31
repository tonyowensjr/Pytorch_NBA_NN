LOCATION_TO_TEAM = {"New Jersey": "New Jersey Nets","Houston" : "Houston Rockets","Utah" : "Utah Jazz",
"L.A. Clippers": "Los Angeles Clippers","L.A. Lakers": "Los Angeles Lakers",
"Phoenix": "Phoenix Suns", "Milwaukee" : "Milwaukee Bucks", "Philadelphia": "Philadelphia 76ers",
 "Denver" : "Denver Nuggets","Brooklyn": "Brooklyn Nets", "Dallas" : "Dallas Mavericks", 
 "New York" : "New York Knicks", "Atlanta" : "Atlanta Hawks", "Portland": "Portland Trail Blazers",
   "Boston": "Boston Celtics", "Golden State" : "Golden State Warriors", "Memphis" : "Memphis Grizzlies",
     "Miami": "Miami Heat", "Indiana" : "Indiana Pacers", "New Orleans" : "New Orleans Pelicans", 
     "Toronto" : "Toronto Raptors", "Chicago": "Chicago Bulls", "San Antonio" : "San Antonio Spurs", 
     "Washington" : "Washington Wizards", "Sacramento" : "Sacramento Kings", "Detroit" : "Detroit Pistons", "Minnesota" : "Minnesota Timberwolves", 
     "Charlotte": "Charlotte Bobcats", "Cleveland": "Cleveland Cavaliers", "Orlando": "Orlando Magic",
       "Oklahoma City" : "Oklahoma City Thunder"}
TEAM_TO_LOCATION = {v: k for k, v in LOCATION_TO_TEAM.items()} | {'New Orleans Hornets': 'New Orleans','Charlotte Hornets':'Charlotte',
'Seattle SuperSonics': 'Seattle','Vancouver Grizzlies':'Vancouver',
"New Orleans/Oklahoma City Hornets":"New Orleans" }

DF_COLS = ['Date', 'Away', 'Away Pts', 'Home', 'Home Pts',
       'Home Team', 'Home PPG', 'Home FGM', 'Home FGA',
       'Home FG%', 'Home 3PM', 'Home 3PA', 'Home 3P%', 'Home FTM', 'Home FTA',
       'Home FT%', 'Home ORB', 'Home DRB','Home APG', 'Home SPG',
       'Home BPG', 'Home TOV', 'Home PF', 'Home W', 'Home L', 'Home W/L%','Home MOV/A', 
                 'Home ORtg/A', 'Home DRtg/A','Away Team', 
        'Away PPG', 'Away FGM',
       'Away FGA', 'Away FG%', 'Away 3PM', 'Away 3PA', 'Away 3P%', 'Away FTM',
       'Away FTA', 'Away FT%', 'Away ORB', 'Away DRB',  'Away APG',
       'Away SPG', 'Away BPG', 'Away TOV', 'Away PF','Away W', 'Away L', 
                 'Away W/L%','Away MOV/A', 'Away ORtg/A', 'Away DRtg/A']
