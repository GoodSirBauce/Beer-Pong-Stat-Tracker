import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_operations import (create_connection, create_tables, get_all_players, get_all_teams, get_all_rule_sets, create_rules_table, refresh_player_list, refresh_team_list,
                           add_player, delete_player, edit_player, add_team, delete_team, edit_team, add_player_to_team, remove_player_from_team, get_player_ids_for_team, get_team_ids_for_player)
from stats import (create_players_listbox, create_teams_listbox, show_listbox, display_stats, get_stats)

def show_delete_warning():
    return messagebox.askyesno("Delete Warning", "Are you sure you want to delete this player or team? This action cannot be undone.")

def assign_player_to_team(player_id, team_id, conn, players_listbox, refresh_player_list):
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET team_id = ? WHERE id = ?", (team_id, player_id))
    conn.commit()
    db_operations.add_player_to_team(player_id, team_id, conn)
    refresh_player_list(players_listbox, conn)

def edit_player_window(player_id, current_name, conn, parent_window, refresh_player_list, players_listbox):
    window = tk.Toplevel()
    window.title("Edit Player")

    edit_player_label = tk.Label(window, text="Edit Player:")
    edit_player_label.grid(row=0, column=0, padx=10, pady=10)

    edit_player_entry = tk.Entry(window)
    edit_player_entry.grid(row=0, column=1, padx=10, pady=10)
    edit_player_entry.insert(0, current_name)

    edit_player_btn = tk.Button(window, text="Save", command=lambda: [edit_player(player_id, edit_player_entry.get(), conn), refresh_player_list(players_listbox, conn), window.destroy()])
    edit_player_btn.grid(row=0, column=2, padx=10, pady=10)

def edit_team_window(team_id, current_name, conn, parent_window, refresh_team_list, teams_listbox):
    window = tk.Toplevel()
    window.title("Edit Team")

    edit_team_label = tk.Label(window, text="Edit Team:")
    edit_team_label.grid(row=0, column=0, padx=10, pady=10)

    edit_team_entry = tk.Entry(window)
    edit_team_entry.grid(row=0, column=1, padx=10, pady=10)
    edit_team_entry.insert(0, current_name)

    edit_team_btn = tk.Button(window, text="Save", command=lambda: [edit_team(team_id, edit_team_entry.get(), conn), refresh_team_list(teams_listbox, conn), window.destroy()])
    edit_team_btn.grid(row=0, column=2, padx=10, pady=10)
    
def edit_players_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Edit Players")
    conn = create_connection()
    
    players_listbox = tk.Listbox(window)
    players_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    refresh_player_list(players_listbox, conn)
    
    add_player_label = tk.Label(window, text="Add Player:")
    add_player_label.grid(row=0, column=0, padx=10, pady=10)

    add_player_entry = tk.Entry(window)
    add_player_entry.grid(row=0, column=1, padx=10, pady=10)

    add_player_btn = tk.Button(window, text="Add Player", command=lambda: [add_player(add_player_entry.get(), conn), refresh_player_list(players_listbox, conn)])
    add_player_btn.grid(row=0, column=2, padx=10, pady=10)

    delete_player_btn = tk.Button(window, text="Delete", command=lambda: [delete_player(players_listbox.get(tk.ANCHOR).split('.')[0], conn), refresh_player_list(players_listbox, conn)] if show_delete_warning() else None)
    delete_player_btn.grid(row=2, column=0, padx=10, pady=10)

    edit_player_btn = tk.Button(window, text="Edit", command=lambda: edit_player_window(players_listbox.get(tk.ANCHOR).split('.')[0], add_player_entry.get(), conn, window, refresh_player_list, players_listbox))
    edit_player_btn.grid(row=2, column=1, padx=10, pady=10)
    
    # Add widgets for selecting a team and assigning the selected player to the team
    teams = get_all_teams(conn)
    team_var = tk.StringVar(window)
    if teams:
        team_var.set(teams[0][1])  # Set the default value to the name of the first team in the list
    else:
        team_var.set("No teams available")
    
    assign_team_label = tk.Label(window, text="Assign Team:")
    assign_team_label.grid(row=3, column=0, padx=10, pady=10)

    assign_team_dropdown = tk.OptionMenu(window, team_var, *[team[1] for team in teams])
    assign_team_dropdown.grid(row=3, column=1, padx=10, pady=10)

    assign_team_btn = tk.Button(window, text="Assign Team", command=lambda: add_player_to_team(players_listbox.get(tk.ANCHOR).split('.')[0], [team[0] for team in teams if team[1] == team_var.get()][0], conn) if teams else None)
    assign_team_btn.grid(row=3, column=2, padx=10, pady=10)
    
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))

