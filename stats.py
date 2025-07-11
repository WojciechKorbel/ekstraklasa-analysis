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




