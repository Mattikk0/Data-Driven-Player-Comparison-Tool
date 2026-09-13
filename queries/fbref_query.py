import modules.config as config

async def get_all_players_stats(player, fbref):
    merge_keys = ["league", "season", "team", "player"]
    def prepare_df(df, keep_metadata=False):
        if keep_metadata:
            return df
        cols_to_drop = []
        for c in df.columns:
            col_name = c[0] if isinstance(c, tuple) else c
            if col_name in ["nation", "pos", "age", "born"] and col_name not in merge_keys:
                cols_to_drop.append(c)

        return df.drop(columns=cols_to_drop)
    
    if player.position == "GK":
        misc = prepare_df(fbref.read_player_season_stats(stat_type="misc"), keep_metadata=True)
        keeper = prepare_df(fbref.read_player_season_stats(stat_type="keeper"))
        playing_time = prepare_df(fbref.read_player_season_stats(stat_type="playing_time"))
   
        temp = misc.merge(keeper, on=merge_keys, how="outer")
        temp = temp.merge(playing_time, on=merge_keys, how="outer")
   
        pos_series = temp["pos"] if "pos" in temp.columns else temp.xs("pos", axis=1, level=0).iloc[:, 0]
        combined = temp[pos_series.str.contains("GK", na=False)]
    else:
        misc = prepare_df(fbref.read_player_season_stats(stat_type="misc"), keep_metadata=True)
        standard = prepare_df(fbref.read_player_season_stats(stat_type="standard"))
        shooting = prepare_df(fbref.read_player_season_stats(stat_type="shooting"))
        playing_time = prepare_df(fbref.read_player_season_stats(stat_type="playing_time"))
  
        temp = misc.merge(standard, on=merge_keys, how="outer")
        temp = temp.merge(shooting, on=merge_keys, how="outer")
        temp = temp.merge(playing_time, on=merge_keys, how="outer")
 
        target_fbref_positions = [
            p.fbref for p in config.fbref_positions_to_tm if player.position in p.tm
        ]
        pos_series = temp["pos"] if "pos" in temp.columns else temp.xs("pos", axis=1, level=0).iloc[:, 0]
  
        pattern = "|".join(target_fbref_positions)
        combined = temp[pos_series.str.contains(pattern, na=False)]
    return combined


    

