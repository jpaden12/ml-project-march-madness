"""For loading and reading data files

  Typical usage:
      from dataset import Dataset
      ds = Dataset()
      ds.<method_name>()
"""
import pandas as pd

class Dataset():
    """Parser for the march-ml-mania dataset.
    
    This class reads the various .csvs provided and provides methods 
    for accessing the game data.

    Attributes:
        datadir: filepath for data directory
        regular_results: game data for the regular season from 1985-2017
            Detailed game data only available for the 2013 season and later (NaNs pre 2013)
        tourney_results: tourney data from 1985-2017
            Detailed game data only available for the 2013 season and later (NaNs pre 2013)
        compact_headers: column names of compact data
        detailed_headers: column names of detailed data
        teams: dictionary mapping team id to team name
        seasons: season and region data
        seeds: seeds of each team for every season
        slots: tourney bracket layout
    """

    def __init__(self, datadir="march-ml-mania-dataset/"):
        """Initializes dataset attributes."""
        self.datadir = datadir

        regular_comp = pd.read_csv(datadir + "RegularSeasonCompactResults.csv")
        tourney_comp = pd.read_csv(datadir + "TourneyCompactResults.csv")
        regular_det = pd.read_csv(datadir + "RegularSeasonDetailedResults.csv")
        tourney_det = pd.read_csv(datadir + "TourneyDetailedResults.csv")

        self.regular_results = pd.concat((regular_comp.loc[regular_comp['Season'] < 2003], regular_det))
        self.tourney_results = pd.concat((tourney_comp.loc[tourney_comp['Season'] < 2003], tourney_det))

        self.compact_headers = regular_comp.columns.tolist()
        self.detailed_headers = regular_det.columns.tolist()

        df = pd.read_csv(datadir + "Teams.csv")
        self.teams = dict(zip(df.Team_Id, df.Team_Name))
        self.seasons = pd.read_csv(datadir + "Seasons.csv")

        self.seeds = pd.read_csv(datadir + "TourneySeeds.csv")
        self.slots = pd.read_csv(datadir + "TourneySlots.csv")

    def getTeam(self, id):
        """Finds the team name of the given id.
        
        Retrieves the team name corresponding to the given team id from 
        the self.teams dataframe.

        Args:
            id: an integer representing the team id.

        Returns:
            The name of the team as a string.
        """
        return self.teams[id]

    def getYears(self):
        """Gets a list of all the season years.
        
        Retrieves all the unique years from the self.seasons dataframe.
        
        Returns:
            A python list of years with game data.
        """
        return self.seasons.Season.unique().tolist()

    def getSeeds(self, season):
        """Gets the seeds for each team in the given season.
        
        Retrives the team ids and their corresponding seeds for the given 
        season.

        Args:
            season: an integer representing the season to look up.

        Returns:
             A dict mapping team ids to their seeds for the season.
        """
        df = self.seeds.loc[self.seeds['Season'] == season]
        return dict(zip(df.Team, df.Seed))

    def getRegularGames(self, season=None, compact=True):
        """Returns a dataframe for regular season game data.
        
        Retrieves the game data from the regular seasons of the given years, 
        including the detailed game data if compact is False.
        See https://www.kaggle.com/c/march-machine-learning-mania-2017/data 
        for more details.

        Args:
            season: an integer or list of integers for the years of regular 
            season game data to retrieve
            compact: if True only compact data columns will be returned

        Returns:
            A pandas DataFrame containing the relevant regular season data.
        """
        if type(season) is int: season = [season]
        headers = self.compact_headers if compact else self.detailed_headers
        if season is None:
            return self.regular_results[headers]
        return self.regular_results.loc[self.regular_results['Season'].isin(list(season))][headers]

    def getTourneyGames(self, season=None, compact=True):
        """Returns a dataframe for tourney game data.
        
        Retrieves the tourney data from the given years, including the 
        detailed tourney data if compact is False.
        See https://www.kaggle.com/c/march-machine-learning-mania-2017/data 
        for more details.

        Args:
            season: an integer or list of integers for the years of regular 
            season game data to retrieve
            compact: if True only compact data columns will be returned

        Returns:
            A pandas DataFrame containing the relevant tourney data.
        """
        if type(season) is int: season = [season]
        headers = self.compact_headers if compact else self.detailed_headers
        if season is None:
            return self.tourney_results[headers]
        return self.tourney_results.loc[self.tourney_results['Season'].isin(list(season))][headers]