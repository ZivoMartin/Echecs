
class Ia:

    def __init__(self, chess_gestion):
        self.chess_gestion = chess_gestion
        

    def get_the_best_move(self, bad_tab, data, color, repeat):
        cases = [None]*8
        for i in range(8):
            cases[i] = [None]*8
            for j in range(8):
                cases[i][j] = [bad_tab[i][j][0], bad_tab[i][j][1]]
        scores = []
        moves = []
        self.color = color
        
        if(self.color == "black"):
            self.no_color = "white"
        else:
            self.no_color = "black"
        count = 0
        for i in range(8):
            for j in range(8):
                if(cases[i][j][1] == self.color):
                    possible_moves = self.get_possible_moves(i, j, cases)
                    size = len(possible_moves)
                    count += size
                    for k in range(size):
                        self.new_move(possible_moves[k], moves, scores, cases, repeat)
                        if(cases[possible_moves[k]["x2"]][possible_moves[k]["y2"]][1] == self.no_color):
                            count += self.get_val(cases[possible_moves[k]["x2"]][possible_moves[k]["y2"]][0])
        size = len(scores)
        if(size > 0): 
            max_score = max(scores)
            for i in range(size):
                if(scores[i] == max_score):
                    if(repeat == 1):
                        return (moves[i], scores[i])
                    else:
                        return (moves[i], scores[i]+count)
        elif(not self.chess_gestion.move_is_legal(0, 0, 0, 0, cases, self.color)):
            return ("loose", "loose")
        else:
            return ("draw", "draw")
        

    def new_move(self, move, moves, scores, cases, repeat):
        scores.append(self.score_of_the_move(cases, move["x1"], move["y1"], move["x2"], move["y2"], repeat))
        moves.append(self.get_move_object(move["x1"], move["y1"], move["x2"], move["y2"]))

    def get_move_object(self, x1, y1, x2, y2):
        return {
            "x1": x1,
            "x2": x2,
            "y1": y1,
            "y2": y2
        }

    def score_of_the_move(self, cases, x1, y1, x2, y2, repeat):
        temp_tab = [None]*8
        for i in range(8):
            temp_tab[i] = [None]*8
            for j in range(8):
                temp_tab[i][j] = [cases[i][j][0], cases[i][j][1]]
        score = 0
        if(temp_tab[x2][y2][1] == self.no_color):
            if(self.color == "black"):
                score += self.get_val(temp_tab[x2][y2][0])*40
            if(self.color == "white"):
                score += self.get_val(temp_tab[x2][y2][0])*40
        temp_tab[x2][y2] = [temp_tab[x1][y1][0], temp_tab[x1][y1][1]]
        temp_tab[x1][y1] = ["vide", "vide"]
        if(repeat < 2):
            temp = self.color
            self.color = self.no_color
            self.no_color = temp
            move, second_score = self.get_the_best_move(temp_tab, {}, self.color, repeat + 1)
            if(second_score == "loose"):
                score += 10000000
            elif(second_score != "draw"):
                score -= second_score
        return score

    def count_possible_move(self, tab):
        count = 0
        for i in range(8):
            for j in range(8):
                if(tab[i][j][1] == self.color):
                    count += self.count_the_possibles_moves_of_this_piece(tab, i, j) 
        return count//5
    
    def count_the_possibles_moves_of_this_piece(self, tab, x, y):
        factor = 2
        if(tab[x][y][0] == "pown"):
            factor = 3
        elif(tab[x][y][0] == "rook" or tab[x][y][0] == "queen" or tab[x][y][0] == "king"):
            factor = 1
        count = 0
        possible_moves = self.get_possible_moves(x, y, tab)
        size = len(possible_moves)
        count += size
        for i in range(size):
            this_case = tab[possible_moves[i]["x2"]][possible_moves[i]["y2"]]
            if(this_case[1] == self.no_color):
                count += factor*self.get_val(this_case[0])/2
            if(tab[x][y][0] == "pown"):
                count += abs(y-possible_moves[i]["y2"])
        return count


    def get_possible_moves(self, x, y, cases):
        piece = cases[x][y][0]
        possible_moves = []
        if(piece == "pown"):
            if(self.color == "black" and y<7):
                    if(cases[x][y+1][0] == "vide" and self.chess_gestion.move_is_legal(x, y, x, y+1, cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, x, y+1))
                        if(y == 1 and cases[x][3][0] == "vide" and self.chess_gestion.move_is_legal(x, 1, x, 3, cases, self.color)):
                            possible_moves.append(self.get_move_object(x, 1, x, 3))
                    if(x<7 and cases[x+1][y+1][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x+1, y+1, cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, x+1, y+1))
                    if(x>0 and cases[x-1][y+1][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x-1, y+1, cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, x-1, y+1))
            elif(self.color == "white" and y>0):
                if(cases[x][y-1][0] == "vide" and self.chess_gestion.move_is_legal(x, y, x, y-1, cases, self.color)):
                    possible_moves.append(self.get_move_object(x, y, x, y-1))
                    if(y == 6 and cases[x][4][0] == "vide" and self.chess_gestion.move_is_legal(x, 6, x, 4, cases, self.color)):
                        possible_moves.append(self.get_move_object(x, 6, x, 4))
                if(x<7 and cases[x+1][y-1][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x+1, y-1, cases, self.color)):
                    possible_moves.append(self.get_move_object(x, y, x+1, y-1))
                if(x>0 and cases[x-1][y-1][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x-1, y-1, cases, self.color)):
                    possible_moves.append(self.get_move_object(x, y, x-1, y-1))

        elif(piece ==  "knight"):
            for i in range(-2, 3):
                xi = x+i
                if(i != 0 and xi<8 and xi >= 0):
                    if(y + (3 - abs(i)) < 8 and cases[xi][y + (3 - abs(i))][1] != self.color and self.chess_gestion.move_is_legal(x, y, xi, y + (3 - abs(i)), cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, xi, y + (3 - abs(i))))
                    if(y - (3 - abs(i)) >= 0 and cases[xi][y - (3 - abs(i))][1] != self.color and self.chess_gestion.move_is_legal(x, y, xi, y - (3 - abs(i)), cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, xi, y - (3 - abs(i))))
        elif(piece == "beshop"):
            self.get_diag_move(cases, possible_moves, x, y)
        elif(piece == "rook"):
            self.get_line_move(cases, possible_moves, x, y)
        elif(piece == "queen"):
            self.get_diag_move(cases, possible_moves, x, y)
            self.get_line_move(cases, possible_moves, x, y)
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if((i != 0 or j != 0) and self.coord_valid(x+i, y+j) and cases[x+i][y+j][1] != self.color and self.chess_gestion.move_is_legal(x, y, x+i, y+j, cases, self.color)):
                        possible_moves.append(self.get_move_object(x, y, x+i, y+j))
        return possible_moves
    

    def get_val(self, piece):
        if(piece == "pown"):
            return 1
        elif(piece == "beshop" or piece == "knight"):
            return 3
        elif(piece == "rook"):
            return 6
        elif(piece == "king" or piece == "queen"):
            return 9
        else:
            return 0
    
    def coord_valid(self, i, j):
        return (i>=0 and j>=0 and i<8 and j<8)
    
    def get_diag_move(self, cases, possible_moves, x, y):
        i = x+1
        j = y+1
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, j))
            i += 1
            j += 1
        if(self.coord_valid(i, j) and cases[i][j][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x-1
        j = y - 1        
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, j))
            i -= 1
            j -= 1
        if(self.coord_valid(i, j) and cases[i][j][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x-1
        j = y+1    
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, j))
            i -= 1
            j += 1
        if(self.coord_valid(i, j) and cases[i][j][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x+1
        j = y-1    
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, j))
            i += 1
            j -= 1
        if(self.coord_valid(i, j) and cases[i][j][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, j, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, j))
        
    def get_line_move(self, cases, possible_moves, x, y):
        i = x+1
        while(self.coord_valid(i, y) and cases[i][y][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, y, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, y))
            i += 1
        if(self.coord_valid(i, y) and cases[i][y][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, y, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, y))
        i = x-1
        while(self.coord_valid(i, y) and cases[i][y][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, i, y, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, i, y))
            i -= 1
        if(self.coord_valid(i, y) and cases[i][y][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, i, y, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, i, y))
        i = y+1
        while(self.coord_valid(x, i) and cases[x][i][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, x, i, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, x, i))
            i += 1
        if(self.coord_valid(x, i) and cases[x][i][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x, i, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, x, i))
        i = y-1
        while(self.coord_valid(x, i) and cases[x][i][0] == "vide"):
            if(self.chess_gestion.move_is_legal(x, y, x, i, cases, self.color)):
                possible_moves.append(self.get_move_object(x, y, x, i))
            i -= 1
        if(self.coord_valid(x, i) and cases[x][i][1] == self.no_color and self.chess_gestion.move_is_legal(x, y, x, i, cases, self.color)):
            possible_moves.append(self.get_move_object(x, y, x, i))
        return possible_moves