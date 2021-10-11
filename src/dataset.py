from pathlib import Path

import pandas as pd

from src.utils import read_json

DATA_PATH = Path("data/")


def concat_dataset(data_path: Path=DATA_PATH) -> pd.DataFrame:
    """
    Concatenate skaters datasets.
    """
    years = range(2016, 2021)
    df = pd.DataFrame()
    for year in years:
        print(f"Data year: {year}")
        df = df.append(pd.read_csv(data_path.joinpath(f"raw/skaters_{year}.csv")))
    return df


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame.
    """
    df = df.query("situation == 'all'")
    df = df.query("icetime >= 6000")
    df.sort_values(["name", "season"], ascending=True, inplace=True)
    df.reset_index(inplace=True)
    return df


def make_dataset(data_path: Path, project_path=Path("./")):
    """
    Create the final dataset for the dashboard.
    """
    df = concat_dataset(data_path=data_path)
    df = clean_df(df)
    players = read_json(project_path.joinpath("config/players.json"))
    score = Score(skaters=df, players=players)
    score.make()
    return score.shooting_df


class Score:
    
    def __init__(self, skaters: pd.DataFrame, players: dict) -> None:
        self.skaters = skaters
        self.players = players
        self.shooting_df = pd.DataFrame()
        self.physical_df = pd.DataFrame()
        self.defending_df = pd.DataFrame()
        self.experience_df = pd.DataFrame()
        self.passing_df = pd.DataFrame()

    def shooting(self):
        """
        Create the shooting DataFrame for the MTL habs.
        """
        self.shooting_df = self.skaters[['season', 'name']].copy(deep=True)
        # Create metrics per game
        self.skaters['goal_pct'] = self.skaters['I_F_goals'] / self.skaters['I_F_shotsOnGoal']
        self.skaters['goal_per_game'] = self.skaters['I_F_goals'] / self.skaters['games_played']
        self.skaters['shot_per_game'] = self.skaters['I_F_highDangerShots'] / self.skaters['games_played']
        self.skaters['primary_per_game'] = self.skaters['I_F_primaryAssists'] / self.skaters['games_played']
        self.skaters['secondary_per_game'] = self.skaters['I_F_secondaryAssists'] / self.skaters['games_played']
        self.skaters['hits_per_game'] = self.skaters['I_F_hits'] / self.skaters['games_played']
        self.skaters['pim_per_game'] = self.skaters['I_F_penalityMinutes'] / self.skaters['games_played']
        # Compute Rank
        self.shooting_df['shooting'] = self.skaters.groupby(["season"])[
            ['goal_per_game', 'shot_per_game', 'goal_pct']].rank(pct=True).mean(axis=1)
        self.shooting_df['passing'] = self.skaters.groupby("season")[
            ['primary_per_game', 'secondary_per_game']].rank(pct=True).mean(axis=1)
        self.shooting_df['physical'] = self.skaters.groupby("season")[
            ['hits_per_game', "pim_per_game"]].rank(pct=True).mean(axis=1)
        # Adjusted Shooting
        adjusted_shooting = self.shooting_df.groupby(["name"])[
            'shooting', 'passing', 'physical'].ewm(com=0.2).mean().reset_index().drop("level_1", axis=1)
        adjusted_shooting.columns = ['name_x', 'adjusted_shooting', 'adjusted_passing', 'adjusted_physical']
        self.shooting_df = pd.concat([self.shooting_df, adjusted_shooting], axis=1)
        self.shooting_df.drop(['name_x', 'shooting', 'passing', 'physical'], axis=1, inplace=True)
        mtl2020 = self.shooting_df.loc[self.shooting_df['name'].apply(lambda x: x in self.players['2020']), :].query('season==2019')
        mtl2021 = self.shooting_df.loc[self.shooting_df['name'].apply(lambda x: x in self.players['2021']), :].query('season==2020')
        self.shooting_df = pd.concat([mtl2020, mtl2021], axis=0)
        # Pretty
        self.shooting_df['shooting_score'] = self.shooting_df['adjusted_shooting'].apply(lambda x: int(x * 100))
        self.shooting_df['passing_score'] = self.shooting_df['adjusted_passing'].apply(lambda x: int(x * 100))
        self.shooting_df['physical_score'] = self.shooting_df['adjusted_physical'].apply(lambda x: int(x * 100))
        self.shooting_df.drop(["adjusted_shooting", 'adjusted_passing', 'adjusted_physical'], axis=1, inplace=True)
        self.shooting_df.sort_values("physical_score", ascending=False, inplace=True)
        self.shooting_df.reset_index(drop=True, inplace=True)

    def passing(self):
        pass

    def physical(self):
        pass

    def defending(self):
        pass

    def experience(self):
        pass

    def make(self):
        self.shooting()
        self.passing()
        self.physical()
        self.defending()
        self.experience()


def shooting_score(skaters: pd.DataFrame, players: dict=None, pretty: bool=True) -> pd.DataFrame:
    """
    Create the shooting DataFrame for the MTL habs.
    """
    shooting = skaters[['season', 'name']].copy(deep=True)
    # Create metrics per game
    skaters['goal_pct'] = skaters['I_F_goals'] / skaters['OnIce_F_shotsOnGoal']
    skaters['goal_per_game'] = skaters['I_F_goals'] / skaters['games_played']
    skaters['shot_per_game'] = skaters['OnIce_F_shotsOnGoal'] / skaters['games_played']
    # Compute Rank
    shooting['shooting'] = skaters.groupby("season")[
        ['goal_per_game', 'shot_per_game', 'goal_pct']].rank(pct=True).mean(axis=1)
    # Adjusted Shooting
    adjusted_shooting = shooting.groupby(["name"])[
        'shooting'].ewm(com=0.2).mean().to_frame().reset_index().drop("level_1", axis=1)
    adjusted_shooting.columns = ['name_x', 'adjusted_shooting']
    # Concat
    shooting = pd.concat([shooting, adjusted_shooting], axis=1)
    shooting.drop(['name_x', 'shooting'], axis=1, inplace=True)
    if players:
        mtl2020 = shooting.loc[shooting['name'].apply(lambda x: x in players['2020']), :].query('season==2019')
        mtl2021 = shooting.loc[shooting['name'].apply(lambda x: x in players['2021']), :].query('season==2020')
        shooting = pd.concat([mtl2020, mtl2021], axis=0)
    if pretty:
        shooting['shooting_score'] = shooting['adjusted_shooting'].apply(lambda x: int(x * 100))
        shooting.drop("adjusted_shooting", axis=1, inplace=True)
    else:
        shooting.rename(columns={"adjusted_shooting": "shooting_score"}, inplace=True)
    return shooting





if __name__ == '__main__':
    score = make_dataset(DATA_PATH)
    score.to_csv(DATA_PATH.joinpath("processed/scores.csv"), index=False)
