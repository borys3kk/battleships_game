from wrapper import Wrapper
class Ship(Wrapper):
    def __init__(self):
        super().__init__()
    
    def load_image(self, path, size:tuple((int, int)), rotate=False):
        return super().load_image(path, size, rotate)