import tkinter as tk
from player import Player
from team import Team
from db_operations import (create_connection, create_tables, get_all_players, get_all_teams, refresh_player_list, refresh_team_list,
                           add_player, delete_player, edit_player, add_team, delete_team, edit_team)
from windows import (show_delete_warning, close_window, edit_players_window, edit_teams_window, edit_player_window, edit_team_window, start_new_game_window,
                     stats_window, rules_editor_window, start_new_tournament_window, view_games_and_tournaments_window,
                     settings_window)

def close_app(conn, root):
    conn.close()
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Beer Pong Stat Tracker")
    
    conn = create_connection()
    if conn:
        create_tables(conn)
    else:
        print("Error! Cannot establish a database connection.")
    
    # Create main menu buttons
    start_new_game_btn = tk.Button(root, text="Start New Game", command=lambda: start_new_game_window(start_new_game_btn))
    start_new_game_btn.grid(row=0, column=0, padx=10, pady=10)
    
    stats_btn = tk.Button(root, text="Stats", command=lambda: stats_window(stats_btn))
    stats_btn.grid(row=0, column=1, padx=10, pady=10)
    
    rules_editor_btn = tk.Button(root, text="Rules Editor", command=lambda: rules_editor_window(rules_editor_btn))
    rules_editor_btn.grid(row=0, column=2, padx=10, pady=10)
    
    edit_players_btn = tk.Button(root, text="Edit Players", command=lambda: edit_players_window(edit_players_btn))
    edit_players_btn.grid(row=0, column=3, padx=10, pady=10)
    
    edit_teams_btn = tk.Button(root, text="Edit Teams", command=lambda: edit_teams_window(edit_teams_btn))
    edit_teams_btn.grid(row=0, column=4, padx=10, pady=10)
    
    start_new_tournament_btn = tk.Button(root, text="Start New Tournament", command=lambda: start_new_tournament_window(start_new_tournament_btn))
    start_new_tournament_btn.grid(row=0, column=5, padx=10, pady=10)
    
    view_games_and_tournaments_btn = tk.Button(root, text="View Games and Tournaments", command=lambda: view_games_and_tournaments_window(view_games_and_tournaments_btn))
    view_games_and_tournaments_btn.grid(row=0, column=6, padx=10, pady=10)
    
    settings_btn = tk.Button(root, text="Settings", command=lambda: settings_window(settings_btn))
    settings_btn.grid(row=0, column=7, padx=10, pady=10)

    # Add more buttons here
    
    # Bind the window close button to the close_app function
    root.protocol("WM_DELETE_WINDOW", lambda: close_app(conn, root))
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
