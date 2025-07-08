from common_classes import *

# sciezka do pliku z danymi txt
source_path = '../data_txt/ekstraklasa2425.txt'

# sciezka do plikow z danymi csv
dest_matches_path = '../data_csv/matches.csv'
dest_goals_path = '../data_csv/goals.csv'

# kontrola poprawnosci odczytu strzelcow bramek
goalsCounter = 0
goalsSaved = 0

# przydzielenie id meczu
matchID = 1

def getAmountOfTeams(file):
    offset = file.tell()
    amountOfTeams = 0

    line = ""
    s1 = []
    while True:
        line = file.readline()
        if line == "\n":
            break

        s1 = line.split('\t')
        if len(s1) != 4:
            continue
        else:
            amountOfTeams += 2

    file.seek(offset)
    return amountOfTeams

def transformScorers(scorers):
    global matchID
    scorers = scorers.split(',')
    scorers = [s.strip() for s in scorers]

    result = []

    for goal in scorers:
        goals = goal.split(' ')

        size = len(goals)
        curr_scorer = ""
        resetScorer = False

        for i in range(0, size):
            try:


                min = int(goals[i])
                new_goal = GoalInfo()
                new_goal.matchID = matchID - 1
                new_goal.Minute = min
                new_goal.Scorer = curr_scorer
                # print(min)
                # print(curr_scorer)

                if (i + 1) != size and goals[i + 1] == "(k)":
                    new_goal.isPenalty = True
                    # print("karny")
                if (i + 1) != size and goals[i + 1] == "(s)":
                    new_goal.isOwnGoal = True
                    # print("samo")


                result.append(new_goal)

                resetScorer = True
            except:
                if resetScorer:
                    curr_scorer = ""
                    resetScorer = False

                if goals[i] != "(k)" and goals[i] != "(s)":
                    if curr_scorer != "":
                        curr_scorer += " "
                    curr_scorer += goals[i]


    # uzupelnienie strzelcow
    index = -1
    for el in result:
        index += 1
        if el.Scorer == "":
            el.Scorer = result[index-1].Scorer


    return result


def readMatch():
    global matchID
    line = ""
    s1 = []


    while True:
        line = file.readline()
        if line == "":
            return None

        s1 = line.split('\t')
        if len(s1) != 4:
            continue
        else:
            break

    s2 = s1[1].split('-')

    s3 = s1[3].split(',')

    s4 = s3[1].split('(')

    s5 = s4[0].split(' ')

    s6 = s4[1].split(')')

    # print(s1)
    # print(s2)
    # print(s3)
    # print(s4)
    # print(s5)
    # print(s6)
    m1 = MatchInfo()
    m1.matchID = matchID
    matchID += 1
    m1.Host = s1[0]
    m1.Guest = s1[2]

    m1.HostGoals = int(s2[0])
    m1.GuestGoals = int(s2[1])

    m1.Date = s3[0]

    m1.Hour = s5[1]

    m1.Attendance = int(s6[0].replace(" ", ""))

    # strzelcy
    if m1.HostGoals > 0 or m1.GuestGoals > 0:
        line = file.readline()

        if m1.HostGoals == 0:
            cleaned = line.strip()
            m1.GuestScorers = transformScorers(cleaned)
            for el in m1.GuestScorers:
                el.isHostTeamGoal = False
        elif m1.GuestGoals == 0:
            cleaned = line.strip()
            m1.HostScorers = transformScorers(cleaned)
            for el in m1.HostScorers:
                el.isHostTeamGoal = True
        else:
            s1 = line.split(' - ')
            cleaned = [s.strip() for s in s1]
            m1.HostScorers = transformScorers(cleaned[0])
            m1.GuestScorers = transformScorers(cleaned[1])

            for el in m1.HostScorers:
                el.isHostTeamGoal = True
            for el in m1.GuestScorers:
                el.isHostTeamGoal = False

    return m1


if __name__ == '__main__':

    with open(source_path, 'r', encoding="utf-8") as file:

        file_matches = open(dest_matches_path, "w", encoding="utf-8")
        file_goals = open(dest_goals_path, "w", encoding="utf-8")

        # file header
        file_matches.write("MatchId;Round;Host;Guest;Date;Hour;Attendance;HostGoals;GuestGoals" + '\n')
        file_goals.write("MatchId;Scorer;Minute;isPenalty;isOwnGoal;isHostTeamGoal" + '\n')

        # header
        line = file.readline()
        s0 = line.split(',')
        s0 = [s.strip() for s in s0]

        file.readline()
        file.readline()
        file.readline()

        season = SeasonInfo(s0[1], s0[0], getAmountOfTeams(file))

        curr_round = 1
        match_in_round = 1

        while True:
            m1 = readMatch()
            if m1 is None:
                break
            m1.Round = curr_round
            # m1.displayInfo()

            match_in_round += 1
            if match_in_round > 9:
                curr_round += 1
                match_in_round = 1

            # zapis meczu do pliku
            # file_matches.write("MatchId;Round;Host;Guest;Date;Hour;Attendance;HostGoals;GuestGoals" + '\n')
            file_matches.write(str(m1.matchID) + ";")
            file_matches.write(str(m1.Round) + ";")
            file_matches.write(str(m1.Host) + ";")
            file_matches.write(str(m1.Guest) + ";")
            file_matches.write(str(m1.Date) + ";")
            file_matches.write(str(m1.Hour) + ";")
            file_matches.write(str(m1.Attendance) + ";")
            file_matches.write(str(m1.HostGoals) + ";")
            file_matches.write(str(m1.GuestGoals) + "\n")

            goalsCounter += m1.GuestGoals + m1.HostGoals

            # zapis goli gospodarzy
            for hg in m1.HostScorers:
                file_goals.write(str(hg.matchID) + ";")
                file_goals.write(hg.Scorer + ";")
                file_goals.write(str(hg.Minute) + ";")
                file_goals.write(str(hg.isPenalty) + ";")
                file_goals.write(str(hg.isOwnGoal) + ";")
                file_goals.write(str(hg.isHostTeamGoal) + "\n")
                goalsSaved += 1

            # zapis goli gospodarzy
            for gg in m1.GuestScorers:
                file_goals.write(str(gg.matchID) + ";")
                file_goals.write(gg.Scorer + ";")
                file_goals.write(str(gg.Minute) + ";")
                file_goals.write(str(gg.isPenalty) + ";")
                file_goals.write(str(gg.isOwnGoal) + ";")
                file_goals.write(str(gg.isHostTeamGoal) + "\n")
                goalsSaved += 1

        file_matches.close()
        file_goals.close()


    control_all = True

    print("Kontrola poprawnosci zapisanych bramek:")
    print("Bramki w sezonie: " + str(goalsCounter))
    print("Bramki zapisane: " + str(goalsSaved))
    control = (goalsCounter == goalsSaved)
    if control is False:
        control_all = False
    print("Result: " + str(control) + "\n")

    print("Kontrola ilości spotkań:")
    print("Liczba drużyn: " + str(season.amountOfTeams))
    print("Ilość spotkań: " + str(matchID - 1))
    control = ( season.rounds * (season.amountOfTeams / 2) == (matchID - 1))
    if control is False:
        control_all = False
    print("Result: " + str(control) + "\n")

    print("Rezultat kontroli poprawnosci: " + str(control_all))
