from src.game import Game
from src.chess_gestion import ChessGestion
from src.ia import Ia   
import os


def main():
        path = os.path.dirname(os.path.dirname(__file__)) + "/Echecs/"
        chess_gestion = ChessGestion()
        ia = Ia(chess_gestion)
        Game(chess_gestion, ia, path) 

#test
if __name__ == "__main__":
    main()
