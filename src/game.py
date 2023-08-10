import tkinter as tk
from PIL import Image, ImageTk

class Game():

    def __init__(self, chess_gestion, ia, path_image):
        self.chess_gestion = chess_gestion
        self.ia = ia
        self.path_image = path_image
        self.window = tk.Tk()   
        self.window.title("Chess")
        self.width = 560
        self.height = 560
        self.case_width = 56
        self.piece_width = 56
        self.id_max = 2
        self.current_piece = {}
        self.player_turn = True
        self.player_can_big_castling = True
        self.player_can_short_castling = True
        self.dico_img = {
            "green": self.get_img(self.case_width-20, self.case_width-20, "green.jpg"),
            "blue" : self.get_img(self.case_width-20, self.case_width-20, "blue.jpg")
            }
        self.current_click_img = []
        self.window.geometry(str(self.width) + "x" + str(self.height))
        self.cases = [None]*8
        for i in range(8):
            self.cases[i] = [None] * 8
            for j in range(8):
                self.init_empty_case(i, j)
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()    
        self.canvas.bind("<Button-1>", lambda event: self.click_on_canvas(event))
        self.init_game()
        self.window.mainloop()
    
    def click_on_canvas(self, event):
        x, y = self.convert_clic_to_indice(event.x, event.y)
        if(x == "out" or (self.cases[x][y]["piece"] == "vide" and not self.cases[x][y]["green"]) or not self.player_turn):
            return
        elif(self.cases[x][y]["blue"] or self.cases[x][y]["green"]):
            self.move_piece(self.current_piece["x"], self.current_piece["y"], x, y)
            self.reset_current_click_img_tab()
            self.player_turn = False
            tab_game = self.get_tab_game()
            move_of_ia = self.ia.get_the_best_move(tab_game, {}, "black")
            if(move_of_ia == "loose" or move_of_ia == "draw"):
                return
            self.move_piece(move_of_ia["x1"], move_of_ia["y1"], move_of_ia["x2"], move_of_ia["y2"])
            self.player_turn = True
            return
        self.reset_current_click_img_tab()
        piece = self.cases[x][y]["piece"] 
        if(self.cases[x][y]["color"] == "white"):
            self.current_piece = {"x": x, "y": y}
            if(piece == "pown"):
                self.click_on_pown(x, y)
            elif(piece == "king"):
                self.click_on_king(x, y)
            elif(piece == "knight"):
                self.click_on_knight(x, y)
            elif(piece == "beshop"):
                self.click_on_beshop(x, y)
            elif(piece == "rook"):
                self.click_on_rook(x, y)
            elif(piece == "queen"):
                self.click_on_queen(x, y)
        
    

    def move_piece(self, x1, y1, x2, y2):
        color = self.cases[x1][y1]["color"]
        if(self.cases[x2][y2]["color"] != "vide" and self.cases[x2][y2]["color"] != color):
            self.canvas.delete(self.cases[x2][y2]["image"])
            self.canvas.delete(self.cases[x2][y2]["blue_img"])

        piece = self.cases[x1][y1]["piece"]
        color = self.cases[x1][y1]["color"]
        id = self.cases[x1][y1]["id"]

        self.canvas.delete(self.cases[x1][y1]["image"])
        self.cases[x2][y2]["piece"] = piece
        self.cases[x2][y2]["color"] = color
        self.cases[x2][y2]["id"] = id

        self.init_empty_case(x1, y1)
        self.cases[x2][y2]["image"] = self.canvas.create_image((x2+1)*self.case_width, (y2+1)*self.case_width, image = self.dico_img[piece+"_"+color+str(id)], anchor = "nw")
        self.test_special_move(piece, color, x2, y2, x1, y1)

    def test_special_move(self, piece, color, x2, y2, x1, y1):
        if(piece == "pown" and ((color == "white" and y2 == 0))):
            promo_frame = tk.Frame(self.canvas)
            buttons_promo = ["queen", "beshop", "knight", "rook"]
            for i in range(4):
                piece = buttons_promo[i]
                buttons_promo[i] = tk.Button(promo_frame, image=self.dico_img[buttons_promo[i]+"_white0"], command=lambda piece=piece: self.promote_pown(piece, x2, y2))
                buttons_promo[i].pack()
            self.promote_window = self.canvas.create_window((x2, y2), window=promo_frame, anchor="nw")
        elif(piece == "king" and color=="white" and (self.player_can_big_castling or self.player_can_short_castling)):
            self.player_can_big_castling = False
            self.player_can_short_castling = False
            d = x1-x2
            if(d == 2):
                self.move_piece(0, 7, 3, 7)
            elif(d == -2):
                self.move_piece(7, 7, 5, 7)
        elif(piece == "rook"):
            if(x1 == 7 and y1 == 7):
                self.player_can_short_castling = False
            elif(x1 == 0 and y1 == 7):
                self.player_can_big_castling = False


    def promote_pown(self, new_piece, x, y):
        id = str(self.id_max)
        if(new_piece == "queen"):
            self.dico_img["queen_white"+id] = self.get_img(self.piece_width, self.piece_width, "wQ.png")
        if(new_piece == "rook"):
            self.dico_img["rook_white"+id] = self.get_img(self.piece_width, self.piece_width, "wR.png")
        elif(new_piece == "beshop"):
            self.dico_img["beshop_white"+id] = self.get_img(self.piece_width, self.piece_width, "wB.png")
        elif(new_piece == "knight"):
            self.dico_img["knight_white"+id] = self.get_img(self.piece_width, self.piece_width, "wN.png")
        self.canvas.delete(self.cases[x][y]["image"])
        self.cases[x][y]["piece"] = new_piece
        self.cases[x][y]["id"] = self.id_max
        self.cases[x][y]["image"] = self.canvas.create_image((x+1)*self.case_width, (y+1)*self.case_width, image=self.dico_img[new_piece+"_white"+id], anchor="nw")
        self.canvas.delete(self.promote_window)
        self.id_max += 1


    def reset_current_click_img_tab(self):
        for i in range(8):
            for j in range(8):
                if(self.cases[i][j]["green"]):
                    self.canvas.delete(self.cases[i][j]["green_img"])
                    self.cases[i][j]["green"] = False
                elif(self.cases[i][j]["blue"]):
                    self.canvas.delete(self.cases[i][j]["blue_img"])
                    self.cases[i][j]["blue"] = False


    def convert_clic_to_indice(self, x, y):
        x = x//self.case_width
        y = y//self.case_width
        if(x == 0 or x == 10 or y == 0 or y == 10):
            return ("out", "out")
        else:
            return (x-1, y-1)
        
    def init_possible_case(self, x, y):
        if(x >= 0 and x <= 7 and y >= 0 and y <= 7 and self.move_is_legal(self.current_piece["x"], self.current_piece["y"], x, y)):
            if(self.cases[x][y]["piece"] == "vide"):
                self.cases[x][y]["green_img"] = self.canvas.create_image((x+1)*self.case_width+10, (y+1)*self.case_width+10,image=self.dico_img["green"], anchor="nw"), 
                self.cases[x][y]["blue"] = False
                self.cases[x][y]["green"] = True
                return "valid"
            else:
                id = self.cases[x][y]["id"]
                piece = self.cases[x][y]["piece"]
                self.cases[x][y]["blue_img"] = self.canvas.create_image((x+1)*self.case_width+10, (y+1)*self.case_width+10,image=self.dico_img["blue"], anchor="nw")
                self.canvas.delete(self.cases[x][y]["image"])
                self.cases[x][y]["image"] = self.canvas.create_image((x+1)*self.case_width, (y+1)*self.case_width,image=self.dico_img[piece+"_black"+str(id)], anchor="nw")
                self.cases[x][y]["blue"] = True
                return "stop"
        return "unvalid"
    
    def move_is_legal(self, x1, y1, x2, y2):
        if(self.cases[x1][y1]["color"] == self.cases[x2][y2]["color"]):
            return False
        temp_tab = self.get_tab_game() 
        return self.chess_gestion.move_is_legal(x1, y1, x2, y2, temp_tab, "white")

    def get_tab_game(self):
        tab = [None]*8
        for i in range(8):
            tab[i] = [None]*8
            for j in range(8):
                tab[i][j] = [self.cases[i][j]["piece"], self.cases[i][j]["color"]]
        return tab
    
    def click_on_king(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(i != 0 or j != 0):
                    self.init_possible_case(x+i, y+j)
        if(self.player_can_short_castling and self.cases[5][7]["piece"] == "vide" and self.cases[6][7]["piece"] == "vide"):
            self.init_possible_case(6, 7)
        elif(self.player_can_big_castling and self.cases[2][7]["piece"] == "vide" and self.cases[1][7]["piece"] == "vide" and self.cases[3][7]["piece"] == "vide"):
            self.init_possible_case(2, 7)

    def click_on_pown(self, x, y):
        if(self.cases[x][y-1]["piece"] == "vide"):
            self.init_possible_case(x, y-1)
        if(y == 6):
            self.init_possible_case(x, 4)
        if(x != 7 and self.cases[x+1][y-1]["piece"] != "vide"):
            self.init_possible_case(x+1, y-1)
        if(x != 0 and self.cases[x-1][y-1]["piece"] != "vide"):
            self.init_possible_case(x-1, y-1)

    def click_on_knight(self, x, y):
        for i in range(-2, 3):
            if(i != 0 and x+i<8 and x+i >= 0):
                if(y + (3 - abs(i)) < 8):
                    self.init_possible_case(x+i, y + (3 - abs(i)))
                if(y - (3 - abs(i)) >= 0):
                    self.init_possible_case(x+i, y - (3 - abs(i)))

    

    def click_on_rook(self, x, y):
        i = x+1
        while(self.init_possible_case(i, y) == "valid"):
            i += 1
        i = x-1
        while(self.init_possible_case(i, y) == "valid"):
            i -= 1
        i = y+1
        while(self.init_possible_case(x, i) == "valid"):
            i += 1
        i = y-1
        while(self.init_possible_case(x, i) == "valid"):
            i -= 1
    
    def click_on_beshop(self, x, y):
        i = x+1
        j = y + 1
        while(self.init_possible_case(i, j) == "valid"):
            i += 1
            j += 1
        i = x-1
        j = y - 1        
        while(self.init_possible_case(i, j) == "valid"):
            i -= 1
            j -= 1
        i = x-1
        j = y+1    
        while(self.init_possible_case(i, j) == "valid"):
            i -= 1
            j += 1
        i = x+1
        j = y-1    
        while(self.init_possible_case(i, j) == "valid"):
            i += 1
            j -= 1
        
    def click_on_queen(self, x, y):
        self.click_on_beshop(x, y)
        self.click_on_rook(x, y)

    def init_empty_case(self, i, j):
            self.cases[i][j] = {
                    "image" : "vide",
                    "piece" : "vide",
                    "color" : "vide",
                    "id" : "vide",
                    "blue" : False,
                    "green" : False,
                    "blue_img" : "vide",
                    "green_img" : "vide"
                }

    def init_game(self):
        self.echiquier = self.get_img(self.width, self.height, "echiquier.jpg")
        self.canvas.create_image(0, 0, image = self.echiquier, anchor = "nw")
       
        color_king = "black"
        path_color = "b"
        for i in range(2):
            self.init_piece(4, i*7, "king", color_king, path_color+"K.png", 0)
            self.init_piece(3, i*7, "queen", color_king,path_color+"Q.png", 0)
            color_king = "white"
            path_color = "w"
            self.init_piece(2+i*3, 0, "beshop", "black", "bB.png", i)
            self.init_piece(2+i*3, 7, "beshop", "white", "wB.png", i)

            self.init_piece(1+i*5, 0, "knight", "black", "bN.png", i)
            self.init_piece(1+i*5, 7, "knight", "white", "wN.png", i)

            self.init_piece(i*7, 0, "rook", "black", "bR.png", i)
            self.init_piece(i*7, 7, "rook", "white", "wR.png", i)
        
            
        for i in range(8):
            self.init_piece(i, 1, "pown", "black", "bP.png", i)
            self.init_piece(i, 6, "pown", "white", "wP.png", i)

        
    def init_piece(self, i, j, piece, color, path, id):
        self.dico_img[piece+"_"+color + str(id)] = self.get_img(self.piece_width, self.piece_width, path)
        self.cases[i][j] = {
            "image" : self.canvas.create_image((i+1)*self.case_width, (j+1)*self.case_width, image = self.dico_img[piece+"_"+color+str(id)], anchor = "nw"),
            "piece" : piece,
            "color" : color,
            "id" : id,
            "blue" : False,
            "green" : False,
            "blue_img" : "vide"
        }


    def get_img(self, width, height, img_path):
        img = Image.open(self.path_image + img_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img


