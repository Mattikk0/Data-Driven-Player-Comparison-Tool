import queries.transfermarkt_query as tm
import soccerdata as sd
import modules.stats_comparator as sc
import requests
import aiohttp
import asyncio
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='static/html', static_folder='static/assets')
CORS(app)
PLAYER_NAME_CACHE = ""
FBREF_CLIENT = None

async def fetch_one_player(player_name, session, pack_limit):
    async with pack_limit:
        return await tm.get_player(player_name, session=session)

async def fetch_players(player_names, session, pack_limit):
    return await asyncio.gather(
        *(fetch_one_player(player_name, session, pack_limit) for player_name in player_names)
    )

@app.route('/', methods=['GET'])
async def index():
    global FBREF_CLIENT
    FBREF_CLIENT = sd.FBref(leagues="Big 5 European Leagues Combined", seasons="2025-2026")
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
async def find_players():
    global PLAYER_NAME_CACHE
    global FBREF_CLIENT
    if not request.is_json:
        return jsonify({'error': 'Request must contain JSON'}), 415

    player_name = PLAYER_NAME_CACHE
    response_least = [] 
    response_most = []
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400
    try:
        player = await tm.get_player(player_name)
        if player is None:
            return jsonify({'error': 'Player not found'}), 404
        else:
            
            similarity = await sc.find_similar_players(player, FBREF_CLIENT)
            if not similarity:
                return jsonify({'error': f'No similar players found for {player.name}'}), 422

            sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=False))
            reversed_sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True))
            top_similar_players = {player: reversed_sorted_similarity[player] for player in list(reversed_sorted_similarity)[:5]}
            least_similar_players = {player: sorted_similarity[player] for player in list(sorted_similarity)[:5]}
            async with aiohttp.ClientSession() as session:
                pack_limit = asyncio.Semaphore(2)
                top_players, least_players = await asyncio.gather(
                    fetch_players(top_similar_players, session, pack_limit),
                    fetch_players(least_similar_players, session, pack_limit),
                )
            for player, p in zip(top_similar_players, top_players):
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
            for player, p in zip(least_similar_players, least_players):
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
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Player data service is unavailable on localhost:8000'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/player_info', methods=['POST', 'GET'])
async def get_player_info():
    global PLAYER_NAME_CACHE
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
            PLAYER_NAME_CACHE = player.name
            return jsonify(player_data), 200
    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException):
            return jsonify({'error': 'Player data service is unavailable on localhost:8000'}), 503
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
    
