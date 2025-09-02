import pandas as pd
from functools import cmp_to_key
# TODO dodanie dokumentacji


# ładowanie danych
def load_data(folder_path):
    matches_data = pd.read_csv(folder_path + "/matches.csv", delimiter=';')
    return matches_data


# ilość spotkań
def get_num_of_matches(matches):
    return matches['MatchId'].count()


# ilość drużyn
def get_num_of_teams(matches):
    return matches[matches['Round'] == 1]['MatchId'].count() * 2


# ilość kolejek
def get_num_of_rounds(matches):
    return (get_num_of_teams(matches) - 1) * 2


# ilość bramek w sezonie
def get_num_of_goals(matches):
    return matches['HostGoals'].sum() + matches['GuestGoals'].sum()


# srednia bramek na mecz
def calculate_avg_goals_per_match(matches):
    num_of_matches = get_num_of_matches(matches)
    if num_of_matches == 0:
        return None
    num_of_goals = get_num_of_goals(matches)
    return num_of_goals / num_of_matches


# srednia strzelonych bramek na mecz dla druzyny / druzyn
def calculate_avg_scored_goals_per_match_for_teams(matches, teams):
    result = {}
    num_of_teams = get_num_of_teams(matches)
    if num_of_teams == 0:
        return None

    for team in teams:
        if team in matches['Host'].values or team in matches['Guest'].values:
            goals = 0
            # jako gospodarz
            goals += matches[matches['Host'] == team]['HostGoals'].sum()
            # jako gosc
            goals += matches[matches['Guest'] == team]['GuestGoals'].sum()
            result[team] = goals / ((num_of_teams - 1) * 2)
        else:
            result[team] = None

    return result


# srednia straconych bramek na mecz dla druzyny / druzyn
def calculate_avg_conceded_goals_per_match_for_teams(matches, teams):
    result = {}
    num_of_teams = get_num_of_teams(matches)
    if num_of_teams == 0:
        return None

    for team in teams:
        if team in matches['Host'].values or team in matches['Guest'].values:
            goals = 0
            # jako gospodarz
            goals += matches[matches['Host'] == team]['GuestGoals'].sum()
            # jako gosc
            goals += matches[matches['Guest'] == team]['HostGoals'].sum()
            result[team] = goals / ((num_of_teams - 1) * 2)
        else:
            result[team] = None

    return result


# zlicza wystepowanie danego wyniku
def count_match_results(matches):
    result = {}
    for row in matches.itertuples():
        # print(row.HostGoals, row.GuestGoals)
        goals1 = row.HostGoals
        goals2 = row.GuestGoals
        if goals2 > goals1:
            tmp = goals2
            goals2 = goals1
            goals1 = tmp
        match_result = str(goals1) + ':' + str(goals2)
        if match_result in result.keys():
            result[match_result] += 1
        else:
            result[match_result] = 1

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


# bilans jako gospodarz
def calculate_balance_as_host(matches):
    result = {}
    for row in matches.itertuples():
        host = row.Host
        goals_scored = row.HostGoals
        goals_conceded = row.GuestGoals

        # TODO zamiana na słownik
        curr_balance = []
        if host in result.keys():
            curr_balance = result.get(host)
        else:
            curr_balance = [0, 0, 0]

        if goals_scored > goals_conceded:
            curr_balance[0] += 1
        elif goals_scored == goals_conceded:
            curr_balance[1] += 1
        else:
            curr_balance[2] += 1

        result[host] = curr_balance

    return dict(sorted(result.items(), key=lambda x: x))


# bilans jako gosc
def calculate_balance_as_guest(matches):
    result = {}
    for row in matches.itertuples():
        guest = row.Guest
        goals_scored = row.GuestGoals
        goals_conceded = row.HostGoals

        # TODO zamiana na słownik
        curr_balance = []
        if guest in result.keys():
            curr_balance = result.get(guest)
        else:
            curr_balance = [0, 0, 0]

        if goals_scored > goals_conceded:
            curr_balance[0] += 1
        elif goals_scored == goals_conceded:
            curr_balance[1] += 1
        else:
            curr_balance[2] += 1

        result[guest] = curr_balance

    return dict(sorted(result.items(), key=lambda x: x))


