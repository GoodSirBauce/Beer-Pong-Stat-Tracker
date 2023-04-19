import tkinter as tk
from tkinter import messagebox
from db_operations import (create_connection, create_tables, get_all_players, get_all_teams, refresh_player_list, refresh_team_list,
                           add_player, delete_player, edit_player, add_team, delete_team, edit_team)
from stats import (create_players_listbox, create_teams_listbox, show_listbox, display_stats, get_stats)

def show_delete_warning():
    return messagebox.askyesno("Delete Warning", "Are you sure you want to delete this player or team? This action cannot be undone.")
  
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
    
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))
      
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
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))
    
def start_new_game_window(button):
    button.config(state=tk.DISABLED)
    window = tk.Toplevel()
    window.title("Start New Game")

    # Add labels, dropdowns, and other widgets for starting a new game here
    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window, button))

def stats_window(button):
    button.config(state=tk.DISABLED)
    stats_window = tk.Toplevel()
    stats_window.title("Stats")
    
    # Inside your main function or where you create the main window
    players_button = tk.Button(stats_window, text="Players", command=lambda: show_listbox(stats_window, "player"))
    players_button.grid(row=0, column=0, padx=10, pady=10)

    teams_button = tk.Button(stats_window, text="Teams", command=lambda: show_listbox(stats_window, "team"))
    teams_button.grid(row=0, column=1, padx=10, pady=10)

    close_button = tk.Button(stats_window, text="Close", command=lambda: close_window(stats_window, button))
    close_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    stats_window.protocol("WM_DELETE_WINDOW", lambda: close_window(stats_window, button))
    
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
    