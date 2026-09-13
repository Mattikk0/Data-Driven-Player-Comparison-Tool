import queries.transfermarkt_query as tm
import soccerdata as sd
import modules.stats_comparator as sc
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='static/html', static_folder='static/assets')
CORS(app)

@app.route('/', methods=['GET'])
async def index():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
async def find_players():
    if not request.is_json:
        return jsonify({'error': 'Request must contain JSON'}), 415

    data = request.get_json(silent=True) or {}
    player_name = data.get('player_name')
    response_least = [] 
    response_most = []
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400
    try:
        player = await tm.get_player(player_name)
        if player is None:
            return jsonify({'error': 'Player not found'}), 404
        else:
            fbref_client = sd.FBref(leagues="Big 5 European Leagues Combined", seasons="2025-2026")
            similarity = await sc.find_similar_players(player, fbref_client)
            if not similarity:
                return jsonify({'error': f'No similar players found for {player.name}'}), 422

            sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=False))
            reversed_sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True))
            top_similar_players = {player: reversed_sorted_similarity[player] for player in list(reversed_sorted_similarity)[:10]}
            least_similar_players = {player: sorted_similarity[player] for player in list(sorted_similarity)[:10]}
            for player in top_similar_players:
                p = await tm.get_player(player)
                if p is None:
                    continue
                player_data1 = {
                    'name': p.name,
                    'position': p.position,
                    'team': p.team,
                    'value': p.tm_value,
                    'age': p.age,
                    'similarity': top_similar_players[player],
                }
                response_most.append(player_data1)
            for player in least_similar_players:
                p = await tm.get_player(player)
                if p is None:
                    continue
                player_data2 = {
                'name': p.name,
                'position': p.position,
                'team': p.team,
                'value': p.tm_value,
                'age': p.age,
                'similarity': least_similar_players[player],
                }
                response_least.append(player_data2)
            return jsonify({
                "least": response_least,
                "most": response_most
            }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 422
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/player_info', methods=['POST', 'GET'])
async def get_player_info():
    if not request.is_json:
        return jsonify({'error': 'Request must contain JSON'}), 415

    data = request.get_json(silent=True) or {}
    player_name = data.get('player_name')
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400
    try:
        player = await tm.get_player(player_name)
        if player is None:
            return jsonify({'error': 'Player not found'}), 404
        else:
            player_data = {
                'name': player.name,
                'position': player.position,
                'team': player.team,
                'value': player.tm_value,
                'age': player.age,
                'image_url': player.image_url
            }
            return jsonify(player_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
    
