import requests

API_URL = 'http://localhost:8000'
clubs = []

class Player:
    def __init__(self, player_id, name, position, team, tm_value=None, age=None, image_url=None):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.tm_value = tm_value
        self.age = age
        self.image_url = image_url

async def get_profile(player_id):
    response = requests.get(API_URL + f'/players/{player_id}/profile')
    if response.status_code == 200:
        return response
    else:
        return await get_profile(player_id)
    
async def get_player(player_name):
    response = requests.get(API_URL + f'/players/search/{player_name}') 
    if response.status_code == 200:
        results = response.json().get('results', [])
        if not results:
            return None
        i=0
        while True:
            data = results[i]
            profile = await get_profile(data.get("id"))
            profile_data = profile.json() if profile.status_code == 200 else {}
            if not profile_data.get('isRetired'):
                break
            i+=1
        player =  Player(
            player_id=data.get('id'),
            name=data.get('name'),
            position=data.get('position'),
            team=data.get('club').get('name'),
            tm_value=data.get('marketValue'),
            age=data.get('age'),
            image_url=profile_data.get('imageUrl')
        )
        return player
    else:
        return await get_player(player_name)
