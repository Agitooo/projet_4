class Player:
    """Player."""

    def __init__(self, **kwargs):
        """Has a lastname, firstname, birthdate, civility and rank."""
        self.player_id = kwargs.get("player_id")
        self.lastname = kwargs.get("lastname")
        self.firstname = kwargs.get("firstname")
        self.birthdate = kwargs.get("birthdate")
        self.civility = kwargs.get("civility")
        self.rank = kwargs.get("rank")
        self.score = 0

    def set_score(self, score):
        self.score = score

    @staticmethod
    def get_civility(civility):
        if civility == "1":
            return {"civ": "Mme.", "genre": "ée"}
        else:
            return {"civ": "Mr.", "genre": "é"}

    def get_player_infos(self):
        civility = self.get_civility(self.civility)
        return f"{civility['civ']} {self.lastname} {self.firstname} class{civility['genre']} " \
               f"{self.rank} n{civility['genre']} le {self.birthdate}"

    def get_player_name(self):
        return f"{self.lastname} {self.firstname}"

    def __str__(self):
        """Used in print."""
        return f"player_id: {self.player_id}, lastname: {self.lastname}, firstname: {self.firstname}, " \
               f"birthdate: {self.birthdate}, civility: {self.civility}, rank: {self.rank}"

    def __repr__(self):
        """Used in print."""
        return str(self)
