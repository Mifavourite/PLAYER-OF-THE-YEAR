import pandas as pd

# ============================================================
# LORDSFAVOUR METRICS PLAYER OF THE YEAR (L-MPOY)
# ============================================================
#
# A 100-POINT DATA-DRIVEN FOOTBALL PLAYER EVALUATION MODEL
#
# TOTAL = 100 POINTS
#
# TEAM SUCCESS = 45 POINTS
#   World Cup / Global Tournament = 15
#   Continental Competitions       = 12
#   Domestic/National Competitions = 10
#   Other Competitions             = 8
#
# INDIVIDUAL PERFORMANCE = 55 POINTS
#   Personal Statistics            = 20
#   MOTM Volume                    = 10
#   MOTM Efficiency                = 10
#   Discipline                     = 15
#
# ============================================================


# ------------------------------------------------------------
# 1. YEAR BEING EVALUATED
# ------------------------------------------------------------

YEAR = 2026


# ------------------------------------------------------------
# 2. ENTER PLAYER DATA
# ------------------------------------------------------------
#
# Add as many players as necessary.
#
# Team-success scores must stay within these limits:
#
# World Cup / Global Tournament = 0–15
# Continental                  = 0–12
# Domestic/National            = 0–10
# Other Competitions           = 0–8
#
# Personal statistics          = 0–20
#
# Discipline is calculated automatically.
# MOTM volume and efficiency are calculated automatically.
#
# ------------------------------------------------------------

players = [

    {
        "player": "Lionel Messi",
        "matches": 49,
        "motm": 20,

        "world_cup": 10,
        "continental": 0,
        "domestic": 7,
        "other": 0,

        "personal_score": 19,

        "yellow_cards": 3,
        "red_cards": 0
    },

    {
        "player": "Harry Kane",
        "matches": 51,
        "motm": 18,

        "world_cup": 8,
        "continental": 10,
        "domestic": 10,
        "other": 5,

        "personal_score": 20,

        "yellow_cards": 3,
        "red_cards": 0
    },

    {
        "player": "Lamine Yamal",
        "matches": 57,
        "motm": 17,

        "world_cup": 15,
        "continental": 0,
        "domestic": 10,
        "other": 6,

        "personal_score": 18,

        "yellow_cards": 6,
        "red_cards": 0
    },

    {
        "player": "Ousmane Dembélé",
        "matches": 51,
        "motm": 16,

        "world_cup": 0,
        "continental": 12,
        "domestic": 10,
        "other": 8,

        "personal_score": 17,

        "yellow_cards": 1,
        "red_cards": 0
    },

    {
        "player": "Kylian Mbappé",
        "matches": 60,
        "motm": 18,

        "world_cup": 0,
        "continental": 0,
        "domestic": 0,
        "other": 0,

        "personal_score": 20,

        "yellow_cards": 8,
        "red_cards": 0
    },

    {
        "player": "Michael Olise",
        "matches": 69,
        "motm": 17,

        "world_cup": 0,
        "continental": 8,
        "domestic": 10,
        "other": 5,

        "personal_score": 18,

        "yellow_cards": 4,
        "red_cards": 0
    },

    {
        "player": "Rodri",
        "matches": 50,
        "motm": 14,

        "world_cup": 15,
        "continental": 0,
        "domestic": 9,
        "other": 7,

        "personal_score": 15,

        "yellow_cards": 5,
        "red_cards": 1
    }
]


# ------------------------------------------------------------
# 3. CREATE DATAFRAME
# ------------------------------------------------------------

df = pd.DataFrame(players)


# ------------------------------------------------------------
# 4. CHECK THAT TEAM-SUCCESS SCORES ARE VALID
# ------------------------------------------------------------

assert df["world_cup"].between(0, 15).all()
assert df["continental"].between(0, 12).all()
assert df["domestic"].between(0, 10).all()
assert df["other"].between(0, 8).all()

assert df["personal_score"].between(0, 20).all()

assert (df["matches"] > 0).all()
assert (df["motm"] >= 0).all()
assert (df["yellow_cards"] >= 0).all()
assert (df["red_cards"] >= 0).all()


# ------------------------------------------------------------
# 5. TEAM SUCCESS — 45 POINTS
# ------------------------------------------------------------

df["team_success"] = (
    df["world_cup"]
    + df["continental"]
    + df["domestic"]
    + df["other"]
)


# ------------------------------------------------------------
# 6. MOTM VOLUME — 10 POINTS
# ------------------------------------------------------------
#
# The player with the highest number of MOTM awards receives
# the full 10 points.
#
# Everyone else receives a proportional score.
#
# Formula:
#
# Player MOTMs / Highest MOTM total × 10
#
# ------------------------------------------------------------

max_motm = df["motm"].max()

if max_motm > 0:
    df["motm_volume"] = (
        df["motm"] / max_motm
    ) * 10
else:
    df["motm_volume"] = 0


# ------------------------------------------------------------
# 7. MOTM EFFICIENCY — 10 POINTS
# ------------------------------------------------------------
#
# Formula:
#
# MOTM awards / matches played
#
# Example:
#
# 15 MOTMs / 30 matches = 50%
#
# The player with the highest MOTM rate receives 10 points.
#
# ------------------------------------------------------------

