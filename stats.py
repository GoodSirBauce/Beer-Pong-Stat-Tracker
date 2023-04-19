import tkinter as tk
from db_operations import create_connection, get_all_players, get_all_teams

def create_players_listbox(window, display_stats):
    conn = create_connection()
    players = get_all_players(conn)
    player_names = [player[1] for player in players]

    players_listbox = tk.Listbox(window)
    players_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky=tk.N + tk.S)

    for player_name in player_names:
        players_listbox.insert(tk.END, player_name)

    players_listbox.bind("<<ListboxSelect>>", lambda event: display_stats(window, players[event.widget.curselection()[0]], "player"))

    return players_listbox

def create_teams_listbox(window, display_stats):
    conn = create_connection()
    teams = get_all_teams(conn)
    team_names = [team[1] for team in teams]

    teams_listbox = tk.Listbox(window)
    teams_listbox.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky=tk.N + tk.S)

    for team_name in team_names:
        teams_listbox.insert(tk.END, team_name)

    teams_listbox.bind("<<ListboxSelect>>", lambda event: display_stats(window, teams[event.widget.curselection()[0]], "team"))

    return teams_listbox

def show_listbox(window, item_type):
    # Remove existing widgets in the window
    for widget in window.winfo_children():
        widget.destroy()

    if item_type == "player":
        create_players_listbox(window, display_stats)
    elif item_type == "team":
        create_teams_listbox(window, display_stats)
    else:
        print("Error: Unsupported item_type.")
        return

def display_stats(window, selected_item, item_type):
    # Clear any existing widgets in the window
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

    if item_type == "player":
        table_name = "players"
    elif item_type == "team":
        table_name = "teams"
    else:
        print("Error: Unsupported item_type.")
        return

    conn = create_connection()
    stats_data = get_stats(selected_item[1], table_name, conn)
    
    if stats_data is None:
        print("Error: No stats found.")
        return


    # Display the statistics in a formatted way
    for index, (stat_name, stat_value) in enumerate(stats_data.items()):
        label = tk.Label(window, text=f"{stat_name}: {stat_value}")
        label.grid(row=index + 1, column=2, padx=10, pady=2, sticky=tk.W)


def get_stats(selected_name, table_name, conn):
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE name=?"
    cur.execute(query, (selected_name,))
    result = cur.fetchone()

    if result is None:
        print(f"Error: {table_name.capitalize()} with ID {selected_name} not found.")
        return None
    
    # Map the statistics to a dictionary (update the keys to match your desired statistic names)
    stats_data = {
        "ID": result[0],
        "Name": result[1],
        "Wins": result[2],
        "Losses": result[3],
        "Shot Percentage": result[4],
        "Shot Percentage: 10-7 cups": result[5],
        "Shot Percentage: 6-4 cups": result[6],
        "Shot Percentage: 3-1 cups": result[7],
        "Shooter Rating": result[8],
        "Hit Streak": result[9],
        "Best 10 Cup Game": result[10],
        "Bounce Shot Percentage": result[11],
        "Cups Per Game": result[12],
        "Hits": result[13],
        "Misses": result[14],
        "Multi-Cups": result[15],
        "Bounce Hits": result[16],
        "Bounce Misses": result[17],
        "Balls Back": result[18],
        "Defends: Finger": result[19],
        "Defends: Swats": result[20],
        "Offensive Recovery": result[21],
        "Trick Shot Attempts": result[22],
        "Trick Shot Hits": result[23],
        "Redemption Attempts": result[24],
        "Redemption Hits": result[25],
        "Redemption Denied": result[26],
        "Party Fouls": result[27],
        "Elbow Fouls": result[28],
        "Island Attempts": result[29],
        "Island Hits": result[30],
        "Average Cups Remaining": result[31],
        "Most Shots in One Game": result[32],
        "Least Shots in One Game": result[33],
    }

    return stats_data