# Populate team_members_listbox with team members
def update_team_members_checkbuttons(team_id, conn, team_members_frame):
    for widget in team_members_frame.winfo_children():
        widget.destroy()

    player_ids = get_player_ids_for_team(team_id, conn)
    team_members_frame.player_vars = {}

    for player_id in player_ids:
        player = [player for player in get_all_players(conn) if player[0] == player_id][0]
        player_var = tk.IntVar()
        player_checkbutton = ttk.Checkbutton(team_members_frame, text=f"{player[0]}. {player[1]}", variable=player_var)
        player_checkbutton.pack(anchor=tk.W)
        team_members_frame.player_vars[player_id] = player_var

def update_team_members_listbox(team_id, conn, team_members_listbox):
    team_members_listbox.delete(0, tk.END)
    player_ids = get_player_ids_for_team(team_id, conn)
    
    for player_id in player_ids:
        player = [player for player in get_all_players(conn) if player[0] == player_id][0]
        member_name = f"{player[0]}. {player[1]} {player[2]}"
        team_members_listbox.insert(tk.END, member_name)

def edit_teams_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Edit Teams")
    conn = create_connection()
    
    teams_listbox = tk.Listbox(window)
    teams_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    refresh_team_list(teams_listbox, conn)
    
    # Add widgets for creating, modifying, and deleting teams here
    add_team_label = tk.Label(window, text="Add Team:")
    add_team_label.grid(row=0, column=0, padx=10, pady=10)

    add_team_entry = tk.Entry(window)
    add_team_entry.grid(row=0, column=1, padx=10, pady=10)
    
    add_team_btn = tk.Button(window, text="Add Team", command=lambda: [add_team(add_team_entry.get(), conn), refresh_team_list(teams_listbox, conn)])
    add_team_btn.grid(row=0, column=2, padx=10, pady=10)

    delete_team_btn = tk.Button(window, text="Delete", command=lambda: [delete_team(teams_listbox.get(tk.ANCHOR).split('.')[0], conn), refresh_team_list(teams_listbox, conn)] if show_delete_warning() else None)
    delete_team_btn.grid(row=2, column=0, padx=10, pady=10)

    edit_team_btn = tk.Button(window, text="Edit", command=lambda: edit_team_window(teams_listbox.get(tk.ANCHOR).split('.')[0], add_team_entry.get(), conn, window, refresh_team_list, teams_listbox))
    edit_team_btn.grid(row=2, column=1, padx=10, pady=10)
    
    # Team members Listbox
    team_members_listbox = tk.Listbox(window)
    team_members_listbox.grid(row=3, column=0, pady=(10, 0), padx=(10, 0))
    
    # Replace 'team_id' with 'current_team_id' which is a list containing a single element
    current_team_id = [None]
    
    # Add the following lines after creating team_members_listbox
    def on_team_selected(event):
        if not teams_listbox.curselection():
            return

        selected_item = teams_listbox.get(tk.ANCHOR)
        team_id = int(selected_item.split('.')[0])
        current_team_id[0] = team_id
        update_team_members_listbox(team_id, conn, team_members_listbox)

    teams_listbox.bind('<<ListboxSelect>>', on_team_selected)

    remove_player_btn = tk.Button(window, text="Remove Player", command=lambda: [remove_player_from_team(team_members_listbox.get(tk.ANCHOR).split('.')[0], current_team_id[0], conn), on_team_selected(None)])
    remove_player_btn.grid(row=5, column=0, pady=(10, 0))
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))

