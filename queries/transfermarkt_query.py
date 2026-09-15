import asyncio
import aiohttp
import random
import weakref
import threading
import time

PROFILE_LIMITS = weakref.WeakKeyDictionary()
API_URL = 'http://localhost:8000'
REQUEST_INTERVAL = 1.5
RATE_LOCK = threading.Lock()
NEXT_REQUEST_AT = 0.0
PLAYER_CACHE = {}
clubs = []

def get_profile_limit():
    loop = asyncio.get_running_loop()
    limit = PROFILE_LIMITS.get(loop)
    if limit is None:
        limit = asyncio.Semaphore(2)
        PROFILE_LIMITS[loop] = limit
    return limit

async def wait_for_request_slot():
    global NEXT_REQUEST_AT
    with RATE_LOCK:
        now = time.monotonic()
        request_at = max(now, NEXT_REQUEST_AT)
        NEXT_REQUEST_AT = request_at + REQUEST_INTERVAL
    await asyncio.sleep(request_at - now)

class Player:
    def __init__(self, player_id, name, position, team, tm_value=None, age=None, image_url=None):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.tm_value = tm_value
        self.age = age
        self.image_url = image_url

async def get_profile(player_id, bug_ctr=0, session=None):
    if session is None:
        async with aiohttp.ClientSession() as new_session:
            return await get_profile(player_id, bug_ctr, new_session)

    async with get_profile_limit():
        await wait_for_request_slot()
        async with session.get(API_URL + f'/players/{player_id}/profile') as response:
            if response.status == 200:
                return await response.json()
            if response.status == 500:
                return None
            retry_after = response.headers.get('Retry-After') if response.status == 403 else None

    delay = float(retry_after) if retry_after else min(40, 2**bug_ctr) + random.uniform(0, 1)
    await asyncio.sleep(delay)
    return await get_profile(player_id, bug_ctr+1, session)
    
async def get_player(player_name, bug_ctr=0, session=None):
    cache_key = player_name.casefold()
    if cache_key in PLAYER_CACHE:
        return PLAYER_CACHE[cache_key]

    if session is None:
        async with aiohttp.ClientSession() as new_session:
            return await get_player(player_name, bug_ctr, new_session)

    retry_after = None
    async with get_profile_limit():
        await wait_for_request_slot()
        async with session.get(API_URL + f'/players/search/{player_name}') as response:
            if response.status == 200:
                results = (await response.json()).get('results', [])
            else:
                retry_after = response.headers.get('Retry-After') if response.status == 403 else None
            

    if response.status == 200:
        if not results:
            return None
        for data in results:
            profile_data = await get_profile(data.get("id"), session=session)
            if profile_data is None:
                continue
            if profile_data.get('isRetired'):
                continue
            break
        else:
            return None
        player =  Player(
            player_id=data.get('id'),
            name=data.get('name'),
            position=data.get('position'),
            team = data.get('club', {}).get('name'),
            tm_value=data.get('marketValue'),
            age=data.get('age'),
            image_url=profile_data.get('imageUrl')
        )
        PLAYER_CACHE[cache_key] = player
        return player

    delay = float(retry_after) if retry_after else min(40, 2**bug_ctr) + random.uniform(0, 1)
    await asyncio.sleep(delay)
    return await get_player(player_name, bug_ctr+1, session)
