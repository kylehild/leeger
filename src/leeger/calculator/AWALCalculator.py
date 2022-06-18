from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.WeekNavigator import WeekNavigator
from src.leeger.util.YearNavigator import YearNavigator


class AWALCalculator(YearCalculator):
    """
    Used to calculate all AWAL stats.
    """

    @classmethod
    @validateYear
    def getAWAL(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        AWAL stands for Adjusted Wins Against the League.
        It is exactly that, an adjustment added to the Wins Against the League (or WAL) of a team.
        In simple terms, this stat more accurately represents how many WAL any given team should have.
        i.e. A team with 6.3 AWAL "deserves" 6.3 WAL.

        AWAL = W * (1/L) + T * (0.5/L)
        Where:
        W = Teams outscored in a week
        T = Teams tied in a week
        L = Opponents in a week (usually league size - 1)

        Returns the number of Adjusted Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAWAL[teamId] = Deci(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                opponentsInWeek = (len(week.matchups) * 2) - 1
                teamsOutscored = dict()
                teamsTied = dict()
                for teamId in allTeamIds:
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                allTeamIdsAndScoresForWeek = WeekNavigator.getTeamIdsAndScores(week)
                allScores = allTeamIdsAndScoresForWeek.values()

                for teamId in allTeamIdsAndScoresForWeek.keys():
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                    score = allTeamIdsAndScoresForWeek[teamId]
                    for s in allScores:
                        if score > s:
                            teamsOutscored[teamId] += 1
                        if score == s:
                            teamsTied[teamId] += 1
                    # remove 1 from the teamsTied tracker since we will always find a tie for this team's score in the list of all scores in the week
                    teamsTied[teamId] -= 1
                    # calculate the AWAL for each team for this week
                    teamIdAndAWAL[teamId] += (
                            (Deci(teamsOutscored[teamId])
                             * (Deci(1) / Deci(opponentsInWeek)))
                            + (Deci(teamsTied[teamId])
                               * (Deci(0.5) / Deci(opponentsInWeek))))

        return teamIdAndAWAL

    @classmethod
    @validateYear
    def getAWALPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndAWAL = AWALCalculator.getAWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndAwalPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAwalPerGame[teamId] = teamIdAndAWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndAwalPerGame

    @classmethod
    @validateYear
    def getOpponentAWAL(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League for each team's opponents in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentAWAL[teamId] = Deci(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                opponentsInWeek = (len(week.matchups) * 2) - 1
                teamsOutscored = dict()
                teamsTied = dict()
                for teamId in allTeamIds:
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                allTeamIdsAndOpponentScoresForWeek = WeekNavigator.getTeamIdsAndOpponentScores(week)
                allScores = allTeamIdsAndOpponentScoresForWeek.values()

                for teamId in allTeamIdsAndOpponentScoresForWeek.keys():
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                    score = allTeamIdsAndOpponentScoresForWeek[teamId]
                    for s in allScores:
                        if score > s:
                            teamsOutscored[teamId] += 1
                        if score == s:
                            teamsTied[teamId] += 1
                    # remove 1 from the teamsTied tracker since we will always find a tie for this team's opponent's score in the list of all scores in the week
                    teamsTied[teamId] -= 1
                    # calculate the AWAL for each team for this week
                    teamIdAndOpponentAWAL[teamId] += (
                            (Deci(teamsOutscored[teamId])
                             * (Deci(1) / Deci(opponentsInWeek)))
                            + (Deci(teamsTied[teamId])
                               * (Deci(0.5) / Deci(opponentsInWeek))))

        return teamIdAndOpponentAWAL

    @classmethod
    @validateYear
    def getOpponentAWALPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team's opponents in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentAWAL = AWALCalculator.getOpponentAWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndOpponentAwalPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentAwalPerGame[teamId] = teamIdAndOpponentAWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentAwalPerGame