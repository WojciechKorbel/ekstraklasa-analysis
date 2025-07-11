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


