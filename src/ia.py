
# Coder une fonction get_possible_move qui renvoie un tableau d'objet des tous les deplacements possible d'une
# pièce donnée sur un emplacement donné. De ce fait, dans la fonction get_the_best_move il suffit de parcourir 
# le plateau en passant le contenu de chaque case ainsi que les coordonés i, j à get_possible_move pour recevoir tous
# les coups possibles de la piece aux coordonés i, j. Reste plus qu'à parcourir ce tableau en appelant à chaque 
# itération la fonction new_move. 
# Pour ce qui est de la fonction count_the_possibles_moves_of_this_piece, on recupere notre tableau de coups possible,
# on ajoute à count la taille de ce tableau (pour les coups possible), ensuite ne reste plus qu'à le parcourir, 
# si on bouge sur une case occupée par un "white", on rajoute des point au compteur en fonction de la pièce mangée
# ainsi que de celle qui mange.

# Deuxieme idée, si on s'interesse à l'architecture du code, on remarque que ca pourrait etre
# une unique grande fonction, en gros, faire plusieurs fonction ne sert qu'a rendre le code plus lisible,
# ce qui signifie qu'il n'est absolument pas dérengant de lancer la recursivité à l'interieur de la fonction la plus
# profonde, soit count_the_possibles_moves_of_this_piece. Donc en modifiant un minimum l'architecture du programme,
# il n'est pas possible de mettre cases, data, scores, moves en attribut de la classe, il est possible sans probleme
# de lancer une recursivité profonde et plutôt optimisée.


class Ia:

    def __init__(self, chess_gestion):
        self.chess_gestion = chess_gestion
        

    def get_the_best_move(self, cases, data):
        self.data = data
        self.cases = cases
        self.scores = []
        self.moves = []

        for i in range(8):
            for j in range(8):
                if(cases[i][j][1] == "black"):
                    possible_moves = self.get_possible_moves(i, j, cases)
                    size = len(possible_moves)
                    for k in range(size):
                        the_move = possible_moves[k]
                        if(self.chess_gestion.move_is_legal(the_move["x1"], the_move["y1"], the_move["x2"], the_move["y2"], cases, "black")):
                            print("new move with ", cases[i][j][0])
                            self.new_move(possible_moves[k])
        print(self.scores)
        max_score = max(self.scores)
        size = len(self.scores)
        for i in range(size):
            if(self.scores[i] == max_score):
                return self.moves[i]
            
            
    def new_move(self, move):
        self.scores.append(self.score_of_the_move(move["x1"], move["y1"], move["x2"], move["y2"], 1))
        self.moves.append(self.get_move_object(move["x1"], move["y1"], move["x2"], move["y2"]))

    def get_move_object(self, x1, y1, x2, y2):
        return {
            "x1": x1,
            "x2": x2,
            "y1": y1,
            "y2": y2
        }

    def score_of_the_move(self, x1, y1, x2, y2, diviseur):
        temp_tab = [None]*8
        for i in range(8):
            temp_tab[i] = [None]*8
            for j in range(8):
                temp_tab[i][j] = [self.cases[i][j][0], self.cases[i][j][1]]
        score = 0
        if(temp_tab[x2][y2][1] == "white"):
            score += self.get_val(temp_tab[x2][y2][0])*40
        temp_tab[x2][y2] = temp_tab[x1][y1]
        temp_tab[x1][y1] = ["vide", "vide"]
        score += self.count_possible_move(temp_tab)
        return score/diviseur

    def count_possible_move(self, tab):
        count = 0
        for i in range(8):
            for j in range(8):
                if(tab[i][j][1] == "black"):
                    count += self.count_the_possibles_moves_of_this_piece(tab, i, j) 
        return count
    
    def count_the_possibles_moves_of_this_piece(self, tab, x, y):
        factor = 3
        if(tab[x][y][0] == "pown"):
            factor = 7
        elif(tab[x][y][0] == "rook" or tab[x][y][0] == "queen" or tab[x][y][0] == "king"):
            factor = 1
        count = 0
        possible_moves = self.get_possible_moves(x, y, tab)
        size = len(possible_moves)
        count += size
        for i in range(size):
            this_case = tab[possible_moves[i]["x2"]][possible_moves[i]["y2"]]
            if(this_case[1] == "white"):
                count += factor*self.get_val(this_case[0])/2
        return count


    def get_possible_moves(self, x, y, cases):
        piece = cases[x][y][0]
        possible_moves = []
        if(piece == "pown"):
            if(y<7):
                if(cases[x][y+1][0] == "vide"):
                    possible_moves.append(self.get_move_object(x, y, x, y+1))
                    if(y == 1 and cases[x][3][0] == "vide"):
                        possible_moves.append(self.get_move_object(x, 1, x, 3))
                if(x<7 and cases[x+1][y+1][1] == "white"):
                    possible_moves.append(self.get_move_object(x, y, x+1, y+1))
                if(x>0 and cases[x-1][y+1][1] == "white"):
                    possible_moves.append(self.get_move_object(x, y, x-1, y+1))
        elif(piece ==  "knight"):
            for i in range(-2, 3):
                xi = x+i
                if(i != 0 and xi<8 and xi >= 0):
                    if(y + (3 - abs(i)) < 8):
                        possible_moves.append(self.get_move_object(x, y, xi, y + (3 - abs(i))))
                    if(y - (3 - abs(i)) >= 0):
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
                    if((i != 0 or j != 0) and self.coord_valid(x+i, y+j)):
                        possible_moves.append(self.get_move_object(x, y, x+i, y+j))
        return possible_moves
    

    def get_val(self, piece):
        if(piece == "pown"):
            return 1
        elif(piece == "beshop" or piece == "knight"):
            return 3
        elif(piece == "rook"):
            return 6
        else:
            return 9
    
    def coord_valid(self, i, j):
        return (i>=0 and j>=0 and i<8 and j<8)
    
    def get_diag_move(self, cases, possible_moves, x, y):
        i = x+1
        j = y+1
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, j))
            i += 1
            j += 1
        if(self.coord_valid(i, j) and cases[i][j][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x-1
        j = y - 1        
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, j))
            i -= 1
            j -= 1
        if(self.coord_valid(i, j) and cases[i][j][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x-1
        j = y+1    
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, j))
            i -= 1
            j += 1
        if(self.coord_valid(i, j) and cases[i][j][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, j))
        i = x+1
        j = y-1    
        while(self.coord_valid(i, j) and cases[i][j][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, j))
            i += 1
            j -= 1
        if(self.coord_valid(i, j) and cases[i][j][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, j))
        
    def get_line_move(self, cases, possible_moves, x, y):
        i = x+1
        while(self.coord_valid(i, y) and cases[i][y][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, y))
            i += 1
        if(self.coord_valid(i, y) and cases[i][y][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, y))
        i = x-1
        while(self.coord_valid(i, y) and cases[i][y][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, i, y))
            i -= 1
        if(self.coord_valid(i, y) and cases[i][y][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, i, y))
        i = y+1
        while(self.coord_valid(x, i) and cases[x][i][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, x, i))
            i += 1
        if(self.coord_valid(x, i) and cases[x][i][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, x, i))
        i = y-1
        while(self.coord_valid(x, i) and cases[x][i][0] == "vide"):
            possible_moves.append(self.get_move_object(x, y, x, i))
            i -= 1
        if(self.coord_valid(x, i) and cases[x][i][1] == "white"):
            possible_moves.append(self.get_move_object(x, y, x, i))
        return possible_moves