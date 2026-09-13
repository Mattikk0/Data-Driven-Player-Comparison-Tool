import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import DictVectorizer
import math

def get_stat_names(df):
    col_list = df.columns.tolist()
    stat_list = []
    for col in col_list:
        if isinstance(col, tuple):
            if not col[1] == "":
                stat_list.append(col)
        else:
                continue
    return stat_list

def get_stat_values(df, player):
    stat_names = get_stat_names(df)
    row = df.xs(player, level="player").iloc[0] if "player" in df.index.names else df.loc[player]
    stats = {}
    for stat_name in stat_names:
        value = row[stat_name]
        stats[stat_name] = 0.0 if pd.isna(value) else value

    return {player: stats}

def count_average(stats):
    totals = {}
    player_count = len(stats)
    for player in stats:
        if not isinstance(player, tuple):
            for stat_name in stats[player]:
                totals[stat_name] = totals.get(stat_name, 0) + stats[player][stat_name]
    avg_stats = {stat_name: total / player_count for stat_name, total in totals.items()}
    return avg_stats

def count_standard_deviation(stats, average):
    player_count = len(stats)
    totals = {}
    for player in stats:
        if not isinstance(player, tuple):
            for stat_name in stats[player]:
                totals[stat_name] = totals.get(stat_name, 0) + ((stats[player][stat_name] - average[stat_name]) ** 2)
    sd = {stat_name: math.sqrt(sum/player_count) for stat_name, sum in totals.items()}
    return sd

def count_z_score(stats, avr, sd):
    z_scores = {}
    for player in stats:
        if not isinstance(player, tuple):
            for stat_name in stats[player]:
                if sd[stat_name] == 0:
                    z_scores.setdefault(player, {})[stat_name] = 0.0
                else:
                    z_scores.setdefault(player, {})[stat_name] = (stats[player][stat_name] - avr[stat_name]) / sd[stat_name]
   
    return z_scores


def count_similarity(single_stats, all_stats):
    temp_combined = single_stats | all_stats
    avr = count_average(temp_combined)
    sd = count_standard_deviation(temp_combined, avr)
    searched_player_z_score = count_z_score(single_stats, avr, sd)
    other_players_z_scores = count_z_score(all_stats, avr, sd)
    dv = DictVectorizer(sparse=False)
    matrix = dv.fit_transform(other_players_z_scores.values())
    vector = dv.transform(searched_player_z_score.values())
    similarities = cosine_similarity(vector, matrix)[0]
    return dict(zip(other_players_z_scores, similarities))
    
    


	
