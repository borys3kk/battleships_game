class ServerData:
    def __init__(self, shot = None, game_won = None, hit = False):
        self._shot = shot
        self._game_won = game_won
        self._hit = hit
        self._game_finished = False
        
    
    def set_shot(self, new_shot):
        self._shot = new_shot
    
    def get_shot(self):
        return self._shot

    def set_game_won(self, game_won):
        self._game_won = game_won

    def get_game_won(self):
        return self._game_won
    
    def set_hit(self, hit):
        self._hit = hit
    
    def get_hit(self):
        return self._hit

    def set_game_finished(self, game_finished):
        self._game_finished = game_finished
    
    def get_game_finished(self):
        return self._game_finished