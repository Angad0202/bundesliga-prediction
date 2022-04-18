# bundesliga-prediction
using lib request, beautifulsoup4 to scrap the data from website and on basis of that trying to perform a prediction

This program is collecting the information from the website of bundesliga. The information collected is that of the fixtures 
the goals scored from matchday 1 till latest matchday that is played.


after collecting the information of fixtures and on basis of that, the code is storing that data of the team that won
the match(denoted by 1) and lost (denoted by 0) in a dataframe matrix type. (-1 denotes that the match is between the team itself(which is not possible)

and after all the data has been collected, the program will trying to perform a randomforest to predict if the team will win its next match based on the previous matches.

with the use of lib such as request , to send simple http request to the bundesliga website
and also beautifulsoup4, to pull out the data from the website.

Steps are as follows:-

1. Clone the repo OR wget https://raw.githubusercontent.com/Angad0202/bundesliga-prediction/main/script.py
2. pip3 install pandas numpy beautifulsoup4 requests sklearn
3. python3 script.py
