from typing import Dict
import tkinter as tk

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.record = {"wins": 0, "losses": 0}
        self.shotPercentage = 0.0
        self.shooterRating = 0
        self.shotPercentageBreakdown = {"10-7_cups": 0.0, "6-4_cups": 0.0, "3-1_cups": 0.0}
        self.hitStreak = 0
        self.best10CupGame = 0
        self.bounceShotPercentage = 0.0
        self.cupsPerGame = 0
        self.hits = 0
        self.misses = 0
        self.multiCups = 0
        self.bounceHits = 0
        self.bounceMisses = 0
        self.ballsBack = 0
        self.defendsFinger = 0
        self.defendsSwats = 0
        self.offensiveRecovery = 0
        self.trickShotsAttempt = 0
        self.trickShotsHit = 0
        self.redemptionsAttempt = 0
        self.redemptionsHit = 0
        self.redemptionsDenied = 0
        self.partyFouls = 0
        self.elbowFouls = 0
        self.islandsAttempt = 0
        self.islandsHit = 0
        self.avgCupRemaining = 0.0
        self.mostShotsOneGame = 0
        self.leastShotsOneGame = 0
        self.tournamentWins = 0

    def add_player(self, player):  # Add this method to add a player to the team
        self.players.append(player)