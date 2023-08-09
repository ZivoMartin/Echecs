from src.game import Game
from src.chess_gestion import ChessGestion
from src.ia import Ia
import os

class Main():
    def __init__(self):
        image_path = os.path.dirname(os.path.dirname(__file__)) + "/Echecs/images/"
        self.chess_gestion = ChessGestion()
        self.ia = Ia(self.chess_gestion)
        self.game = Game(self.chess_gestion, self.ia, image_path)

Main()