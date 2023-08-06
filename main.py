from src.game import Game
from src.chess_gestion import ChessGestion
import os

class Main():
    def __init__(self):
        image_path = os.path.dirname(os.path.dirname(__file__)) + "/Echecs/images/"
        self.chess_gestion = ChessGestion()
        self.game = Game(self.chess_gestion, image_path)

Main()