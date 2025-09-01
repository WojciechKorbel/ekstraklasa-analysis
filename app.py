import tkinter as tk
from tkinter import ttk
import os
import stats

from enum import Enum


class TableType(Enum):
    ALL_SEASON_TABLE = 1
    BY_ROUND_TABLE = 2
    BY_DATE_TABLE = 3


APP_TITLE = "Ekstraklasa analysis"
APP_GEOMETRY = "800x600"

current_season = None
matches_data = None

def get_available_seasons():
    dir_paths = [f.path for f in os.scandir("data_csv") if f.is_dir()]
    seasons = [p.split("\\")[1] for p in dir_paths]
    return seasons

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.frames = {}

        for F in (ChooseSeasonWindow, ChooseStatsWindow, TableAnaliseWindow, SeasonStatsWindow, TeamStatsWindow, SeriesAnaliseWindow):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ChooseSeasonWindow)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def get_frame(self, frame_class):
        return self.frames[frame_class]

class ChooseSeasonWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Wybierz sezon:", font=("Arial", 14))
        label.pack(pady=10)

        button = tk.Button(self, text="Dalej", command=self.go_to_choose_stats)
        button.pack(pady=10)

        self.available_seasons = get_available_seasons()
        self.combobox = ttk.Combobox(self, values=self.available_seasons)
        self.combobox.pack(pady=50)  # put listbox on window

    def go_to_choose_stats(self):
        chosen_season = self.combobox.get()
        if chosen_season in self.available_seasons:
            # zmiana sezonu
            global current_season
            current_season = chosen_season

            # wczytanie sezonu
            global matches_data
            matches_data = stats.load_data("data_csv/" + str(current_season))

            # przelaczenie ekranu
            f = self.controller.get_frame(ChooseStatsWindow)
            f.update_season()
            self.controller.show_frame(ChooseStatsWindow)
        else:
            # TODO komunikat o bledzie
            pass


class ChooseStatsWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # label
        self.labelText = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.labelText, font=("Arial", 14))
        self.label.pack(pady=10)

        # buttons
        table_analise_button = tk.Button(self, text="Analiza tabeli", command=self.go_to_table_analise)
        table_analise_button.pack(pady=10)

        season_stats_button = tk.Button(self, text="Statystyki sezonu", command=self.go_to_season_stats)
        season_stats_button.pack(pady=20)

        team_stats_button = tk.Button(self, text="Statystyki drużyny", command=self.go_to_team_stats)
        team_stats_button.pack(pady=30)

        series_analise_button = tk.Button(self, text="Analiza serii", command=self.go_to_series_analise)
        series_analise_button.pack(pady=40)

        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.pack(pady=50)

    # metody
    def update_season(self):
        self.labelText.set(str(current_season))

    def go_to_table_analise(self):
        self.controller.show_frame(TableAnaliseWindow)

    def go_to_season_stats(self):
        self.controller.show_frame(SeasonStatsWindow)

    def go_to_team_stats(self):
        self.controller.show_frame(TeamStatsWindow)

    def go_to_series_analise(self):
        self.controller.show_frame(SeriesAnaliseWindow)

    def back(self):
        self.controller.show_frame(ChooseSeasonWindow)


class TableAnaliseWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # box1
        self.box1 = tk.Label(self, bg='#fff')
        self.box1.grid(row=0, column=0, sticky=tk.NW, pady=0)

        # box2
        self.box2 = tk.Label(self, bg='#aaa')
        self.box2.grid(row=0, column=1, sticky=tk.NW, pady=0) # na tabele

        # label
        self.label = tk.Label(self.box1, text="Analiza tabeli", font=("Arial", 14))
        self.label.pack(pady=10)

        # radiobuttons
        self.var = tk.IntVar()
        self.R1 = tk.Radiobutton(self.box1, text="Cały sezon", variable=self.var, value=TableType.ALL_SEASON_TABLE.value)
        self.R1.pack(anchor=tk.W)
        self.R2 = tk.Radiobutton(self.box1, text="Według kolejek", variable=self.var, value=TableType.BY_ROUND_TABLE.value)
        self.R2.pack(anchor=tk.W)
        self.R3 = tk.Radiobutton(self.box1, text="Według dat", variable=self.var, value=TableType.BY_DATE_TABLE.value)
        self.R3.pack(anchor=tk.W)
        self.var.set(1) # defaultowo

        # scale
        self.scale_start_var = tk.DoubleVar()
        self.scale = tk.Scale(self.box1, variable=self.scale_start_var, length=120, orient=tk.HORIZONTAL, from_=1, to=34) # TODO liczby nie recznie!!!
        self.scale.pack(anchor=tk.CENTER)

        self.scale_end_var = tk.DoubleVar()
        self.scale1 = tk.Scale(self.box1, variable=self.scale_end_var, length=120, orient=tk.HORIZONTAL, from_=1, to=34)  # TODO liczby nie recznie!!!
        self.scale1.pack(anchor=tk.CENTER)

        # buttons
        generate_button = tk.Button(self.box1, text="Generuj", command=self.generate)
        generate_button.pack(pady=10)

        back_button = tk.Button(self.box1, text="Powrót", command=self.back)
        back_button.pack(pady=20)

        # tabela
        self.table_labels = ["Poz.", "Drużyna", "Mecze", "Punkty", "Wygrane", "Remisy", "Przegrane", "Gole +", "Gole -"]

    # metody
    def generate(self):
        table = {}
        value = int(self.var.get())

        match value:
            case TableType.ALL_SEASON_TABLE.value:
                table = stats.create_table(matches_data)
                print(table)
            case TableType.BY_ROUND_TABLE.value:
                if self.scale_start_var.get() > self.scale_end_var.get():
                    return # TODO komunikat o bledzie
                table = stats.create_table(matches_data, fromRound=self.scale_start_var.get(), toRound=self.scale_end_var.get())
                print(table)
            case TableType.BY_DATE_TABLE.value:
                pass
            case _:
                print("ERROR!")

        self.clean_table()

        # szerokosci pol
        field_widths = [4 if len(self.table_labels[0]) <= 4 else len(self.table_labels[0]),
                        self.get_longest_team_name_len(table) if len(self.table_labels[1]) < self.get_longest_team_name_len(table) else len(self.table_labels[1])]
        for index in range(0,7): # TODO nie recznie
            field_widths.append(5 if len(self.table_labels[index + 2]) <= 5 else len(self.table_labels[index + 2]))
        # longest_team_len = self.get_longest_team_name_len(table)

        # nazwy params
        for index in range(0, len(self.table_labels)):
            title = tk.Label(self.box2, text=self.table_labels[index], bg="#abc", width=field_widths[index])
            title.grid(row=0, column=index, sticky=tk.NW, pady=0)

        # pozycje
        index = 0
        for pos in range(len(table)):
            new_label = tk.Label(self.box2, text=str(index+1) + ".", bg="#cde", width=field_widths[0])
            new_label.grid(row=index + 1, column=0, sticky=tk.NW, pady=0)
            index += 1

        # nazwy druzyn
        index = 0
        for key in table.keys():
            new_label = tk.Label(self.box2, text=key, bg="#cde", width=field_widths[1])
            new_label.grid(row=index+1, column=1, sticky=tk.NW, pady=0)
            index += 1

        # staty
        curr_row = 1
        curr_col = 2
        for key in table.keys():
            vals = table[key]
            curr_col = 2
            for val in range(len(vals)):
                new_label = tk.Label(self.box2, text=str(vals[val]), bg="#cde", width=field_widths[curr_col])
                new_label.grid(row=curr_row, column=curr_col, sticky=tk.NW, pady=0)
                curr_col += 1
            curr_row += 1


    def clean_table(self):
        for widget in self.box2.winfo_children():
            widget.destroy()

    def get_longest_team_name_len(self, table):
        maximum = -1
        for key in table.keys():
            if len(key) > maximum:
                maximum = len(key)
        return maximum

    def back(self):
        # clean
        self.clean_table()

        # przełączenie
        self.controller.show_frame(ChooseStatsWindow)


class SeasonStatsWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # label
        self.label = tk.Label(self, text="Statystyki sezonu", font=("Arial", 14))
        self.label.pack(pady=10)

        # buttons
        back_button = tk.Button(self, text="Powrót", command=self.back)
        back_button.pack(pady=20)

    # metody
    def back(self):
        self.controller.show_frame(ChooseStatsWindow)


class TeamStatsWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # label
        self.label = tk.Label(self, text="Statystyki drużyny", font=("Arial", 14))
        self.label.pack(pady=10)

        # buttons
        back_button = tk.Button(self, text="Powrót", command=self.back)
        back_button.pack(pady=20)

    # metody
    def back(self):
        self.controller.show_frame(ChooseStatsWindow)


class SeriesAnaliseWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # label
        self.label = tk.Label(self, text="Analiza serii", font=("Arial", 14))
        self.label.pack(pady=10)

        # buttons
        back_button = tk.Button(self, text="Powrót", command=self.back)
        back_button.pack(pady=20)

    # metody
    def back(self):
        self.controller.show_frame(ChooseStatsWindow)


if __name__ == "__main__":
    app = App()
    app.mainloop()


