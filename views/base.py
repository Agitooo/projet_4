from datetime import datetime


class View:
    """Main controller."""

    def create_tournament(self):
        """creer tournois"""

    def add_player(self):
        """ajouter joueur"""

    def generate_round(self):
        """generer round"""

    def get_result_match(self):
        """resultat match"""

    def get_result_round(self):
        """resultat round"""

    def get_report(self):
        """sortir un rapport"""

    def get_choice_add_player_in_tournament(self):
        choice_add_player = ""
        allowed_menu_choice_add_player = ["1", "2"]
        while choice_add_player not in allowed_menu_choice_add_player:
            choice_add_player = input("Ajouter un joueur au tournois :  \n "
                                      "1 : Créer un nouveau joueur \n "
                                      "2 : Rechercher une joueur \n ")
        return choice_add_player

    def get_name_tournament(self):
        name_tournament = ""
        while not name_tournament:
            name_tournament = input("Saisissez le nom du tournois : ")
        return name_tournament

    def get_location_tournament(self):
        location_tournament = ""
        while not location_tournament:
            location_tournament = input("Saisissez le lieu du tournois : ")
        return location_tournament

    def get_date_start_tournament(self):
        date_start_tournament = ""
        date_start_tournament_valid = ""
        while not date_start_tournament:
            date_start_tournament = input("Saisissez la date de debut du tournois (jj/mm/aaaa) : ")
            date_start_tournament_valid = self.verif_date(date_start_tournament)
        return date_start_tournament_valid

    def get_date_end_tournament(self):
        date_end_tournament = ""
        date_end_tournament_valid = ""
        while not date_end_tournament:
            date_end_tournament = input("Saisissez la date de fin du tournois (jj/mm/aaaa) : ")
            date_end_tournament_valid = self.verif_date(date_end_tournament)
        return date_end_tournament_valid

    def get_time_control_tournament(self, time_control):
        choice_time_control_tournament = 0
        list_time_control = ""
        allowed_time_control_choice = range(1, len(time_control) + 1)

        for index, time_control_choice in time_control.items():
            list_time_control += f"{index} : {time_control_choice} \n"

        while int(choice_time_control_tournament) not in allowed_time_control_choice:
            choice_time_control_tournament = input(f"Choisissez le contrôle du temps : \n"
                                                   f"{list_time_control}")
        return int(choice_time_control_tournament)

    def get_choice_match(self, matchs):
        choice_match = 0
        list_match = ""
        allowed_choice_match = range(1, len(matchs) + 1)

        for index, match_choice in enumerate(matchs):
            list_match += f"{index + 1} : {match_choice.get_versus()} \n"

        while int(choice_match) not in allowed_choice_match:
            choice_match = input(f"Choisissez le match pour saisir le score : \n"
                                 f"{list_match}")
        return matchs[int(choice_match) - 1]

    def get_winner_match(self, match):
        choice_winner = 0
        list_resultat = ""
        # On fait +2, car il y a le joueur 1, le joueur 2 ou le match nul
        allowed_choice_winner = range(1, len(match.players) + 2)

        dict_resultat = {index + 1: player for index, player in enumerate(match.players)}
        dict_resultat = {3: "Match nul entre les 2 joueurs", **dict_resultat}

        sorted_keys = sorted(dict_resultat.keys())
        for key in sorted_keys:
            if key != 3:
                list_resultat += f"{key}: {dict_resultat[key].get_player_name()} \n"
            else:
                list_resultat += f"{key}: {dict_resultat[key]} \n"

        while int(choice_winner) not in allowed_choice_winner:
            choice_winner = input(f"Choisissez le vainqueur : \n"
                                  f"{list_resultat}")
        winner = []

        if choice_winner == "3":
            winner = match.players
        else:
            winner.append(dict_resultat[int(choice_winner)])
        return winner

    def get_description(self):
        description = ""
        while not description:
            description = input("Saisissez une description : ")
        return description

    def verif_date(self, date):
        try:
            nouvelle_date = datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
            return nouvelle_date
        except ValueError:
            print("format de date invalide, 'jj/mm/aaaa' attendu")

    def create_player(self):
        """Create player."""

        firstname = ""
        lastname = ""
        birthdate = ""
        civility = ""
        rank = ""

        allowed_civility_choice = ["1", "2", "3"]

        while not firstname:
            firstname = input("Saisissez le prénom du joueur : ")
        while not lastname:
            lastname = input("Saisissez le nom du joueur : ")
        while not birthdate:
            birthdate = input("Saisissez date de naissance du joueur (jj/mm/aaaa): ")
            birthdate = self.verif_date(birthdate)
        while not (civility in allowed_civility_choice):
            civility = input("Saisissez la civilité du joueur (1 = Femme, 2 = Homme, 3 = Autre) : ")
        while not rank:
            rank = input("Saisissez le classement du joueur : ")

        return {"firstname": firstname, "lastname": lastname,
                "birthdate": birthdate, "civility": civility, "rank": rank}

    def menu_search_player(self):
        choice_search_player = ""
        allowed_menu_choice_search_player = ["1", "2"]
        while not (choice_search_player in allowed_menu_choice_search_player):
            choice_search_player = input("Rechercher un joueur par son :  \n "
                                         "1 : Nom \n "
                                         "2 : Classement \n ")
        return choice_search_player

    def menu_search_by_name(self):
        search_name = ""
        while not search_name:
            search_name = input("Saisissez le nom du joueur : ")
        return search_name

    def menu_search_by_rank(self):
        search_rank = ""
        while not search_rank:
            search_rank = input("Saisissez le classement du joueur : ")
        return search_rank

    def update_rank(self, player):
        """maj rank"""
        rank = ""
        while not rank:
            rank = input(f"tapez le nouveau classement du joueur {player.firstname} {player.lastname} "
                         f"(actuellement {player.rank}) : ")
        return rank

    def get_result_tournament(self, all_player):
        """maj rank"""
        recap = "Voici le classement des joueurs : \n"
        for index, player in enumerate(all_player):
            if isinstance(player['score'], int):
                score = int(player['score'])
            else:
                score = player['score']
            recap += f"{index + 1} : {player['player'].get_player_infos()} avec un score de {score} \n"
        return print(recap)

    def menu(self):
        choice = ""
        allowed_menu_choice = ["1", "2", "3", "4", "5"]

        while not (choice in allowed_menu_choice):
            choice = input("Veuillez choisir un action :  \n "
                           "1 : Créer un nouveau joueur  \n "
                           "2 : Mettre à jour le classement d'un joueur  \n "
                           "3 : Créer un tournoi  \n "
                           "4 : Reprendre un tournoi en cour \n "
                           "5 : Consulter l'historique des tournois \n")
        return choice

    def menu_select_player(self, player):
        player_selected = 0
        list_player = ""
        # le range fait max -1... donc pour le créer dynamiquement faut faire +1... logique -_-
        allowed_select_player_choice = range(1, len(player) + 1)

        for index, player_choice in enumerate(player):
            list_player += f"{index + 1} : {player_choice.get_player_infos()} \n"

        while int(player_selected) not in allowed_select_player_choice:
            player_selected = input(f"Plusieurs joueurs correspondent a votre recherche, veuillez en selection un : \n"
                                    f"{list_player} \n")

        return player[int(player_selected) - 1]

    def menu_select_tournament(self, tournament):
        tournament_selected = 0
        list_tournament = ""
        # le range fait max -1... donc pour le créer dynamiquement faut faire +1... logique -_-
        allowed_select_tournament_choice = range(1, len(tournament) + 1)
        for index, tournament_choice in enumerate(tournament):
            list_tournament += f"{index + 1} : tournois {tournament_choice['name']} " \
                               f"à {tournament_choice['location']} le {tournament_choice['date_start']} \n"

        while int(tournament_selected) not in allowed_select_tournament_choice:
            tournament_selected = input(f"Plusieurs tournois correspondent a votre recherche, "
                                        f"veuillez en selection un : \n{list_tournament}")

        return tournament[int(tournament_selected) - 1]

    def round_done(self, round_infos):
        return print(f"Le {round_infos.name} est terminé")

    def round_next(self, new_round):
        return print(f"Début du {new_round.name}")

    def all_match_done(self, tournament):
        return print(f"Tous les matchs du {tournament.name} sont terminés")

    def no_tournament(self):
        return print("Il n'y a pas de tournoi en cour")

    def no_tournament_done(self):
        return print("Il n'y a pas de tournoi a consulter")

    def player_infos(self, player):
        return print(player.get_player_infos())
