class SeasonInfo:
    def __init__(self, league, season1, amount_of_teams):
        self.league = league
        self.season = season1
        self.amountOfTeams = amount_of_teams
        self.rounds = (amount_of_teams - 1) * 2

    def displayInfo(self):
        print(f"🏆  Liga: {self.league}")
        print(f"📅  {self.season}")
        print(f"👥  Liczba drużyn: {self.amountOfTeams}")

class GoalInfo:
    def __init__(self):
        self.Scorer = "noName"
        self.Minute = 1
        self.isPenalty = False
        self.isOwnGoal = False
        self.matchID = -1
        self.isHostTeamGoal = False

    def displayInfo(self):
        print(
            f"⚽ Strzelec: {self.Scorer} | "
            f"⏱️ Minuta: {self.Minute} | "
            f"🎯 Karny: {self.isPenalty} | "
            f"❌️ Samobój: {self.isOwnGoal}"
        )
class MatchInfo:
    def __init__(self):
        self.matchID = -1
        self.Round = 1
        self.Host = "team1"
        self.Guest = "team2"
        self.Date = "01.01.2000"
        self.Hour = "00:00"
        self.Attendance = 0
        self.HostGoals = 0
        self.GuestGoals = 0
        self.HostScorers = []
        self.GuestScorers = []

    def displayInfo(self):
        print(f"🕹️  ID {self.matchID}")
        print(f"🕹️  Kolejka {self.Round}")
        print(f"📅 Data: {self.Date} {self.Hour}")
        print(f"🏟️  Frekwencja: {self.Attendance}")
        print(f"⚽ Mecz: {self.Host} {self.HostGoals} : {self.GuestGoals} {self.Guest}")

        print(f"🎯 Strzelcy {self.Host}: ", end="")
        for s in self.HostScorers:
            s.displayInfo()
        print(f"🎯 Strzelcy {self.Guest}: ", end="")
        for s in self.GuestScorers:
            s.displayInfo()
