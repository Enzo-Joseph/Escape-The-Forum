import gspread
import os
from datetime import datetime
import pandas as pd
import numpy as np

NB_QUESTIONS = 6


def get_data_from_gsheet() -> dict:
    '''
    Return a dictionary containing the treated data from the google sheet
    keys : 'time_per_question_labels', 'time_per_question_values', 'average_time_per_game', 'scoreboard_values', 'scoreboard_labels', 'best_player', 'participants_by_hour_values', 'participants_by_hour_labels', 'number_of_users'
    '''
    
    escape_game_data = {}
    script_dir = os.path.dirname(__file__)

    #connect to the service account
    gc = gspread.service_account(filename=script_dir+"\\creds.json")

    # get worksheet from google sheet
    worksheet = gc.open("Data from Chatfuel 3").sheet1
    usernames_worksheet = gc.open("Data from Chatfuel 4").sheet1

    # get the data as a dataframe
    df_game_data = pd.DataFrame(worksheet.get_all_records())
    df_game_data['timestamp'] = pd.to_datetime(df_game_data['timestamp'], format='%Y-%m-%d %H:%M:%S')
    unique_users = list(set(df_game_data['chatfuel user id']))
    
    # get the usernames
    df_usernames = pd.DataFrame(usernames_worksheet.get_all_records())
    df_game_data = df_game_data.merge(df_usernames[['chatfuel user id', 'name']], on='chatfuel user id', how='left') # Add the 'name' column from df_usernames
    df_game_data['name'] = df_game_data['name'].fillna('Unknown') # Fill missing names with 'Unknown'

    # get the mean time spent by question
    df_users_time_per_question = get_users_time_per_question(df_game_data, unique_users) # columns : user_id  question_1  question_2  question_3  question_4  question_5  question_6  total_time
    mean_time_per_question = df_users_time_per_question.drop(columns=['user_id']).mean(axis = 0) # returns a series

    escape_game_data['time_per_question_labels'] = ['Question '+str(i+1) for i in range(NB_QUESTIONS)]
    escape_game_data['time_per_question_values'] = mean_time_per_question.values.tolist()[:NB_QUESTIONS]
    escape_game_data['average_time_per_game'] = round(mean_time_per_question['total_time'], 2)

    # get the scoreboard
    scoreboard = df_users_time_per_question[['user_id', 'total_time']].sort_values(by=['total_time'])
    scoreboard = scoreboard[scoreboard['total_time'] != 0]
    scoreboard['rank'] = range(1, len(scoreboard)+1)    
    scoreboard = scoreboard.merge(df_usernames[['chatfuel user id', 'name']], left_on='user_id', right_on='chatfuel user id', how='left')
    scoreboard = scoreboard.drop(columns=['user_id', 'chatfuel user id'])

    escape_game_data['scoreboard_values'] = scoreboard['total_time'].tolist()
    escape_game_data['scoreboard_labels'] = [str(x) for x in scoreboard['name'].tolist()]
    escape_game_data['best_player'] = scoreboard.iloc[0]['name']

    # get number of participants by hour
    participants_by_hour = df_game_data.drop_duplicates(subset=['chatfuel user id'], keep='first')['timestamp'].dt.hour.value_counts().sort_index() # index is the hour, value is the number of participants

    escape_game_data['participants_by_hour_values'] = participants_by_hour.values.tolist()
    escape_game_data['participants_by_hour_labels'] = [str(x+1) for x in participants_by_hour.index.tolist()]

    # get the number of games
    escape_game_data['number_of_users'] = len(unique_users)


    return escape_game_data


def get_users_time_per_question(df_game_data : pd.DataFrame, users : list) -> pd.DataFrame:
    '''
    Return a dataframe containing the time spent for each users on each question
    The columns are : 'user_id', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'total_time'
    '''

    # time_spent = np.array(users).reshape(-1, 1)
    time_spent = np.zeros((len(users), NB_QUESTIONS+2)) # one column for the user id, and one for the total time spent
    for i, user in enumerate(users):
        time_spent[i][0] = user
        time_by_question = get_time_by_question(df_game_data, user)

        time_spent[i][1:7] = time_by_question[:]
        time_spent[i][-1] = np.sum(time_by_question)

    time_spent = time_spent[~np.isnan(time_spent).any(axis=1)] # remove invalid rows : users who haven't finished
    df_game_data = pd.DataFrame(time_spent, columns=['user_id', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'total_time'])

    return df_game_data
    


def get_time_by_question(df_game_data : pd.DataFrame, user_id : int) -> np.array :
    '''
    Return the time spent by user on each question
    '''
    time_by_question = np.zeros(NB_QUESTIONS)

    for i in range(NB_QUESTIONS):
        df_filtered = df_game_data[(df_game_data['chatfuel user id'] == user_id) & (df_game_data['step'].str.contains('enigme_'+str(i+1)))]

        # check if user has finished the question
        if df_filtered['step'].str.contains('end').any():
            # in that case, keep the last entry
            df_filtered = df_filtered.iloc[-2:]
            time_by_question[i] = (df_filtered.iloc[1]['timestamp'] - df_filtered.iloc[0]['timestamp']).seconds / 60 # in minutes
        else:
            return np.full(NB_QUESTIONS, np.nan)

    return time_by_question
    
    

if __name__ == "__main__":
    get_data_from_gsheet()