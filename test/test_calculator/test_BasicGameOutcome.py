import unittest

from src.leeger.calculator.BasicGameOutcome import BasicGameOutcome
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestBasicGameOutcome(unittest.TestCase):
    def test_getWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = BasicGameOutcome.getWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWins(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = BasicGameOutcome.getWins(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getLosses_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = BasicGameOutcome.getLosses(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getLosses(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getLosses(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getLosses(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getLosses_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getLosses(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = BasicGameOutcome.getLosses(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getTies_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = BasicGameOutcome.getTies(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getTies_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getTies(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getTies(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getTies(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getTies(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = BasicGameOutcome.getTies(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWinPercentage_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = BasicGameOutcome.getWinPercentage(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.375"), response[teams[0].id])
        self.assertEqual(Deci("0.625"), response[teams[1].id])

    def test_getWinPercentage_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWinPercentage(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWinPercentage_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWinPercentage(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.0"), response[teams[0].id])
        self.assertEqual(Deci("1.0"), response[teams[1].id])

    def test_getWinPercentage_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWinPercentage(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWinPercentage_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = BasicGameOutcome.getWinPercentage(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.0"), response[teams[0].id])
        self.assertEqual(Deci("1.0"), response[teams[1].id])

    def test_getWinPercentage_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = BasicGameOutcome.getWinPercentage(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