def start_new_game_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Start New Game")
    conn = create_connection()
    
    def update_listboxes(game_mode):
        if game_mode == "1v1":
            selected_team1_players_frame.grid_remove()
            selected_team2_players_frame.grid_remove()
            refresh_player_list(team1_listbox, conn)
            refresh_player_list(team2_listbox, conn)
        elif game_mode == "2v2":
            selected_team1_players_frame.grid()
            selected_team2_players_frame.grid()
            refresh_team_list(team1_listbox, conn)
            refresh_team_list(team2_listbox, conn)
    
    # Add radio buttons for game type selection (1v1 or 2v2)
    game_mode_var = tk.StringVar()
    game_mode_var.set("2v2")

    game_mode_label = tk.Label(window, text="Game Mode:")
    game_mode_label.grid(row=0, column=3, padx=10, pady=10)

    game_mode_1v1 = tk.Radiobutton(window, text="1v1", variable=game_mode_var, value="1v1", command=lambda: update_listboxes(game_mode_var.get()))
    game_mode_1v1.grid(row=1, column=3, padx=10, pady=10)

    game_mode_2v2 = tk.Radiobutton(window, text="2v2", variable=game_mode_var, value="2v2", command=lambda: update_listboxes(game_mode_var.get()))
    game_mode_2v2.grid(row=2, column=3, padx=10, pady=10)


    # Add a dropdown menu (combobox) to select a rule set
    rule_sets = get_all_rule_sets(conn)
    rule_set_names = [rule_set[1] for rule_set in rule_sets]

    rule_set_label = tk.Label(window, text="Rule Set:")
    rule_set_label.grid(row=3, column=3, padx=10, pady=10)

    rule_set_var = tk.StringVar()
    rule_set_combobox = ttk.Combobox(window, textvariable=rule_set_var, values=rule_set_names, state="readonly")
    rule_set_combobox.grid(row=4, column=3, padx=10, pady=(0, 10))

    if rule_set_names:
        rule_set_combobox.current(0)

    # Add widgets to select teams and list their members

    # Team 1
    team1_label = tk.Label(window, text="Team 1")
    team1_label.grid(row=0, column=0, padx=10, pady=10)

    team1_listbox = tk.Listbox(window)
    team1_listbox.grid(row=1, column=0, padx=10, pady=10)

    # Team 2
    team2_label = tk.Label(window, text="Team 2")
    team2_label.grid(row=0, column=1, padx=10, pady=10)

    team2_listbox = tk.Listbox(window)
    team2_listbox.grid(row=1, column=1, padx=10, pady=10)

    # Selected Players Frames
    selected_team1_players_frame = tk.Frame(window)
    selected_team1_players_frame.grid(row=3, column=0, padx=10, pady=10)
    selected_team1_players_frame.player_vars = {}
    
    selected_team2_players_frame = tk.Frame(window)
    selected_team2_players_frame.grid(row=3, column=1, padx=10, pady=10)
    selected_team2_players_frame.player_vars = {}
    
    selected_team1 = tk.StringVar()
    selected_team2 = tk.StringVar()

    # Add a function to update the list of team members when a team is selected
    def on_team_selected(team_listbox, team_members_frame, selected_var):
        selected_item = team_listbox.get(tk.ANCHOR)
        selected_var.set(selected_item)
        team_id = int(selected_item.split('.')[0])
        update_team_members_checkbuttons(team_id, conn, team_members_frame)

    # Bind the ListboxSelect event to the on_team_selected function for both team listboxes
    team1_listbox.bind('<<ListboxSelect>>', lambda event: on_team_selected(team1_listbox, selected_team1_players_frame, selected_team1))
    team2_listbox.bind('<<ListboxSelect>>', lambda event: on_team_selected(team2_listbox, selected_team2_players_frame, selected_team2))

    # Refresh the team listboxes with the available teams
    refresh_team_list(team1_listbox, conn)
    refresh_team_list(team2_listbox, conn)

    # Function to update checkbuttons with team members
    def update_team_members_checkbuttons(team_id, conn, team_members_frame):
        for widget in team_members_frame.winfo_children():
            widget.destroy()

        player_ids = get_player_ids_for_team(team_id, conn)
        for player_id in player_ids:
            player = [player for player in get_all_players(conn) if player[0] == player_id][0]
            var = tk.BooleanVar()
            player_checkbutton = ttk.Checkbutton(team_members_frame, text=f"{player[0]}. {player[1]}", variable=var)
            player_checkbutton.pack(anchor=tk.W)
            team_members_frame.player_vars[player_id] = var

    def validate_selections():
        game_mode = game_mode_var.get()

        if game_mode == "1v1":
            if selected_team1.get() and selected_team2.get():
                player1_id = int(selected_team1.get().split('.')[0])
                player2_id = int(selected_team2.get().split('.')[0])

                if player1_id == player2_id:
                   return False, "You must select two different players for a 1v1 game."
            else:
                return False, "Please select a player for each side in a 1v1 game."

        elif game_mode == "2v2":
            if selected_team1.get() and selected_team2.get():
                team1_id = int(selected_team1.get().split('.')[0])
                team2_id = int(selected_team2.get().split('.')[0])

                if team1_id == team2_id:
                    return False, "You must select two different teams for a 2v2 game."

                selected_team1_player_count = sum([v.get() for v in selected_team1_players_frame.player_vars.values()])
                selected_team2_player_count = sum([v.get() for v in selected_team2_players_frame.player_vars.values()])

                if selected_team1_player_count != 2 or selected_team2_player_count != 2:
                    return False, "Please select exactly two players for each team in a 2v2 game."
            else:
                return False, "Please select a team for each side in a 2v2 game."

        if not rule_set_var.get():
            return False, "Please select a rule set before starting the game."

        return True, ""


    # Add a "Start Game" button
    def start_new_game():
        is_valid, error_message = validate_selections()
        if not is_valid:
            messagebox.showwarning("Invalid Selections", error_message)
        else:
            show_confirmation_window()
            
    def show_confirmation_window():
        game_mode = game_mode_var.get()
        rule_set_name = rule_set_var.get()

        if game_mode == "1v1":
            player1_id = int(team1_listbox.get(tk.ANCHOR).split('.')[0])
            player2_id = int(team2_listbox.get(tk.ANCHOR).split('.')[0])
            message = f"Starting a new 1v1 game with Player {player1_id} and Player {player2_id}"
        elif game_mode == "2v2":
            team1_id = int(team1_listbox.get(tk.ANCHOR).split('.')[0])
            team2_id = int(team2_listbox.get(tk.ANCHOR).split('.')[0])
            message = f"Starting a new 2v2 game with Team {team1_id} and Team {team2_id}"

        message += f"\nRule Set: {rule_set_name}"

        def confirm():
            print(message)
            # Initialize the game with the selected players/teams
            # Add any additional logic and database interactions needed to start the game here
            confirmation_window.destroy()
            window.destroy()
            button.config(state=tk.NORMAL)

        confirmation_window = tk.Toplevel()
        confirmation_window.title("Confirm Game Settings")

        message_label = tk.Label(confirmation_window, text=message)
        message_label.pack(padx=10, pady=10)

        confirm_button = tk.Button(confirmation_window, text="Confirm", command=confirm)
        confirm_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = tk.Button(confirmation_window, text="Cancel", command=confirmation_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    start_game_btn = tk.Button(window, text="Start Game", command=start_new_game)
    start_game_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))

