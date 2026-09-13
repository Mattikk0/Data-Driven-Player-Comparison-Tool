import modules.data_processing as dp
import queries.fbref_query as fbref
from unidecode import unidecode
import soccerdata as sd

async def find_similar_players(player, fb):
    combined = await fbref.get_all_players_stats(player, fb)
    players = combined.index.get_level_values("player")
    stat_matrix = {}
    for fbref_player in players:
        stats = dp.get_stat_values(combined, fbref_player)
        stat_matrix[unidecode(fbref_player)] = stats[fbref_player]
    try:
        searched_player_name = unidecode(player.name)
        searched_player = {searched_player_name: stat_matrix[searched_player_name]}
        del stat_matrix[searched_player_name]
    except KeyError:
        raise ValueError(f"No stats found for player: {player.name}")

    return dp.count_similarity(searched_player, stat_matrix)


