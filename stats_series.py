import math

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


# konwersja goli na symbole
def convert_goals_to_symbols(matches, team):
    result = []
    for row in matches.itertuples():
        match = {}
        if team == row.Host:
            match['isHost'] = True
            match['teamGoals'] = row.HostGoals
            match['opponentGoals'] = row.GuestGoals
            result.append(match)
        elif team == row.Guest:
            match['isHost'] = False
            match['teamGoals'] = row.GuestGoals
            match['opponentGoals'] = row.HostGoals
            result.append(match)
    return result


# wyświetla gole druzyny:
def display_teams_goals(team_goals):
    for el in team_goals:
        if el['isHost']:
            print(str(el['teamGoals']) + ":" + str(el['opponentGoals']) + ', Host')
        else:
            print(str(el['teamGoals']) + ":" + str(el['opponentGoals']) + ', Guest')


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


# najdluzsza seria bez ... (pomocnicza)
def get_longest_series_without_symbols(team_results, symbols):
    matches = len(team_results)
    if matches == 0 or (matches == 1 and team_results[0] not in symbols):
        return 0
    elif matches == 1:
        return 1

    result = 0
    curr_len = 0
    for el in team_results:
        if el in symbols:
            curr_len += 1
        else:
            if curr_len > result:
                result = curr_len
            curr_len = 0

    if curr_len > result:
        result = curr_len

    return result


# najdłuższa seria bez porażki
def get_longest_not_lose_series(team_results):
    symbols = ['W', 'D']
    return get_longest_series_without_symbols(team_results, symbols)


# najdłuższa seria bez wygranej
def get_longest_not_win_series(team_results):
    symbols = ['L', 'D']
    return get_longest_series_without_symbols(team_results, symbols)


# najdłuższa seria bez remisu
def get_longest_not_draw_series(team_results):
    symbols = ['L', 'W']
    return get_longest_series_without_symbols(team_results, symbols)


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


# najdłuższa seria ze stratą gola
def get_longest_streak_of_losing_a_goal(team_goals):
    matches = len(team_goals)
    if matches == 0:
        return 0
    if matches == 1 and team_goals[0]['opponentGoals'] > 0:
        return 1

    result = 0
    curr_len = 0
    for el in team_goals:
        if el['opponentGoals'] > 0:
            curr_len += 1
        else:
            if curr_len > result:
                result = curr_len
            curr_len = 0

    if curr_len > result:
        result = curr_len
    return result


# najdłuższa seria bez straty gola
def get_longest_streak_without_losing_a_goal(team_goals):
    matches = len(team_goals)
    if matches == 0:
        return 0
    if matches == 1 and team_goals[0]['opponentGoals'] == 0:
        return 1

    result = 0
    curr_len = 0
    for el in team_goals:
        if el['opponentGoals'] == 0:
            curr_len += 1
        else:
            if curr_len > result:
                result = curr_len
            curr_len = 0

    if curr_len > result:
        result = curr_len
    return result


# obie drużyny strzelają - najdłuższa seria
def get_longest_both_teams_to_score_streak(team_goals):
    matches = len(team_goals)
    if matches == 0:
        return 0
    if matches == 1 and team_goals[0]['teamGoals'] > 0 and team_goals[0]['opponentGoals'] > 0:
        return 1
    elif matches == 1:
        return 0

    result = 0
    curr_len = 0
    for el in team_goals:
        if el['teamGoals'] > 0 and el['opponentGoals'] > 0:
            curr_len += 1
        else:
            if curr_len > result:
                result = curr_len
            curr_len = 0

    if curr_len > result:
        result = curr_len
    return result


# występowanie ciągów rezultatów o zadanej długości
def count_sliding_window(team_results, size):
    matches = len(team_results)
    if size <= 0 or size > matches:
        return None
    if matches == 0:
        return 0

    result = {}
    for index in range(0, matches - size + 1):
        curr_window = []
        for el in range(0, size):
            curr_window.append(team_results[index + el])
            # print(team_results[index + el], end=' ')
        # print()
        curr_window = tuple(curr_window)
        # print(curr_window)
        if curr_window in result.keys():
            result[curr_window] += 1
        else:
            result[curr_window] = 1

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


# entropia wyników danej drużyny
def team_entropy(team_results):
    matches = len(team_results)

    pWin = team_results.count('W') / matches
    pDraw = team_results.count('D') / matches
    pLose = team_results.count('L') / matches

    els = []
    if pWin > 0:
        els.append(pWin * math.log2(pWin))
    if pDraw > 0:
        els.append(pDraw * math.log2(pDraw))
    if pLose > 0:
        els.append(pLose * math.log2(pLose))
    return abs(-sum(els))


# najdluzsza seria powyzej x goli
def get_longest_above_n_goals_streak(team_goals, n, count_scored=False, count_conceded=False):
    if not count_scored and not count_conceded:
        return None

    result = 0
    curr_len = 0
    for el in team_goals:
        goals_cnt = 0
        if count_scored:
            goals_cnt += el['teamGoals']
        if count_conceded:
            goals_cnt += el['opponentGoals']

        if goals_cnt > n:
            curr_len += 1
        else:
            if curr_len > result:
                result = curr_len
            curr_len = 0

    if curr_len > result:
        result = curr_len
    return result


# TODO do usuniecia pozniej
if __name__ == '__main__':
    matches_data = load_data("data_csv/ekstraklasa2425")
    legia_symbols = convert_match_results_to_symbols(matches_data, "Legia Warszawa")
    print(legia_symbols)
    print(get_longest_series(legia_symbols))
    print(streak_stability_score(legia_symbols))
    print(streak_points_stability_score(legia_symbols))
    print(get_longest_not_lose_series(legia_symbols))
    print(get_longest_not_win_series(legia_symbols))
    print(get_longest_not_draw_series(legia_symbols))

    legia_goals = convert_goals_to_symbols(matches_data, "Legia Warszawa")
    print(legia_goals)
    display_teams_goals(legia_goals)
    print(get_longest_streak_of_losing_a_goal(legia_goals))
    print(get_longest_streak_without_losing_a_goal(legia_goals))
    print(get_longest_both_teams_to_score_streak(legia_goals))

    print(count_sliding_window(legia_symbols, 3))

    print(team_entropy(legia_symbols)) # najbardziej nieprzewidywalne wyniki: maksymalna entropia: log2(3) = 1,585

    print(get_longest_above_n_goals_streak(legia_goals, 1.5, count_scored=True, count_conceded=False))