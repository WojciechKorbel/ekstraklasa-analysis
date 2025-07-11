import pandas as pd

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


# tworzenie tabeli
def create_table(matches, fromRound = -1, toRound = -1):
    if fromRound == -1 and toRound == -1:
        fromRound = 1
        toRound = get_num_of_rounds(matches)
    elif fromRound > toRound:
        return None

    result = {}

    # [0,1,2,3,4,5,6] - mecze, punkty, zwycięstwa, remisy, porażki, bramki zdobyte, bramki stracone
    # TODO zamiana na slownik
    for row in matches.itertuples():
        if row.Round < fromRound or row.Round > toRound:
            continue

        host = row.Host
        guest = row.Guest
        host_goals = row.HostGoals
        guest_goals = row.GuestGoals
        host_points, guest_points = calculate_points_for_match(host_goals, guest_goals)

        curr_balance = [0, 0, 0, 0, 0, 0, 0]
        if host in result.keys():
            curr_balance = result.get(host)

        curr_balance[0] += 1
        curr_balance[1] += host_points
        if host_points == 3:
            curr_balance[2] += 1
        elif host_points == 1:
            curr_balance[3] += 1
        else:
            curr_balance[4] += 1
        curr_balance[5] += host_goals
        curr_balance[6] += guest_goals

        result[host] = curr_balance

        curr_balance = [0, 0, 0, 0, 0, 0, 0]
        if guest in result.keys():
            curr_balance = result.get(guest)

        curr_balance[0] += 1
        curr_balance[1] += guest_points
        if guest_points == 3:
            curr_balance[2] += 1
        elif guest_points == 1:
            curr_balance[3] += 1
        else:
            curr_balance[4] += 1
        curr_balance[5] += guest_goals
        curr_balance[6] += host_goals

        result[guest] = curr_balance

    # TODO uwzglednienie drużyn z tą samą ilością punktów (mecze bezpośrednie)
    return dict(sorted(result.items(), key=lambda x: x[1][1], reverse=True)) # sortowanie po punktach


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
            print(f"{stats[0]:<4}", end='')
        if points:
            print(f"{stats[1]:<5}", end='')
        if wins:
            print(f"{stats[2]:<4}", end='')
        if draws:
            print(f"{stats[3]:<4}", end='')
        if loses:
            print(f"{stats[4]:<4}", end='')
        if goal_balance:
            print(f"{stats[5]}:{stats[6]:<7}", end='')

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
    table = create_table(matches_data)
    print("Tabela na koniec sezonu:")
    display_table(table)