# obliczenie liczby punktow za mecz
def calculate_points_for_match(host_goals, guest_goals):
    if host_goals == guest_goals:
        return 1, 1
    elif host_goals > guest_goals:
        return 3, 0
    else:
        return 0, 3


# klasa reprezentujaca bilans
class Balance:
    def __init__(self, matches=0, points=0, wins=0, draws=0, loses=0, scored=0, conceded=0):
        self.matches = matches
        self.points = points
        self.wins = wins
        self.draws = draws
        self.loses = loses
        self.scored = scored
        self.conceded = conceded

    def update_balance(self, host_goals, guest_goals, host_points, guest_points, is_host_balance):
        self.matches += 1
        if is_host_balance:
            self.points += host_points
            if host_points == 3:
                self.wins += 1
            elif host_points == 1:
                self.draws += 1
            elif host_points == 0:
                self.loses += 1
            self.scored += host_goals
            self.conceded += guest_goals
        else:
            self.points += guest_points
            if guest_points == 3:
                self.wins += 1
            elif guest_points == 1:
                self.draws += 1
            elif guest_points == 0:
                self.loses += 1
            self.scored += guest_goals
            self.conceded += host_goals


# tworzenie nieposortowanej tabeli
def create_unsorted_table(matches, fromRound=-1, toRound=-1):
    result = {}

    for row in matches.itertuples():
        if row.Round < fromRound or row.Round > toRound:
            continue

        host = row.Host
        guest = row.Guest
        host_goals = row.HostGoals
        guest_goals = row.GuestGoals
        host_points, guest_points = calculate_points_for_match(host_goals, guest_goals)

        if host in result.keys():
            curr_balance = result.get(host)
        else:
            curr_balance = Balance()
        curr_balance.update_balance(host_goals, guest_goals, host_points, guest_points, True)
        result[host] = curr_balance

        if guest in result.keys():
            curr_balance = result.get(guest)
        else:
            curr_balance = Balance()

        curr_balance.update_balance(host_goals, guest_goals, host_points, guest_points, False)
        result[guest] = curr_balance

    return result


# tworzenie tabeli
def create_table(matches, fromRound=-1, toRound=-1):
    if fromRound == -1 and toRound == -1:
        fromRound = 1
        toRound = get_num_of_rounds(matches)
    elif fromRound > toRound:
        return None

    unsorted_table = create_unsorted_table(matches, fromRound, toRound)

    return dict(sorted(
        unsorted_table.items(),
        key=cmp_to_key(lambda item1, item2: compare_teams(item1[0], item2[0], matches, unsorted_table, fromRound, toRound))
    ))

def calculate_balance_in_direct_matches(team1, team2, matches, fromRound, toRound):
    team1_balance = Balance()
    team2_balance = Balance()

    for row in matches.itertuples():
        if row.Round < fromRound or row.Round > toRound:
            continue

        host = row.Host
        guest = row.Guest

        if host != team1 and host != team2:
            continue
        if guest != team1 and guest != team2:
            continue

        host_goals = row.HostGoals
        guest_goals = row.GuestGoals
        host_points, guest_points = calculate_points_for_match(host_goals, guest_goals)

        if team1 == host and team2 == guest:
            team1_balance.update_balance(host_goals, guest_goals, host_points, guest_points, True)
            team2_balance.update_balance(host_goals, guest_goals, host_points, guest_points, False)
        elif team1 == guest and team2 == host:
            team1_balance.update_balance(host_goals, guest_goals, host_points, guest_points, False)
            team2_balance.update_balance(host_goals, guest_goals, host_points, guest_points, True)
    return team1_balance, team2_balance

def count_away_wins(team, matches, fromRound, toRound):
    away_wins = 0
    for row in matches.itertuples():
        if row.Round < fromRound or row.Round > toRound:
            continue

        guest = row.Guest

        if guest != team:
            continue

        host_goals = row.HostGoals
        guest_goals = row.GuestGoals
        _, guest_points = calculate_points_for_match(host_goals, guest_goals)

        if guest_points == 3:
            away_wins += 1

    return away_wins

