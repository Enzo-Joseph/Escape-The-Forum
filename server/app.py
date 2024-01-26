from flask import Flask, jsonify
from flask_cors import CORS
import format_data
import connect_gsheet

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/dashboard_data/', methods=['GET'])
def dashboard_data():    
    escape_game_data = connect_gsheet.get_data_from_gsheet()
    time_per_question = format_data.formatChartData(escape_game_data['time_per_question_labels'], escape_game_data['time_per_question_values'], color = "#414487FF", chartType='bar')
    time_per_question['title'] = "Temps passé par énigme en minutes"

    scoreboard = format_data.formatChartData(escape_game_data['scoreboard_labels'], escape_game_data['scoreboard_values'], color = "#2A788EFF", chartType='hbar')
    scoreboard['title'] = "Temps par joueur en minutes"

    participants_by_hour = format_data.formatChartData(escape_game_data['participants_by_hour_labels'], escape_game_data['participants_by_hour_values'], color = "#22A884FF", chartType='bar')
    participants_by_hour['title'] = "Nombre de participants par heure"

    return jsonify({
        'charts': {
            'participantsByHour': participants_by_hour,
            'timePerQuestion': time_per_question,
            'scoreboard': scoreboard,
        },
        'cards': [
            {
                'title': "Durée moyenne des parties",
                'text': str(escape_game_data['average_time_per_game']) + " minutes",
            },
            {
                'title': "Nombres de joueurs",
                'text': escape_game_data['number_of_users'],
            },
            {
                'title': "Meilleur joueur",
                'text': escape_game_data['best_player'],
            }
        ],
        'json_data': {
            'time_per_question':{
                'labels': escape_game_data['time_per_question_labels'],
                'values': escape_game_data['time_per_question_values'],
            },
            'scoreboard':{
                'labels': escape_game_data['scoreboard_labels'],
                'values': escape_game_data['scoreboard_values'],
            },
            'participants_by_hour':{
                'labels': escape_game_data['participants_by_hour_labels'],
                'values': escape_game_data['participants_by_hour_values'],
            },
            'average_time_per_game': escape_game_data['average_time_per_game'],
            'number_of_users': escape_game_data['number_of_users'],
            'best_player': escape_game_data['best_player'],
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5005)      