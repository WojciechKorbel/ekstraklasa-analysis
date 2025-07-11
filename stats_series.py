from stats import load_data

# TODO dokumentacja

# dla pojedyńczych drużyn:


# konwersja wynikow na symbole
def convert_match_results_to_symbols(matches, team):
    result = []
    for row in matches.itertuples():
        if team == row.Host:
            if row.HostGoals > row.GuestGoals:
                result.append('W')
            elif row.HostGoals == row.GuestGoals:
                result.append('D')
            else:
                result.append('L')
        elif team == row.Guest:
            if row.HostGoals > row.GuestGoals:
                result.append('L')
            elif row.HostGoals == row.GuestGoals:
                result.append('D')
            else:
                result.append('W')
    return result

# TODO do usuniecia pozniej
if __name__ == '__main__':
    matches_data = load_data("data_csv/ekstraklasa2425")
    print(convert_match_results_to_symbols(matches_data, "Legia Warszawa"))