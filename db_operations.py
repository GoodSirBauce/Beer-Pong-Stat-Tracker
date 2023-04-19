import sqlite3
from player import Player
from team import Team
import tkinter as tk

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("beer_pong_stats.db")
    except sqlite3.Error as e:
        print(e)
    
    create_rules_table(conn)
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    # Create players table
    players_table = """
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        wins INTEGER,
        losses INTEGER,
        shot_percentage REAL,
        shot_percentage_10_7 REAL,
        shot_percentage_6_4 REAL,
        shot_percentage_3_1 REAL,
        shooter_rating REAL,
        hit_streak INTEGER,
        best_10_cup_game INTEGER,
        bounce_shot_percentage REAL,
        cups_per_game REAL,
        hits INTEGER,
        misses INTEGER,
        mutli_cups INTEGER,
        bounce_hits INTEGER,
        bounce_misses INTEGER,
        balls_back INTEGER,
        defends_finger INTEGER,
        defends_swats INTEGER,
        offensive_recovery INTEGER,
        trick_shot_attempt INTEGER,
        trick_shot_hit INTEGER,
        redemption_attempt INTEGER,
        redemption_hit INTEGER,
        redemption_denied INTEGER,
        party_fouls INTEGER,
        elbow_fouls INTEGER,
        island_attempt INTEGER,
        island_hit INTEGER,
        avg_cup_remaining REAL,
        most_shots_one_game INTEGER,
        least_shots_one_game INTEGER

    );
    """

    # Create teams table
    teams_table = """
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        wins INTEGER,
        losses INTEGER,
        shot_percentage REAL,
        shot_percentage_10_7 REAL,
        shot_percentage_6_4 REAL,
        shot_percentage_3_1 REAL,
        shooter_rating REAL,
        hit_streak INTEGER,
        best_10_cup_game INTEGER,
        bounce_shot_percentage REAL,
        cups_per_game REAL,
        hits INTEGER,
        misses INTEGER,
        mutli_cups INTEGER,
        bounce_hits INTEGER,
        bounce_misses INTEGER,
        balls_back INTEGER,
        defends_finger INTEGER,
        defends_swats INTEGER,
        offensive_recovery INTEGER,
        trick_shot_attempt INTEGER,
        trick_shot_hit INTEGER,
        redemption_attempt INTEGER,
        redemption_hit INTEGER,
        redemption_denied INTEGER,
        party_fouls INTEGER,
        elbow_fouls INTEGER,
        island_attempt INTEGER,
        island_hit INTEGER,
        avg_cup_remaining REAL,
        most_shots_one_game INTEGER,
        least_shots_one_game INTEGER
    );
    """

    cursor.execute(players_table)
    cursor.execute(teams_table)
    conn.commit()
    
def create_rules_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    cups INTEGER,
                    multi_cup INTEGER,
                    same_cup INTEGER,
                    island INTEGER,
                    island_limit INTEGER,
                    balls_back INTEGER,
                    consecutive_balls_back INTEGER)''')
    conn.commit()
    
def get_all_players(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM players")
    return cur.fetchall()

def get_all_teams(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams")
    return cur.fetchall()

def refresh_player_list(players_listbox, conn):
    players_listbox.delete(0, tk.END)
    for player in get_all_players(conn):
        players_listbox.insert(tk.END, f"{player[0]}. {player[1]}")
        
def refresh_team_list(teams_listbox, conn):
    teams_listbox.delete(0, tk.END)
    for team in get_all_teams(conn):
        teams_listbox.insert(tk.END, f"{team[0]}. {team[1]}")        

def add_player(name, conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (name, wins, losses, shot_percentage, shot_percentage_10_7, shot_percentage_6_4, shot_percentage_3_1, shooter_rating, hit_streak, best_10_cup_game, bounce_shot_percentage, cups_per_game, hits, misses, mutli_cups, bounce_hits, bounce_misses, balls_back, defends_finger, defends_swats, offensive_recovery, trick_shot_attempt, trick_shot_hit, redemption_attempt, redemption_hit, redemption_denied, party_fouls, elbow_fouls, island_attempt, island_hit, avg_cup_remaining, most_shots_one_game, least_shots_one_game)
        VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    """, (name,))
    conn.commit()

def delete_player(player_id, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()
            
def edit_player(player_id, updated_name, conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET name = ? WHERE id = ?", (updated_name, player_id))
    conn.commit()
    
def add_team(name, conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teams (name, wins, losses, shot_percentage, shot_percentage_10_7, shot_percentage_6_4, shot_percentage_3_1, shooter_rating, hit_streak, best_10_cup_game, bounce_shot_percentage, cups_per_game, hits, misses, mutli_cups, bounce_hits, bounce_misses, balls_back, defends_finger, defends_swats, offensive_recovery, trick_shot_attempt, trick_shot_hit, redemption_attempt, redemption_hit, redemption_denied, party_fouls, elbow_fouls, island_attempt, island_hit, avg_cup_remaining, most_shots_one_game, least_shots_one_game)
        VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    """, (name,))
    conn.commit()

def delete_team(team_id, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    conn.commit()

def edit_team(team_id, updated_name, conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE teams SET name = ? WHERE id = ?", (updated_name, team_id))
    conn.commit()