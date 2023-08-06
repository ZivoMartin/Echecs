class ChessGestion:

    def __init__(self):
        pass
    
    def move_is_possible(self, x1, y1, x2, y2, tab_cases, color, king_coord):
        return True
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(tab_cases[i][j][1] != color and (tab_cases[i][j][0] == "king" or (abs(i)+abs(j) == 2 and tab_cases[i][j][0] == "pown"))):
                    return False
        for i in range(-2, 3):
            if(i != 0 and (tab_cases[king_coord["x"]+i][king_coord["y"] +(3-abs(i))][0]=="knight" or tab_cases[king_coord["x"]+i][king_coord["y"] -(3-abs(i))][0]=="knight")):
                return False
        i = king_coord["x"] + 1
        while(tab_cases[i+1][king_coord["y"]][0] == "vide" and i < 8):
            i += 1
            if(tab_cases[i+1][king_coord["y"]][0] == "rook" or tab_cases[i+1][king_coord["y"]][0] == "queen"):
                return False
        i = king_coord["x"]-1
        while(self.init_possible_case(i, y) == "valid"):
            i -= 1
        i = y+1
        while(self.init_possible_case(x, i) == "valid"):
            i += 1
        i = y-1
        while(self.init_possible_case(x, i) == "valid"):
            i -= 1
    