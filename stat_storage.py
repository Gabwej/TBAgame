

class RunStats:
    def __init__(self):
        self.total_damage = 0
        self.total_healing = 0
        self.battles_won = 0
        self.events_seen = 0

    def reset(self):
        self.total_damage = 0
        self.total_healing = 0
        self.battles_won = 0
        self.events_seen = 0