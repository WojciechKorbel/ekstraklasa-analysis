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






# TODO póżniej do usunięcia
if __name__ == '__main__':
    matches_data = load_data("data_csv/ekstraklasa2425")
    # pd.set_option('display.max_columns', None)
    # print(matches_data)
    print("ilość spotkań:", get_num_of_matches(matches_data))
    print("ilość drużyn: ", get_num_of_teams(matches_data))



