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


# zwraca najdluzsze serie na podstawie symbolicznych wynikow
def get_longest_series(team_results):
    if len(team_results) == 0:
        return {
            'win': 0,
            'draw': 0,
            'lost': 0,
        }

    longest_wins = 0
    longest_draws = 0
    longest_loses = 0

    curr_symbol = team_results[0]
    curr_len = 1
    is_first = True

    for symbol in team_results:
        if is_first:
            is_first = False
            continue

        if curr_symbol == symbol:
            curr_len += 1

        else:
            if curr_symbol == 'W' and curr_len > longest_wins:
                longest_wins = curr_len
            if curr_symbol == 'D' and curr_len > longest_draws:
                longest_draws = curr_len
            if curr_symbol == 'L' and curr_len > longest_loses:
                longest_loses = curr_len
            curr_symbol = symbol
            curr_len = 1

    if curr_symbol == 'W' and curr_len > longest_wins:
        longest_wins = curr_len
    if curr_symbol == 'D' and curr_len > longest_draws:
        longest_draws = curr_len
    if curr_symbol == 'L' and curr_len > longest_loses:
        longest_loses = curr_len

    return {
        'win': longest_wins,
        'draw': longest_draws,
        'lost': longest_loses,
    }


# wspolczynnik stabilnosci
def streak_stability_score(team_results):
    matches = len(team_results)
    if matches == 0 or matches == 1:
        return 0

    changes = 0
    curr_element = team_results[0]
    is_first = True
    for el in team_results:
        if is_first:
            is_first = False
            continue

        if el != curr_element:
            changes += 1
            curr_element = el

    return changes / (matches - 1)


# wspolczynnik stabilnosci: points/noPoints
def streak_points_stability_score(team_results):
    matches = len(team_results)
    if matches == 0 or matches == 1:
        return 0

    changes = 0
    curr_element = team_results[0]
    is_first = True
    for el in team_results:
        if is_first:
            is_first = False
            continue

        if (el == 'W' or el == 'D') and curr_element == 'L':
            changes += 1
            curr_element = el
        elif (curr_element == 'W' or curr_element == 'D') and el == 'L':
            changes += 1
            curr_element = el

    return changes / (matches - 1)


# TODO do usuniecia pozniej
if __name__ == '__main__':
    matches_data = load_data("data_csv/ekstraklasa2425")
    legia_symbols = convert_match_results_to_symbols(matches_data, "Legia Warszawa")
    print(legia_symbols)
    print(get_longest_series(legia_symbols))
    print(streak_stability_score(legia_symbols))
    print(streak_points_stability_score(legia_symbols))