from dataclasses import dataclass
import string

@dataclass(frozen=True) 
class FPT:
    fbref: string
    tm: string

fbref_positions_to_tm = [
    FPT(fbref="DF", tm="CB"), FPT(fbref="DF", tm="LB"), FPT(fbref="DF", tm="RB"),
    FPT(fbref="MF", tm="CM"), FPT(fbref="MF", tm="DM"), FPT(fbref="MF", tm="AM"), FPT(fbref="MF", tm="LM"), FPT(fbref="MF", tm="RM"), FPT(fbref="MF", tm="LB"), FPT(fbref="MF", tm="RB"),
    FPT(fbref="FW", tm="CF"), FPT(fbref="FW", tm="LW"), FPT(fbref="FW", tm="RW")
]