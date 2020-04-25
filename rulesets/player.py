class Player:
    def __init__(self, name):
        self.name = name
        self.current_match = None

        self.match_history = []
        self.valid = True
    
    def update_match(self, result):
        self.match_history.append(self.current_match)
        self.current_match = None

        if not result:
            self.valid = False

    def set_current_match(self, next_match):
        self.current_match = next_match
