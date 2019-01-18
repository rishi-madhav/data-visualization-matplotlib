# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load the dataset and create column `year` which stores the year in which match was played
data_ipl = pd.read_csv(path)
data_ipl['year'] = data_ipl['date'].apply(lambda x: x[:4])

# Plot the wins gained by teams across all seasons
match_data = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)
total_wins = match_data['winner'].value_counts()
plot_wins_total = total_wins.plot(kind='bar', title='No of wins across seasons 2008-2016', figsize=(7,5))
plt.xlabel('Team Name')
plt.ylabel('Number of wins')

# Top bowlers taking wickets with bowled
wickets = data_ipl[data_ipl['wicket_kind'] == 'bowled']
bowler_wickets = wickets.groupby(['bowler'])['wicket_kind'].count()
bowler_wickets.sort_values(ascending=False, inplace=True)
bowler_wickets[:10].plot(kind='bar', title='Top bowlers taking wickets with bowled', figsize=(7,5))
plt.xlabel('Bowler Name')
plt.ylabel('No.of wickets')

# How did the different pitches behave? What was the average score for each stadium?
score_per_venue = data_ipl.loc[:,['match_code','venue','inning','total']]
avg_score_per_venue = score_per_venue.groupby(['venue','match_code','inning']).agg({'total':sum}).reset_index()
avg_score_per_venue = avg_score_per_venue.groupby(['venue','inning'])['total'].mean().reset_index()
avg_score_per_venue = avg_score_per_venue[(avg_score_per_venue['inning'] == 1) | (avg_score_per_venue['inning'] == 2)]

plt.figure(figsize=(19,8))
plt.plot(avg_score_per_venue[avg_score_per_venue['inning'] == 1]['venue'],avg_score_per_venue[avg_score_per_venue['inning'] == 1]['total'],'-b',marker='o', label='inning1')
plt.plot(avg_score_per_venue[avg_score_per_venue['inning'] == 2]['venue'],avg_score_per_venue[avg_score_per_venue['inning'] == 2]['total'],'-r',marker='o', label='inning2')
plt.legend(loc='upper right', fontsize=16)
plt.xticks(rotation=90, fontsize=14)
plt.xlabel('Venue', fontsize=18)
plt.ylabel('Average score per venue', fontsize=16)
plt.show()


# Types of Dismissal and how often they occur
dismissed = data_ipl.groupby(['wicket_kind']).count().reset_index()
dismissed = dismissed[['wicket_kind','delivery']]

f, (ax1,ax2) = plt.subplots(1, 2, figsize=(15,7))
f.suptitle("Top Dismissal Visualizations", fontsize=12)

dismissed.plot.bar(ax=ax1, legend=False)
ax1.set_xticklabels(list(dismissed['wicket_kind']), fontsize=8)

explode = [0.01, 0.02, 0.1, 0.2, 0.25, 0.4, 0.35, 0.05, 0.05] 
properties = ax2.pie(dismissed['delivery'], labels=None, startangle=150, autopct='%1.1f%%', explode=explode)
ax2.legend(bbox_to_anchor=(1,1), labels=dismissed['wicket_kind'])

# Plot no. of boundaries across IPL seasons
boundaries_ipl = data_ipl.loc[:,['runs','year']]
boundaries_fours = boundaries_ipl[boundaries_ipl['runs'] == 4]
fours = boundaries_fours.groupby('year')['runs'].count()
boundaries_sixes = boundaries_ipl[boundaries_ipl['runs'] == 6]
sixes = boundaries_sixes.groupby('year')['runs'].count()

plt.figure(figsize=(12,8))
plt.plot(fours.index, fours, '-b', marker='o', ms=6, lw=2, label='Fours')
plt.plot(sixes.index, sixes, '-r', marker='o', ms=6, lw=2, label='Sixes')
plt.legend(loc='upper right', fontsize=19)
plt.xticks(rotation=90)
plt.xlabel('IPL Seasons')
plt.ylabel('Total 4s and 6s scored across seasons', fontsize=16)
plt.show()

#Get the average statistics across seasons (such as average runs scored per match, average balls bowled per match by season and average runs scored against each ball bowled per season)

per_match_data = data_ipl.drop_duplicates(subset='match_code', keep='first').reset_index(drop=True)

total_runs_per_season = data_ipl.groupby('year')['total'].sum()
balls_delivered_per_season = data_ipl.groupby('year')['delivery'].count()
no_of_matches_played_per_season = per_match_data.groupby('year')['match_code'].count()

average_balls_per_match = balls_delivered_per_season / no_of_matches_played_per_season
average_runs_per_match = total_runs_per_season / no_of_matches_played_per_season
average_runs_per_ball = total_runs_per_season / balls_delivered_per_season

avg_data = pd.DataFrame([no_of_matches_played_per_season, average_runs_per_match, average_balls_per_match, average_runs_per_ball])
avg_data.index = ['No of Matches', 'Average Runs per Match', 'Average balls bowled', 'Average runs per ball']

avg_data.T.plot(kind='bar', figsize=(12,10), colormap='coolwarm')
plt.xlabel('Season')
plt.ylabel('Average')
plt.legend(loc=9, ncol=4)