def compare_teams(team1, team2, matches, table, fromRound, toRound):
    # 1. punkty z calego sezonu:
    if table.get(team1).points != table.get(team2).points:
        return table.get(team2).points - table.get(team1).points

    # jeśli cały sezon został rozegrany
    if fromRound == 1 and toRound == get_num_of_rounds(matches):
        team1_balance, team2_balance = calculate_balance_in_direct_matches(team1, team2, matches, fromRound, toRound)

        # 2. punkty zdobyte w meczach bezpośrednich między porównywanymi drużynami
        if team1_balance.points != team2_balance.points:
            return team2_balance.points - team1_balance.points

        # 3. korzystniejsza różnica bramek w meczach bezpośrednich
        delta1 = team1_balance.scored - team1_balance.conceded
        delta2 = team2_balance.scored - team2_balance.conceded

        if delta1 != delta2:
            return delta2 - delta1

    # 4. korzystniejsza różnica bramek w całym sezonie
    delta1 = table.get(team1).scored - table.get(team1).conceded
    delta2 = table.get(team2).scored - table.get(team2).conceded

    if delta1 != delta2:
        return delta2 - delta1

    # 5. więcej zdobytych bramek w całym sezonie
    team1_scored = table.get(team1).scored
    team2_scored = table.get(team2).scored

    if team1_scored != team2_scored:
        return team2_scored - team1_scored

    # 6. więcej wygranych meczów w całym sezonie
    team1_wins = table.get(team1).wins
    team2_wins = table.get(team2).wins

    if team1_wins != team2_wins:
        return team2_wins - team1_wins

    # 7. więcej wygranych meczów wyjazdowych w danym sezonie
    team1_away_wins = count_away_wins(team1, matches, fromRound, toRound)
    team2_away_wins = count_away_wins(team2, matches, fromRound, toRound)

    if team1_away_wins != team2_away_wins:
        return team2_away_wins - team1_away_wins

    # drużyny są rownoważne
    return 0

# wyswietlanie tabeli
def display_table(table, matches=True, points=True, wins=True, draws=True, loses=True, goal_balance=True):
    index = 1
    print(f"{'Lp.':<4} {'Drużyna':<35}", end='')

    if matches:
        print(f"{'M':<4}", end='')
    if points:
        print(f"{'Pkt':<5}", end='')
    if wins:
        print(f"{'W':<4}", end='')
    if draws:
        print(f"{'R':<4}", end='')
    if loses:
        print(f"{'P':<4}", end='')
    if goal_balance:
        print(f"{'Bilans':<7}", end='')

    print()

    for key, stats in table.items():
        print(f"{index:<4} {key:<35}", end='')

        if matches:
            print(f"{stats.matches:<4}", end='')
        if points:
            print(f"{stats.points:<5}", end='')
        if wins:
            print(f"{stats.wins:<4}", end='')
        if draws:
            print(f"{stats.draws:<4}", end='')
        if loses:
            print(f"{stats.loses:<4}", end='')
        if goal_balance:
            print(f"{stats.scored}:{stats.conceded:<7}", end='')

        print()
        index += 1

    print()


# TODO póżniej do usunięcia
if __name__ == '__main__':
    matches_data = load_data("data_csv/ekstraklasa2425")
    # pd.set_option('display.max_columns', None)
    # print(matches_data)
    print("ilość spotkań:", get_num_of_matches(matches_data))
    print("ilość drużyn: ", get_num_of_teams(matches_data))
    print("ilość kolejek: ", get_num_of_rounds(matches_data))
    print("ilość bramek w seoznie: ", get_num_of_goals(matches_data))
    print("średnia bramek na mecz: ", calculate_avg_goals_per_match(matches_data))
    print("średnia strzelonych bramek na mecz:")
    print(
        calculate_avg_scored_goals_per_match_for_teams(matches_data,
                    ['Legia Warszawa', 'Pogoń Szczecin', 'xxx'])
    )
    print("średnia straconych bramek na mecz:")
    print(
        calculate_avg_conceded_goals_per_match_for_teams(matches_data,
                    ['Legia Warszawa', 'Pogoń Szczecin', 'xxx'])
    )
    print("Najczęstsze wyniki:", count_match_results(matches_data))
    print("Bilans jako gospodarz:", calculate_balance_as_host(matches_data))
    print("Bilans jako gość:", calculate_balance_as_guest(matches_data))
    table = create_table(matches_data, fromRound=1, toRound=3)
    print("Tabela po pierszych trzech rundach:")
    display_table(table)
