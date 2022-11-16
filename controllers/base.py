from collections import defaultdict
from tinydb import TinyDB, where
from models.tournament import Tournament, Round, Match, TIME_CONTROL, STATUS_IN_PROGRESS, \
    STATUS_DONE, ALL_STATUS, NB_PLAYER_TOURNAMENT_MAX, NB_ROUND_TOURNAMENT, MATCH_WIN, MATCH_LOST, MATCH_DRAW
from models.player import Player
from datetime import datetime
import uuid

SEARCH_PLAYER_BY_NAME = "1"
SEARCH_PLAYER_BY_RANK = "2"
SEARCH_PLAYER_BY_ID = "3"


class Controller:
    """Main controller."""

    db = TinyDB("./db/db_chess.json")

    # def __init__(self, tournament: Tournament, view):
    def __init__(self, view):
        """init."""
        # self.tournament = tournament
        self.view = view
        self.players = []
        self.player_table = self.db.table('players', cache_size=0)
        self.tournament_table = self.db.table('tournaments', cache_size=0)
        self.round_table = self.db.table('rounds', cache_size=0)
        self.match_table = self.db.table('matchs', cache_size=0)

        """export tournament data."""

    def insert_player(self, player):
        return self.player_table.insert(player)

    def init_round(self, tournament):
        if tournament.rounds:
            number_round = len(tournament.rounds) + 1
        else:
            number_round = 1
        new_round = {
            "tournament_id": tournament.tournament_id,
            "round_id": str(uuid.uuid4()),
            "round_number": number_round,
            "status": STATUS_IN_PROGRESS,
            "name": f"Round {number_round}",
            "datetime_start": datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            "datetime_end": ""
        }
        tournament_round = Round()
        for k, v in new_round.items():
            setattr(tournament_round, k, v)
        self.round_table.insert(new_round)
        return tournament_round

    def init_match(self, first_round, tournament):

        # joueurs triés par rank
        player_sorted_by_rank = sorted(tournament.players, key=lambda x: x.rank)
        # On fait 2 tableaux de joueurs en prenant
        # la moitié des mieux classée et l'autre moitié des moins bien classée
        nb_player_per_group = int(len(player_sorted_by_rank) / 2)
        group_player_one = player_sorted_by_rank[:nb_player_per_group]
        group_player_two = player_sorted_by_rank[nb_player_per_group:]
        # Et on fait match les vis-à-vis (a 8 joueurs : 1 => 5, 2 => 6, 3 => 7, 4 => 8)
        match_list = zip(group_player_one, group_player_two)

        list_match_db = []
        for match in match_list:
            match_detail_for_obj = {
                "match_id": str(uuid.uuid4()),
                "round_id": first_round.round_id,
                "tournament_id": tournament.tournament_id,
                "status": STATUS_IN_PROGRESS,
                "players": match,
                "players_score": []
            }

            match_obj = Match()
            for k, v in match_detail_for_obj.items():
                setattr(match_obj, k, v)
            list_match_db.append(match_obj)

            list_player_match_db = []
            for players in match:
                list_player_match_db.append(players.player_id)
            match_detail_for_db = match_detail_for_obj.copy()
            match_detail_for_db["players"] = list_player_match_db
            self.match_table.insert(match_detail_for_db)

        return list_match_db

    def check_available_opponent(self, player_one, player_two, all_match):
        for match in all_match:
            if player_one.player_id in match.players and player_two.player_id in match.players:
                return False
        return True

    def create_match(self, tournament, round_tournament):
        all_player_sorted = self.get_score_by_player(tournament)
        player_sorted = []
        for players in all_player_sorted:
            player_sorted.append(players['player'])

        list_player = player_sorted.copy()

        # On récupère tous les matchs du tournoi
        all_match = self.get_match_by_tournament_id(tournament.tournament_id, STATUS_DONE)

        new_matchs_round = []
        loop = 1

        while len(list_player) > 0:
            i = 0
            available_opponent = False
            while not available_opponent:
                available_opponent = self.check_available_opponent(
                    list_player[0],
                    list_player[1 + i],
                    all_match
                )
                if not available_opponent and i < len(list_player) and loop < 4:
                    # Si l'adversaire a deja été joué, on cherche le suivant
                    i += 1
                elif loop == 4:
                    # Dernier match possible, donc on associe
                    available_opponent = True

            new_matchs_round.append([list_player[0], list_player[1 + i]])
            del list_player[1 + i]
            del list_player[0]
            loop += 1

        list_match_db = []
        for match in new_matchs_round:
            match_detail_for_obj = {
                "match_id": str(uuid.uuid4()),
                "round_id": round_tournament.round_id,
                "tournament_id": tournament.tournament_id,
                "status": STATUS_IN_PROGRESS,
                "players": match,
                "players_score": []
            }

            match_obj = Match()
            for k, v in match_detail_for_obj.items():
                setattr(match_obj, k, v)
            list_match_db.append(match_obj)

            list_player_match_db = []
            for players in match:
                list_player_match_db.append(players.player_id)
            match_detail_for_db = match_detail_for_obj.copy()
            match_detail_for_db["players"] = list_player_match_db
            self.match_table.insert(match_detail_for_db)

            round_tournament.set_matchs(list_match_db)

        return list_match_db

    def create_tournament(self):
        tournament_id = str(uuid.uuid4())
        name_tournament = self.view.get_name_tournament()
        location_tournament = self.view.get_location_tournament()
        date_start_tournament = self.view.get_date_start_tournament()
        date_end_tournament = self.view.get_date_end_tournament()
        number_round = NB_ROUND_TOURNAMENT
        # Création, donc round numéro 1
        actual_round = 1
        # On demande d'ajouter des joueurs tant qu'il n'y en a pas 8
        player = []
        list_player_db = []
        while len(self.players) < NB_PLAYER_TOURNAMENT_MAX:
            choice_add_player = self.view.get_choice_add_player_in_tournament()
            if choice_add_player == "1":
                # On crée un joueur
                player = self.create_player()
            elif choice_add_player == "2":
                # Get the choice how to search (by name or by rank)
                choice_search_player = self.view.menu_search_player()
                # Get the player selected
                player = self.search_player(choice_search_player)

            self.players.append(player)
            list_player_db.append(player.player_id)

        time_control = self.view.get_time_control_tournament(TIME_CONTROL)
        description = self.view.get_description()

        tournament_array_for_obj = {
            "tournament_id": tournament_id,
            "name": name_tournament,
            "location": location_tournament,
            "date_start": date_start_tournament,
            "date_end": date_end_tournament,
            "number_round": number_round,
            "actual_round": actual_round,
            "players": self.players,
            "time_control": TIME_CONTROL[time_control],
            "description": description,
            "status": STATUS_IN_PROGRESS
        }

        tournament_array_for_db = tournament_array_for_obj.copy()
        # Pour la base de données, on ne stocke que l'id des joueurs et pas l'objet joueur entier
        tournament_array_for_db["players"] = list_player_db

        tournament = Tournament()
        for k, v in tournament_array_for_obj.items():
            setattr(tournament, k, v)

        self.tournament_table.insert(tournament_array_for_db)

        first_round = self.init_round(tournament)
        tournament.set_rounds(first_round)
        matchs = self.init_match(first_round, tournament)
        first_round.set_matchs(matchs)

        return tournament

    def get_round_by_tournament_id(self, tournament_id, round_status=ALL_STATUS):

        if round_status == ALL_STATUS:
            rounds_db = self.round_table.search((where("tournament_id") == tournament_id))
        else:
            rounds_db = self.round_table.search((where("tournament_id") == tournament_id) &
                                                (where("status") == round_status))
        all_round_by_tournament = []
        for list_round in rounds_db:
            tournament_round = Round()
            for k, v in list_round.items():
                setattr(tournament_round, k, v)
            all_round_by_tournament.append(tournament_round)
        return all_round_by_tournament

    def get_score_by_player(self, tournament):
        player_sorted_by_score = []
        score = defaultdict(list)
        # On récupère les matchs terminés du tournoi
        matchs = self.get_match_by_tournament_id(tournament.tournament_id, STATUS_DONE)
        for match in matchs:
            for player_score in match.players_score:
                score[player_score.get("player_id")].append(player_score.get("score"))
        # On trie les joueurs par score
        for id_player, score_player in sorted(score.items(), key=lambda x: sum(x[1]), reverse=True):
            player = self.search_player(SEARCH_PLAYER_BY_ID, id_player)
            player_with_score = {
                "player": player,
                "score": sum(score_player)
            }
            player_sorted_by_score.append(player_with_score)
        # joueurs triés par rank
        all_player_rank_sorted = sorted(player_sorted_by_score, key=lambda x: x['player'].rank, reverse=False)
        # joueurs triés par score
        all_player = sorted(all_player_rank_sorted, key=lambda x: x['score'], reverse=True)
        return all_player

    def get_match_by_round_id(self, round_id, match_status=ALL_STATUS):
        if match_status == ALL_STATUS:
            matchs_db = self.match_table.search((where("round_id") == round_id))
        else:
            matchs_db = self.match_table.search(
                (where("round_id") == round_id) &
                (where("status") == match_status)
            )
        all_match_by_round = []
        for list_match in matchs_db:
            # On récupère les joueurs (objets) du match
            player_match = []
            for player_id in list_match["players"]:
                player = self.search_player(SEARCH_PLAYER_BY_ID, player_id)
                player_match.append(player)

            list_match["players"] = player_match

            round_match = Match()
            for k, v in list_match.items():
                setattr(round_match, k, v)
            all_match_by_round.append(round_match)
        del matchs_db
        return all_match_by_round

    def get_match_by_tournament_id(self, tournament_id, match_status=ALL_STATUS):
        if match_status == ALL_STATUS:
            matchs_db = self.match_table.search((where("tournament_id") == tournament_id))
        else:
            matchs_db = self.match_table.search(
                (where("tournament_id") == tournament_id) &
                (where("status") == match_status)
            )
        all_match_by_tournament = []
        for list_match in matchs_db:
            # On récupère les joueurs (objets) du match
            player_match = []
            for player_id in list_match["players"]:
                player = self.search_player(SEARCH_PLAYER_BY_ID, player_id)
                player_match.append(player)

            list_match["players"] = player_match

            round_match = Match()
            for k, v in list_match.items():
                setattr(round_match, k, v)
            all_match_by_tournament.append(round_match)
        del matchs_db
        return all_match_by_tournament

    def resume_tournament(self):
        tournament_list = []
        tournament_search = self.tournament_table.search(where("status") == STATUS_IN_PROGRESS)

        if len(tournament_search) == 0:
            return self.view.no_tournament()

        for tournament_find in tournament_search:
            tournament_list.append(tournament_find)

        if len(tournament_list) > 1:
            selected_tournament = self.view.menu_select_tournament(tournament_list)
        else:
            selected_tournament = tournament_list[0]

        for player_id in selected_tournament["players"]:
            player = self.search_player(SEARCH_PLAYER_BY_ID, player_id)
            self.players.append(player)

        selected_tournament["players"] = self.players

        tournament = Tournament()
        for k, v in selected_tournament.items():
            setattr(tournament, k, v)

        # On récupère les rounds du tournoi
        rounds = self.get_round_by_tournament_id(tournament.tournament_id, ALL_STATUS)
        for round_list in rounds:
            # On récupère les matchs du round
            # matchs = self.get_match_by_round_id(round_list.round_id, STATUS_IN_PROGRESS)
            matchs = self.get_match_by_round_id(round_list.round_id, ALL_STATUS)

            for matchs_list in matchs:
                # On instancie les matchs dans chaque round
                round_list.set_matchs(matchs_list)
            tournament.set_rounds(round_list)

        return tournament

    def get_histo_tournament(self):
        tournament_list = []
        tournament_search = self.tournament_table.search(where("status") == STATUS_DONE)

        if len(tournament_search) == 0:
            return self.view.no_tournament_done()

        for tournament_find in tournament_search:
            tournament_list.append(tournament_find)

        if len(tournament_list) > 1:
            selected_tournament = self.view.menu_select_tournament(tournament_list)
        else:
            selected_tournament = tournament_list[0]

        for player_id in selected_tournament["players"]:
            player = self.search_player(SEARCH_PLAYER_BY_ID, player_id)
            self.players.append(player)

        selected_tournament["players"] = self.players

        tournament = Tournament()
        for k, v in selected_tournament.items():
            setattr(tournament, k, v)

        # On récupère les rounds du tournoi
        rounds = self.get_round_by_tournament_id(tournament.tournament_id, STATUS_DONE)
        for round_list in rounds:
            # On récupère les matchs du round
            matchs = self.get_match_by_round_id(round_list.round_id, STATUS_DONE)

            for matchs_list in matchs:
                # On instancie les matchs dans chaque round
                round_list.set_matchs(matchs_list)
            tournament.set_rounds(round_list)

        return tournament

    def create_player(self):
        new_player = self.view.create_player()
        # Cast en string de l'uuid sinon json pas content
        player_id = str(uuid.uuid4())
        # On ajoute l'uuid en tant qu'id dans player
        new_player["player_id"] = player_id

        player = Player()
        for k, v in new_player.items():
            setattr(player, k, v)
        # On insert le player dans la db
        self.insert_player(new_player)
        return player

    def update_player_rank(self, player):
        # On demande le noveau rank
        new_rank = self.view.update_rank(player)
        # On maj le player avec le nouveau rank
        self.player_table.update({"rank": new_rank}, where("player_id") == player.player_id)
        player.rank = new_rank
        return player

    def search_player(self, choice_search_player, player_id=""):
        player_search = []
        players_list = []

        if choice_search_player == SEARCH_PLAYER_BY_NAME:
            search_name = self.view.menu_search_by_name()
            player_search = self.player_table.search(where("lastname") == search_name)

        elif choice_search_player == SEARCH_PLAYER_BY_RANK:
            search_rank = self.view.menu_search_by_rank()
            player_search = self.player_table.search(where("rank") == search_rank)

        elif choice_search_player == SEARCH_PLAYER_BY_ID:
            player_search = self.player_table.search(where("player_id") == player_id)

        for player_find in player_search:
            player = Player()
            for k, v in player_find.items():
                setattr(player, k, v)
            players_list.append(player)

        if len(players_list) > 1:
            selected_player = self.view.menu_select_player(players_list)
        else:
            selected_player = players_list[0]
        return selected_player

    def set_score(self, choice_match, winner):
        players_score = []
        # On boucle sur les joueurs du match pour leurs mettre le score
        for player in choice_match.players:
            if len(winner) > 1:
                # Si 2 gagnants, alors match nul
                players_score.append({"player_id": player.player_id, "score": MATCH_DRAW})
            elif player.player_id == winner[0].player_id and len(winner) == 1:
                # Si le joueur est le gagnant et qu'il n'y a qu'un gagnant, c'est le gagnant
                players_score.append({"player_id": winner[0].player_id, "score": MATCH_WIN})
            else:
                # Sinon, c'est le perdant
                players_score.append({"player_id": player.player_id, "score": MATCH_LOST})

        # ajout score dans l'objet match
        choice_match.set_players_score(players_score)
        # ajout score dans la table match
        self.match_table.update(
            {
                "players_score": players_score,
                "status": STATUS_DONE
            },
            where("match_id") == choice_match.match_id
        )
        return choice_match

    def update_round(self, round_tournament, status):
        round_tournament.set_status(status)
        self.round_table.update(
            {
                "status": status,
                "datetime_end": datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            },
            where("round_id") == round_tournament.round_id
        )

    def update_actual_round_tournament(self, tournament, new_round):
        tournament.set_actual_round(new_round.round_number)
        tournament.set_rounds(new_round)
        self.tournament_table.update(
            {"actual_round": tournament.actual_round},
            where("tournament_id") == tournament.tournament_id
        )

    def update_status_tournament(self, tournament, status):
        tournament.set_status(status)
        self.tournament_table.update(
            {"status": status},
            where("tournament_id") == tournament.tournament_id
        )

    def is_match_in_progress_by_round_id(self, round_id):
        matchs = self.get_match_by_round_id(round_id, STATUS_IN_PROGRESS)
        if len(matchs) == 0:
            return False
        else:
            return True

    def play_tournament(self, tournament):
        if not isinstance(tournament, Tournament):
            # Si on ne récupère pas un tournoi
            self.get_menu_choice()
        # On parcours les rounds
        for round_tournament in tournament.rounds:
            flag_match_in_progress = True
            while round_tournament.status == STATUS_IN_PROGRESS and flag_match_in_progress:
                # Si on a des matchs
                if len(round_tournament.matchs) > 0:
                    # On récupère la liste des matchs en cours pour le round
                    # afin d'avoir toujours une liste de match à jour
                    matchs = self.get_match_by_round_id(round_tournament.round_id, STATUS_IN_PROGRESS)
                    # Si on a plus de match en cours
                    if len(matchs) == 0:
                        # No match in progress => update round to done
                        flag_match_in_progress = False
                        self.update_round(round_tournament, STATUS_DONE)
                        self.view.round_done(round_tournament)
                        # And create a new one if nb_round < 4
                        if len(tournament.rounds) < 4:
                            # Add new round to tournament
                            new_round = self.init_round(tournament)
                            self.view.round_next(new_round)
                            self.update_actual_round_tournament(tournament, new_round)
                            self.create_match(tournament, new_round)
                        else:
                            # Tournoi terminé
                            self.view.all_match_done(tournament)
                            player_score = self.get_score_by_player(tournament)
                            self.update_status_tournament(tournament, STATUS_DONE)
                            self.view.get_result_tournament(player_score)
                            self.get_menu_choice()
                    else:
                        # Des matchs sont toujours en cours
                        choice_match = self.view.get_choice_match(matchs)
                        winner = self.view.get_winner_match(choice_match)
                        self.set_score(choice_match, winner)
                else:
                    flag_match_in_progress = False
                    self.update_round(round_tournament, STATUS_DONE)
                    new_round = self.init_round(tournament)
                    self.view.round_next(new_round)
                    self.update_actual_round_tournament(tournament, new_round)
                    self.create_match(tournament, new_round)

    def get_menu_choice(self):
        menu_choice = self.view.menu()

        if menu_choice == "1":
            player = self.create_player()
            self.view.player_infos(player)
            self.get_menu_choice()

        elif menu_choice == "2":
            # Get the choice (by name or by rank)
            choice_search_player = self.view.menu_search_player()
            # Get the player selected
            player = self.search_player(choice_search_player)
            # Update the player rank
            self.update_player_rank(player)
            self.get_menu_choice()

        elif menu_choice == "3":
            tournament = self.create_tournament()
            self.play_tournament(tournament)

        elif menu_choice == "4":
            tournament = self.resume_tournament()
            self.play_tournament(tournament)

        elif menu_choice == "5":
            tournament = self.get_histo_tournament()
            player_score = self.get_score_by_player(tournament)
            self.view.get_result_tournament(player_score)
            self.get_menu_choice()
