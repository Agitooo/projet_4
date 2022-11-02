class Report:
    """Report."""

    def __init__(self, player, tournament, rounds, match):
        self.player = player
        self.tournament = tournament
        self.rounds = rounds
        self.match = match

    def __repr__(self):
        """Used in print."""
        return str(self)
