import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
teamAbbr = []
teamName = []

def getTeamNames():
    URL = "https://www.bundesliga.com/en/bundesliga/table"
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "html.parser")
    #Abbr -> d-sm-none FUllName -> d-lg-inline
    #Getting team Abbrevations
    global teamAbbr
    global teamName
    teamAbbr = [s  for span in soup.select('.team .d-sm-none') for s in span.stripped_strings]
    #Getting Teams Full name
    teamName = [s  for span in soup.select('.team .d-lg-inline') for s in span.stripped_strings]

def getmtchurl(matchday):
    if matchday=="supercup":
        return "https://www.bundesliga.com/en/bundesliga/matchday/2021-2022/supercup"
    else:
        return "https://www.bundesliga.com/en/bundesliga/matchday/2021-2022/"+str(matchday)

def matchDay(match_day):
    # 1 SuperCup & 31 matchdays -> 32 
    # urlmatch= getmtchurl("supercup")
    urlmatch= getmtchurl(match_day)
    if(match_day=="supercup"):
        print("\nMatch: SuperCup\n")
    else:
        print("\nMatch Day: #"+str(match_day))
    print("\n")
    print(urlmatch)
    print("\n")
    matchpage=requests.get(urlmatch).text
    soup = BeautifulSoup(matchpage, "html.parser")
    #Score Bug is the element
    scorebugElement = 'score-bug'
    # home(div) -> left; tlc(div) -> ABBR; score(div) -> Goals Scored 
    homeGoal = [s  for scorebugElement in soup.select('.home .score') for s in scorebugElement.stripped_strings]
    homeTeam = [s  for scorebugElement in soup.select('.home .tlc') for s in scorebugElement.stripped_strings]
    # away(div) -> right; tlc(div) -> ABBR; score(div) -> Goals Scored 
    awayGoal = [s  for scorebugElement in soup.select('.away .score') for s in scorebugElement.stripped_strings]
    awayTeam = [s  for scorebugElement in soup.select('.away .tlc') for s in scorebugElement.stripped_strings]
    
    # Intial Data
    # print("intial Match table points \n")
    # print(df)
    # Rows -> Home => teamAbbr.index(${teamName})
    # Columns -> Away => sub_df[${teamNamw}]
    # 1. Iterate Home Team as well as away team
    # 2. determine by homegoal and awaygoal, the winner
    # 3. Update the dataframe, the winner by one value
    for i in range(len(homeTeam)):
        if(int(homeGoal[i]) == int(awayGoal[i])):
            #there is a tie
            goalscored[homeTeam[i]]+=int(homeGoal[i])
            goalscored[awayTeam[i]]+=int(awayGoal[i])
            continue
        elif(int(homeGoal[i]) > int(awayGoal[i])):
            # Hometeam is winner
            print(str(homeTeam[i])+" at home beat    "+str(awayTeam[i])+" by "+str(int(homeGoal[i])-int(awayGoal[i]))+" goals!!")
            sub_df = df.iloc[int(teamAbbr.index(homeTeam[i]))]
            sub_df.iloc[int(teamAbbr.index(awayTeam[i]))]=1
            goalscored[homeTeam[i]]+=int(homeGoal[i])
            goalscored[awayTeam[i]]+=int(awayGoal[i])
        else:
            #awayteam is winner
            print(str(homeTeam[i])+" at home lost to "+str(awayTeam[i])+" by "+str(int(awayGoal[i])-int(homeGoal[i]))+" goals!!")
            sub_df = df.iloc[int(teamAbbr.index(homeTeam[i]))]
            sub_df.iloc[int(teamAbbr.index(awayTeam[i]))]=1
            goalscored[homeTeam[i]]+=int(homeGoal[i])
            goalscored[awayTeam[i]]+=int(awayGoal[i])
    # print(df)

getTeamNames()
#if the value is 1 team won match on their home
# for i,i => Value is -1 as one team cannot play itself
nm="-1"
goalscored={}
for i in range(len(teamAbbr)):
    goalscored[teamAbbr[i]]=0
initial=len(teamAbbr)*[0]
df=pd.DataFrame({teamAbbr[0]:initial})
for i in range(1,len(teamAbbr)):
    df[teamAbbr[i]] = initial
for j in range(0,len(teamAbbr)):
    df.rename(index={j:teamAbbr[j]}, inplace=True)
np.fill_diagonal(df.values,nm)
print("intial Match table \n")
print(df)
print('*****************')
matchDay("supercup")
print('*****************')
for x in range(1,30):
    matchDay(x)
print("\n final match table \n")
print(df)
print(goalscored)
X=df.iloc[:,0:len(teamAbbr)-1].values
t=df.iloc[:,len(teamAbbr)-1].values
X_train,X_test,t_train,t_test=train_test_split(X,t,test_size=0.2,random_state=2)
model =RandomForestClassifier(criterion="gini")
model.fit(X_train,t_train)
if model.predict([[-1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,1]])==1:
	print("Won the match")
else:
	print("Didn't win the match")
