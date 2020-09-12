import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
import requests
from datetime import datetime
import numpy as np
df = pd.read_csv('ipl.csv')
#df.head()
# --- Data Cleaning ---
# Removing unwanted columns
columns_to_remove = ['mid', 'venue', 'batsman', 'bowler', 'striker', 'non-striker']
df.drop(labels=columns_to_remove, axis=1, inplace=True)
#df.head()
#df['bat_team'].unique()
# Keeping only consistent teams
consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Daredevils', 'Sunrisers Hyderabad']
df = df[(df['bat_team'].isin(consistent_teams)) & (df['bowl_team'].isin(consistent_teams))]
# Removing the first 5 overs data in every match
df = df[df['overs']>=5.0]
#df.head()
#print(df['bat_team'].unique())
#print(df['bowl_team'].unique())
# Converting the column 'date' from string into datetime object
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
# --- Data Preprocessing ---
# Converting categorical features using OneHotEncoding method
encoded_df = pd.get_dummies(data=df, columns=['bat_team', 'bowl_team'])
#encoded_df.head()
#encoded_df.columns
# Rearranging the columns
encoded_df = encoded_df[['date', 'bat_team_Chennai Super Kings', 'bat_team_Delhi Daredevils', 'bat_team_Kings XI Punjab',
              'bat_team_Kolkata Knight Riders', 'bat_team_Mumbai Indians', 'bat_team_Rajasthan Royals',
              'bat_team_Royal Challengers Bangalore', 'bat_team_Sunrisers Hyderabad',
              'bowl_team_Chennai Super Kings', 'bowl_team_Delhi Daredevils', 'bowl_team_Kings XI Punjab',
              'bowl_team_Kolkata Knight Riders', 'bowl_team_Mumbai Indians', 'bowl_team_Rajasthan Royals',
              'bowl_team_Royal Challengers Bangalore', 'bowl_team_Sunrisers Hyderabad',
              'overs', 'runs', 'wickets', 'runs_last_5', 'wickets_last_5', 'total']]
# Splitting the data into train and test set
X_train = encoded_df.drop(labels='total', axis=1)[encoded_df['date'].dt.year <= 2016]
X_test = encoded_df.drop(labels='total', axis=1)[encoded_df['date'].dt.year >= 2017]
y_train = encoded_df[encoded_df['date'].dt.year <= 2016]['total'].values
y_test = encoded_df[encoded_df['date'].dt.year >= 2017]['total'].values
# Removing the 'date' column
X_train.drop(labels='date', axis=True, inplace=True)
X_test.drop(labels='date', axis=True, inplace=True)
regressor = LinearRegression()
regressor.fit(X_train,y_train)
filename = 'first-innings-score-lr-model.pkl'
pickle.dump(regressor, open(filename, 'wb'))


def predict(batting_team,bowling_team,overs,runs,wickets,runs_in_prev_5 ,wickets_in_prev_5):
    temp_array = list()
    if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
    elif batting_team == 'Delhi Daredevils':
        temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
    elif batting_team == 'Kings XI Punjab':
        temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
    elif batting_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
    elif batting_team == 'Mumbai Indians':
        temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
    elif batting_team == 'Rajasthan Royals':
        temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
    elif batting_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
    elif batting_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

    if bowling_team == 'Chennai Super Kings':
        temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
    elif bowling_team == 'Delhi Daredevils':
        temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
    elif bowling_team == 'Kings XI Punjab':
        temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
    elif bowling_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
    elif bowling_team == 'Mumbai Indians':
        temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
    elif bowling_team == 'Rajasthan Royals':
        temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
    elif bowling_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
    elif bowling_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

    overs = float(overs)
    runs = int(runs)
    wickets = int(wickets)
    runs_in_prev_5 = int(runs_in_prev_5)
    wickets_in_prev_5 = int(wickets_in_prev_5)
    temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
    data = np.array([temp_array])
    my_prediction = int(regressor.predict(data)[0])
    print(my_prediction)

class ScoreGet:
    def __init__(self):
        """
        Declaring the endpoints, apikey
        """
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "OwLxEcGPb4XauHDjEw1ntQZc0Gb2"
        self.unique_id = ""  # unique to every match

    def get_unique_id(self):
        """
        Returns Indian cricket teams match id, if the match is Live
        :return:
        """
        uri_params = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found = 0
        s = input("Enter the country name whose score you want to fetch\n")
        for i in resp_dict['matches']:
            if (i['team-1'] ==s  or i['team-2'] == "India") and i['matchStarted']:
                todays_date = datetime.today().strftime('%Y-%m-%d')
                #todays_date = "2020-03-03"
                if todays_date == i['date'].split("T")[0]:
                    uid_found = 1
                    self.unique_id = i['unique_id']
                    print(self.unique_id)
                    break
        if not uid_found:
            self.unique_id = -1

        send_data = self.get_score(self.unique_id)
        return send_data

    def get_score(self, unique_id):
        data = ""  # stores the cricket match data
        if unique_id == -1:
            data = "No India matches today"
        else:
            uri_params = {"apikey": self.api_key, "unique_id": self.unique_id}
            resp = requests.get(self.url_get_score, params=uri_params)
            data_json = resp.json()
            # print(data_json)
            try:
                data = "Here's the score : " + "\n" + data_json['stat'] + '\n' + data_json['score']
            except KeyError as e:
                data = "Something went wrong"
        return data


if __name__ == "__main__":
    check=input('DO YOU WANT CURRENT SCORE [y/n]')
    if check=='y':
        match_obj = ScoreGet()
        send_message = match_obj.get_unique_id()
        print(send_message)
        from twilio.rest import Client
    
        account_sid = 'ACbcac77f3894e01d8da56899550271805'
        auth_token = '2a8770e08e26667481a3f5d5229bebc7'
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=send_message, from_='whatsapp:+14155238886',
                                         to='whatsapp:+918586997939')
    else:
        #batting_team,bowling_team,overs,runs,wickets,runs_in_prev_5 ,wickets_in_prev_5
        predict('Chennai Super Kings','Delhi Daredevils',10,42,3,21,2)
