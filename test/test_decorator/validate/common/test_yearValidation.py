import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestYearValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_twoChampionshipWeeksInYear_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has more than 1 championship week.", str(context.exception))

    def test_validateLeague_yearHasNoWeeks_raisesException(self):
        year = Year(yearNumber=2000, teams=list(), weeks=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_validateLeague_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week1duplicate = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_validateLeague_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_validateLeague_weekNumbersNotOneThroughN_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week4 = Week(weekNumber=4, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4])  # no week 3

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4, week3])  # weeks not in order
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

    def test_validateLeague_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-playoff week after a playoff week.", str(context.exception))

    def test_validateLeague_nonChampionshipWeekAfterChampionshipWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-championship week after a championship week.", str(context.exception))

    def test_validateLeague_yearHasLessThanTwoTeams_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        year = Year(yearNumber=2000, teams=[team1], weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 needs at least 2 teams.", str(context.exception))

    def test_validateLeague_yearNumberIsntInValidRange_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")
        year = Year(yearNumber=1919, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 1919 is not in range 1920-2XXX.", str(context.exception))

        year = Year(yearNumber=3000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 3000 is not in range 1920-2XXX.", str(context.exception))

    def test_validateLeague_teamsHaveDuplicateOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="1", name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has teams with the same owner IDs.", str(context.exception))

    def test_validateLeague_teamsInAYearHaveDuplicateNames_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="1")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 has teams with duplicate names.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_validateLeague_yearNumberIsntTypeInt_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=None, teams=list(), weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year number must be type 'int'.", str(context.exception))

    def test_validateLeague_yearTeamsIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=None, weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year teams must be type 'list'.", str(context.exception))

    def test_validateLeague_yearWeeksIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=list(), weeks=None)
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year weeks must be type 'list'.", str(context.exception))