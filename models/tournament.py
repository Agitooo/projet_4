from typing import List
from models.player import Player

TIME_CONTROL = {1: "bullet", 2: "blitz", 3: "coup rapide"}
MATCH_WIN = 1.0
MATCH_LOST = 0.0
MATCH_DRAW = 0.5
NB_PLAYER_TOURNAMENT_MAX = 8
NB_ROUND_TOURNAMENT = 4
STATUS_IN_PROGRESS = "1"
STATUS_DONE = "2"
ALL_STATUS = "all"


class Tournament:
    """Tournament."""

    def __init__(self, **kwargs):
        """Has a name, location, date, number_round, turn, players, time_control and description."""
        self.tournament_id = kwargs.get("tournament_id")
        self.name = kwargs.get("name")
        self.location = kwargs.get("location")
        self.date_start = kwargs.get("date_start")
        self.date_end = kwargs.get("date_end")
        self.number_round = kwargs.get("number_round")
        self.actual_round = kwargs.get("actual_round")
        self.players: List[Player] = kwargs.get("players")
        self.time_control = kwargs.get("time_control")
        self.description = kwargs.get("description")
        self.status = kwargs.get("status")
        self.rounds: List[Round] = []

    def set_actual_round(self, rounds):
        self.actual_round = rounds

    def set_status(self, status):
        self.status = status

    def set_rounds(self, rounds):
        self.rounds.append(rounds)

    def get_tournament_detail(self):
        list_player = ""
        for index, player_choice in enumerate(self.players):
            list_player += f"{index + 1} : {player_choice.get_player_infos()} \n"
        return f"Tournois {self.name} à {self.location} le {self.date_start}.\n" \
               f"La liste des joueurs :\n" \
               f"{list_player}" \
               f"le tournois est actuellement au round {self.actual_round}/{str(self.number_round)} " \
               f"en mode {self.time_control}"

    def __str__(self):
        """Used in print."""
        return f"name: {self.name}, location: {self.location}, date_start: {self.date_start}, " \
               f"date_end: {self.date_end}, number_round: {self.number_round}, round: {self.actual_round}, " \
               f"player: {self.players}, time_control: {self.time_control}, description: {self.description}, " \
               f"status: {self.status}, rounds: {self.rounds}"

    def __repr__(self):
        """Used in print."""
        return str(self)


class Match:
    """Match."""

    def __init__(self, **kwargs):
        self.match_id = kwargs.get("match_id")
        self.round_id = kwargs.get("round_id")
        self.tournament_id = kwargs.get("tournament_id")
        self.status = kwargs.get("status")
        self.players: List[Player] = kwargs.get("player")
        self.players_score = []

    def __str__(self):
        """Used in print."""
        return f"match_id: {self.match_id}, status {self.status}, round_id: {self.round_id}"

    def __repr__(self):
        """Used in print."""
        return str(self)

    def get_match_detail(self):
        return f"Le match va opposer {self.players[0].get_player_name()} (rang : {self.players[0].rank}) " \
               f"à {self.players[1].get_player_name()} (rang : {self.players[1].rank})."

    def get_versus(self):
        return f"{self.players[0].get_player_name()} (rang : {self.players[0].rank}) " \
               f"contre {self.players[1].get_player_name()} (rang : {self.players[1].rank})."

    def set_players_score(self, players_score):
        self.players_score = players_score


class Round:
    """Round."""

    def __init__(self, **kwargs):
        self.round_id = kwargs.get("round_id")
        self.tournament_id = kwargs.get("tournament_id")
        self.name = kwargs.get("name")
        self.round_number = kwargs.get("round_number")
        self.status = kwargs.get("status")
        self.datetime_start = kwargs.get("datetime_start")
        self.datetime_end = kwargs.get("datetime_end")
        self.matchs: List[Match] = []

    def set_status(self, status):
        self.status = status

    def set_matchs(self, matchs):
        self.matchs.append(matchs)

    def get_round_detail(self):
        if self.status == STATUS_IN_PROGRESS:
            status = "en cours"
        else:
            status = "terminé"
        return f"Le {self.name} est {status}"

    def __str__(self):
        """Used in print."""
        return f"name: {self.name}, status {self.status}, datetime_start: {self.datetime_start}, " \
               f"datetime_end: {self.datetime_end}"

    def __repr__(self):
        """Used in print."""
        return str(self)