df["motm_efficiency_rate"] = (
    df["motm"] / df["matches"]
)

max_efficiency = df["motm_efficiency_rate"].max()

if max_efficiency > 0:
    df["motm_efficiency"] = (
        df["motm_efficiency_rate"]
        / max_efficiency
    ) * 10
else:
    df["motm_efficiency"] = 0


# ------------------------------------------------------------
# 8. DISCIPLINE — 15 POINTS
# ------------------------------------------------------------
#
# Starting score = 15
#
# Yellow card = -1 point
# Red card    = -5 points
#
# Minimum = 0
#
# Formula:
#
# 15 - yellow cards - (red cards × 5)
#
# ------------------------------------------------------------

df["discipline"] = (
    15
    - df["yellow_cards"]
    - (df["red_cards"] * 5)
)

# Discipline can never be negative.
df["discipline"] = df["discipline"].clip(lower=0)


# ------------------------------------------------------------
# 9. FINAL LORDSFAVOUR METRICS SCORE
# ------------------------------------------------------------

df["final_score"] = (
    df["team_success"]
    + df["personal_score"]
    + df["motm_volume"]
    + df["motm_efficiency"]
    + df["discipline"]
)


# ------------------------------------------------------------
# 10. ROUND SCORES
# ------------------------------------------------------------

df["motm_efficiency_rate"] = (
    df["motm_efficiency_rate"] * 100
).round(2)

df["team_success"] = df["team_success"].round(2)
df["motm_volume"] = df["motm_volume"].round(2)
df["motm_efficiency"] = df["motm_efficiency"].round(2)
df["discipline"] = df["discipline"].round(2)
df["final_score"] = df["final_score"].round(2)


# ------------------------------------------------------------
# 11. RANK PLAYERS
# ------------------------------------------------------------
#
# Tie-breakers:
#
# 1. Team Success
# 2. Personal Statistics
# 3. MOTM Efficiency
# 4. MOTM Volume
# 5. Discipline
#
# ------------------------------------------------------------

df = df.sort_values(
    by=[
        "final_score",
        "team_success",
        "personal_score",
        "motm_efficiency",
        "motm_volume",
        "discipline"
    ],
    ascending=False
).reset_index(drop=True)

df["rank"] = df.index + 1


# ------------------------------------------------------------
# 12. DISPLAY LORDSFAVOUR METRICS RANKING
# ------------------------------------------------------------

print()
print("=" * 90)
print(f"LORDSFAVOUR METRICS PLAYER OF THE YEAR — {YEAR}")
print("=" * 90)

ranking = df[
    [
        "rank",
        "player",
        "team_success",
        "personal_score",
        "motm_volume",
        "motm_efficiency",
        "discipline",
        "final_score"
    ]
]

print(
    ranking.to_string(
        index=False,
        formatters={
            "team_success": "{:.2f}".format,
            "personal_score": "{:.2f}".format,
            "motm_volume": "{:.2f}".format,
            "motm_efficiency": "{:.2f}".format,
            "discipline": "{:.2f}".format,
            "final_score": "{:.2f}".format
        }
    )
)


# ------------------------------------------------------------
# 13. DETAILED PLAYER BREAKDOWN
# ------------------------------------------------------------

print()
print("=" * 90)
print("LORDSFAVOUR METRICS — DETAILED BREAKDOWN")
print("=" * 90)

for _, player in df.iterrows():

    print()
    print(
        f"{int(player['rank'])}. "
        f"{player['player']}"
    )

    print("-" * 55)

    print(
        f"World Cup / Global:      "
        f"{player['world_cup']:.2f} / 15"
    )

    print(
        f"Continental:             "
        f"{player['continental']:.2f} / 12"
    )

    print(
        f"Domestic/National:       "
        f"{player['domestic']:.2f} / 10"
    )

    print(
        f"Other Competitions:      "
        f"{player['other']:.2f} / 8"
    )

    print(
        f"TEAM SUCCESS:            "
        f"{player['team_success']:.2f} / 45"
    )

    print(
        f"Personal Statistics:     "
        f"{player['personal_score']:.2f} / 20"
    )

    print(
        f"MOTM Volume:             "
        f"{player['motm_volume']:.2f} / 10"
    )

    print(
        f"MOTM Efficiency:         "
        f"{player['motm_efficiency']:.2f} / 10"
    )

    print(
        f"Discipline:              "
        f"{player['discipline']:.2f} / 15"
    )

    print(
        f"LORDSFAVOUR SCORE:       "
        f"{player['final_score']:.2f} / 100"
    )


# ------------------------------------------------------------
# 14. SAVE RESULTS TO EXCEL
# ------------------------------------------------------------

output_columns = [
    "rank",
    "player",
    "matches",
    "motm",
    "motm_efficiency_rate",
    "world_cup",
    "continental",
    "domestic",
    "other",
    "team_success",
    "personal_score",
    "motm_volume",
    "motm_efficiency",
    "yellow_cards",
    "red_cards",
    "discipline",
    "final_score"
]

filename = f"LordSfavor_Metrics_Player_of_the_Year_{YEAR}.xlsx"

df[output_columns].to_excel(
    filename,
    index=False
)

print()
print("=" * 90)
print(f"Results saved to: {filename}")
print("=" * 90)