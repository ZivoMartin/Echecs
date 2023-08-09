class ChessGestion:

    def __init__(self):
        self.tab_cases = []
        self.color = "white"
        self.no_color = "black"
    
    def move_is_legal(self, x1, y1, x2, y2, tab_cases, color):
        x2_y2 = tab_cases[x1][y1]
        tab_cases[x2][y2] = tab_cases[x1][y1]
        tab_cases[x1][y1] = ["vide, vide"]
        self.color = color
        if(self.color == "white"):
            self.no_color = "black"
        else:
            self.no_color = "white"
        self.tab_cases = tab_cases
        coord_queen, coord_rooks, coord_beshops, coord_king = self.init_coords()
        xk = coord_king["x"]
        yk = coord_king["y"]
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = xk+i
                y = yk+j
                if(x>= 0 and y >= 0 and x<8 and y<8 and self.tab_cases[x][y][1] != self.color and (self.tab_cases[x][y][0] == "king" or (abs(i)+abs(j) == 2 and self.tab_cases[x][y][0] == "pown"))):
                    if(self.tab_cases[x][y][0] == "pown" and self.color == "white" and y<yk):
                        self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                        return False
                    elif(self.tab_cases[x][y][0] == "pown" and self.color == "black" and y>yk):
                        self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                        return False
                    elif(self.tab_cases[x][y][0] == "king"):
                        self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                        return False
        for i in range(-2, 3):
            x = xk + i
            y1 = yk + (3-abs(i))
            y2 = yk - (3-abs(i))
            if(i != 0 and x>=0 and x<8 and ((y1>=0 and y1<8 and self.tab_cases[x][y1]==["knight", self.no_color]) or (y2 >=0 and y2<8 and self.tab_cases[x][y2]==["knight", self.no_color]))):
                self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                return False
        for i in range(coord_rooks["i"]):
            x1 = coord_rooks["rook_"+str(i)]["x"]
            y1 = coord_rooks["rook_"+str(i)]["y"]
            if((x1 == xk or y1 == yk) and not self.line_obstacle(x1, y1, xk, yk)):
                self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                return False
        for i in range(coord_beshops["i"]):
            x1 = coord_beshops["beshop_"+str(i)]["x"]
            y1 = coord_beshops["beshop_"+str(i)]["y"]
            if((abs(x1 - xk) == abs(y1 - yk)) and not self.diag_obstacle(x1, y1, xk, yk)):
                self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                return False
        for i in range(coord_queen["i"]):
            x1 = coord_queen["queen_"+str(i)]["x"]
            y1 = coord_queen["queen_"+str(i)]["y"]
            if(((abs(x1 - xk) == abs(y1 - yk)) and not self.diag_obstacle(x1, y1, xk, yk)) or ((x1 == xk or y1 == yk) and not self.line_obstacle(x1, y1, xk, yk))):
                self.reset_change(self, x2_y2, x1, y1, x2, y2, tab_cases)
                return False
        return True

    def diag_obstacle(self, x1, y1, x2, y2):
        if(y1 >  y2):
            if(x1 > x2):
                for i in range(1, x1-x2):
                    if(self.tab_cases[x2+i][y2+i][0] != "vide"):
                        return True
            else:
                for i in range(1, x2-x1):
                    if(self.tab_cases[x2-i][y2+i][0] != "vide"):
                        return True
        else:
            if(x1 > x2):
                for i in range(1, x1-x2):
                    if(self.tab_cases[x2+i][y2-i][0] != "vide"):
                        return True
            else:
                for i in range(1, x2-x1):
                    if(self.tab_cases[x2-i][y2-i][0] != "vide"):
                        return True
        return False

    def reset_change(self, x2_y2, x1, y1, x2, y2, tab):
        tab[x1][y1] = tab[x2][y2]
        tab[x2][y2] = x2_y2

    def line_obstacle(self, x1, y1, x2, y2):
        if(x1 == x2):
            max_y = max(y1, y2)
            min_y = min(y1, y2) 
            while(max_y > min_y):
                min_y += 1
                if(self.tab_cases[x1][min_y][0] != "vide" and max_y != min_y):
                    return True
        else:
            max_x = max(x1, x2)
            min_x = min(x1, x2) 
            while(max_x > min_x):
                min_x += 1
                if(self.tab_cases[min_x][y1][0] != "vide" and max_x != min_x):
                    return True
        return False
    
    def init_coords(self):
        coord_rooks = {"i": 0}
        coord_beshops = {"i": 0}
        coord_queen = {"i": 0}
        coord_king = {}
        for i in range(8):
            for j in range(8):
                if(self.tab_cases[i][j][0] == "queen" and self.tab_cases[i][j][1] != self.color):
                    coord_queen["queen_"+str(coord_queen["i"])] = {
                        "x" : i,
                        "y" : j
                    }
                    coord_queen["i"] += 1
                elif(self.tab_cases[i][j][0] == "rook" and self.tab_cases[i][j][1] != self.color):
                    coord_rooks["rook_"+str(coord_rooks["i"])] = {
                        "x" : i,
                        "y" : j
                    }
                    coord_rooks["i"] += 1
                elif(self.tab_cases[i][j][0] == "beshop" and self.tab_cases[i][j][1] != self.color):
                    coord_beshops["beshop_"+str(coord_beshops["i"])] = {
                        "x" : i,
                        "y" : j
                    }
                    coord_beshops["i"] += 1
                elif(self.tab_cases[i][j][0] == "king" and self.tab_cases[i][j][1] == self.color):
                    coord_king["x"] = i
                    coord_king["y"] = j
        return (coord_queen, coord_rooks, coord_beshops, coord_king)