def stats_window(button):
    button.config(state=tk.DISABLED)
    stats_window = tk.Toplevel()
    stats_window.title("Stats")
    
    players_button = tk.Button(stats_window, text="Players", command=lambda: show_listbox(stats_window, "player"))
    players_button.grid(row=0, column=0, padx=10, pady=10)

    teams_button = tk.Button(stats_window, text="Teams", command=lambda: show_listbox(stats_window, "team"))
    teams_button.grid(row=0, column=1, padx=10, pady=10)

    close_button = tk.Button(stats_window, text="Close", command=lambda: close_window(stats_window, button))
    close_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    stats_window.protocol("WM_DELETE_WINDOW", lambda: close_window(stats_window, button))
    
    # Configure rows
    stats_window.grid_rowconfigure(2, weight=1)

    show_listbox(stats_window, "player")  # Show the "Players" listbox initially
    
def rules_editor_window(button):
    button.config(state=tk.DISABLED)
    rules_window = tk.Toplevel()
    rules_window.title("Rules Editor")

    # Rule name
    rule_name_label = tk.Label(rules_window, text="Rule name:")
    rule_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    rule_name_entry = tk.Entry(rules_window)
    rule_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    # Number of cups
    cups_label = tk.Label(rules_window, text="Number of cups:")
    cups_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    cups_var = tk.StringVar(rules_window)
    cups_var.set("10")
    cups_options = ["10", "6"]
    cups_dropdown = tk.OptionMenu(rules_window, cups_var, *cups_options)
    cups_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    # Multi-cup rule
    multi_cup_var = tk.BooleanVar(rules_window)
    multi_cup_check = tk.Checkbutton(rules_window, text="Multi-cup rule", variable=multi_cup_var)
    multi_cup_check.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    # Same cup rule
    same_cup_var = tk.BooleanVar(rules_window)
    same_cup_check = tk.Checkbutton(rules_window, text="Same cup rule", variable=same_cup_var)
    same_cup_check.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    # Island rule
    island_var = tk.BooleanVar(rules_window)
    island_check = tk.Checkbutton(rules_window, text="Island rule", variable=island_var)
    island_check.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    # Limit of island attempts
    island_limit_label = tk.Label(rules_window, text="Limit of island attempts:")
    island_limit_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    island_limit_var = tk.StringVar(rules_window)
    island_limit_var.set("No limit")
    island_limit_options = ["No limit", "1", "2", "3"]
    island_limit_dropdown = tk.OptionMenu(rules_window, island_limit_var, *island_limit_options)
    island_limit_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

    # Balls back rule
    balls_back_var = tk.BooleanVar(rules_window)
    balls_back_check = tk.Checkbutton(rules_window, text="Balls back rule", variable=balls_back_var)
    balls_back_check.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

    # Consecutive balls back in the same round
    consecutive_balls_back_var = tk.BooleanVar(rules_window)
    consecutive_balls_back_check = tk.Checkbutton(rules_window, text="Consecutive balls back in the same round", variable=consecutive_balls_back_var)
    consecutive_balls_back_check.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

    # Save and close buttons
    save_button = tk.Button(rules_window, text="Save", command=lambda: save_rules(rules_window, rule_name_entry, cups_var, multi_cup_var, same_cup_var, island_var, island_limit_var, balls_back_var, consecutive_balls_back_var, button))
    save_button.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

    close_button = tk.Button(rules_window, text="Close", command=lambda: close_window(rules_window, button))
    close_button.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)
    
    rules_window.protocol("WM_DELETE_WINDOW", lambda: close_window(rules_window, button))

