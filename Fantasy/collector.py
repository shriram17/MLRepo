import urllib
import json
import pandas as pd
import numpy as np

htmltext = urllib.urlopen("http://jokecamp.github.io/epl-fantasy-geek/js/data.json")
data = json.load(htmltext)
no_of_players = len(data["elInfo"])
# print  no_of_players
#print data["elInfo"][1]
playerdata=[]
for i in range(1,no_of_players):
    playerdata.append(data["elInfo"][i])
#for i in range(no_of_players-1):
#  print playerdata[i],"\n"
no_of_stats = len(data["elStat"])


#for key in data["elStat"].items():
#    print key
stats = []
stats = sorted(data["elStat"].items(), key=lambda x: x[1])
#stats.append()
print stats
#print playerdata[50]
sczeny = {}
for key,value in stats:
    for row in range(0, no_of_players-1):
        sczeny[key] = playerdata[row][value]
#print sczeny
#print sczeny[]
#Elemet Type ID 1 GK, 2 DEF, 3 MID , 4 STR
#Status 'a' available, 'd' - Doubtful , 'u' - Unavailable, 'i' - Injured, 's' - Suspended

#(u'id', 0), (u'status', 1), (u'code', 2), (u'first_name', 3), (u'second_name', 4), (u'web_name', 5),(u'value_form', 16),
# (u'value_season', 17), (u'in_dreamteam', 22), (u'dreamteam_count', 23)
# (u'minutes', 42), (u'goals_scored', 43), (u'assists', 44), (u'clean_sheets', 45), (u'goals_conceded', 46),
# (u'own_goals', 47), (u'penalties_saved', 48), (u'penalties_missed', 49),
#(u'yellow_cards', 50), (u'red_cards', 51), (u'saves', 52), (u'bonus', 53), (u'ea_index', 54),
# position - 56, team_code -  57

# Columns we need - 0, 1, 2, 3, 4, 5, 16, 17, 22, 23, 36, 38, 42, 43, 44, 45, 46, 47, 48, 49, 50,51, 52, 53, 54, 56, 57
#0 , 1


req_col = [0, 1, 2, 3, 4, 5, 16, 17, 22, 23, 36, 38, 42, 43, 44, 45, 46, 47, 48, 49, 50,51, 52, 53, 54, 56, 57]
playerdata2 = []
#print len(playerdata)

for row in range(0, len(playerdata)):
    #eliminate unavailable players
    if playerdata[row][1] != 'u':
        #Min 100mins played and 15 points
        if playerdata[row][42] > 150 and playerdata[row][36]>20:
            for col in req_col:
               playerdata2.append(playerdata[row][col])

chunks = [playerdata2[x:x+len(req_col)] for x in xrange(0, len(playerdata2), len(req_col))]
# print chunks
if chunks[0][1] == 'u': print 'true'

print "No of players available : ", len(chunks)
keepers = []
defenders = []
midfielders = []
strikers = []

# print chunks[0][25]

for row in range(0, len(chunks)-1):
    #Can use switch
    if chunks[row][25] == 1:
        keepers.append(chunks[row])
    elif chunks[row][25] == 2:
        defenders.append(chunks[row])
    elif chunks[row][25] == 3:
        midfielders.append(chunks[row])
    else:
        strikers.append(chunks[row])

# print len(keepers), len(defenders), len(midfielders), len(strikers)

#Accessing Team names, where '1' is the last collumn
#print data["eiwteams"]['1']['name']
#print len(data["eiwteams"])

#print playerdata2
epl_table = pd.read_csv('EPLtable_detailed.csv')
#print epl_table.head(6)
#print epl_table['GA'].idxmin()
#print epl_table[:5][['Team_code','Rank','GF','GA','GD','Pts']]

#print midfielders[0][13]
topfour =[] #[7,1,14,9]

#

#Create a dataframe of top4
top4 = epl_table[epl_table['Rank'] <=4]
topfour = top4['Team_code'].tolist()

top6 = epl_table[epl_table['Rank'] <=6]
topsix = top6['Team_code'].tolist()

#Create a dataframe of tophalf
top10 = epl_table[epl_table['Rank'] <= 10]
tophalf= top10['Team_code'].tolist()

# Sample recommendation for Southampton, to finish in top 4

team_selected = input("Enter Team Code :")
team_stats = epl_table[epl_table['Team_code'] == team_selected]
print "\n Team Stats \n", team_stats

#Select your objective for next season - Winners (1), Champions League(2), Europa(3), Top Half(4)
print "\n SELECT YOUR OBJECTIVES FOR THE SEASON 16/17 \n 1 - Champions \n 2 - Champions League Spot \n 3 - Europa Spot \n 4 - Top Half "
objective = input(" \n Your Choice  :  ")

sol=[]
for mids in range(len(midfielders)):
   if(midfielders[mids][13] + midfielders[mids][14])> 12 and midfielders[mids][26]!= 13 and midfielders[mids][9]>3 and midfielders[mids][26] not in topfour:
       sol.append(midfielders[mids])

print '\n Top 5 suggestions \n'
for mids in range(5):
    print sol[mids],"\n"
#print len(sol)

