from src.game import Game
from src.chess_gestion import ChessGestion
from src.ia import Ia
import os


def main():
        image_path = os.path.dirname(os.path.dirname(__file__)) + "/Echecs/images/"
        chess_gestion = ChessGestion()
        ia = Ia(chess_gestion)
        Game(chess_gestion, ia, image_path)


if __name__ == "__main__":
    main()