def save_rules(rules_window, rule_name, cups_var, multi_cup_var, same_cup_var, island_var, island_limit_var, balls_back_var, consecutive_balls_back_var, button):
    
    # Retrieve the values from the input fields
    rule_name = rule_name.get()
    cups = int(cups_var.get())
    multi_cup = multi_cup_var.get()
    same_cup = same_cup_var.get()
    island = island_var.get()
    island_limit = island_limit_var.get()
    balls_back = balls_back_var.get()
    consecutive_balls_back = consecutive_balls_back_var.get()

    if island_limit == "No limit":
        island_limit = None
    else:
        island_limit = int(island_limit)

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO rules (name, cups, multi_cup, same_cup, island, island_limit, balls_back, consecutive_balls_back) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (rule_name, cups, multi_cup, same_cup, island, island_limit, balls_back, consecutive_balls_back))
    conn.commit()

    # Save the rules and close the window
    button.config(state=tk.NORMAL)
    rules_window.destroy()
        
def start_new_tournament_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Start New Tournament")

    # Add widgets for creating a new tournament with selected teams and players here

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))
       
def view_games_and_tournaments_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("View Games and Tournaments")

    # Add widgets for viewing a list of past games and tournaments, with the option to view more detailed stats for each

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))    

def settings_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Settings")

    # Add widgets for displaying and editing settings here

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))
    
def close_window(window, button):
    window.destroy()
    if button:
        button.config(state=tk.NORMAL)    
    