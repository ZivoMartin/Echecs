import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from random import randint



class Game():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chess")
        self.width = 560
        self.height = 560
        self.case_width = 56
        self.piece_width = 56
        self.actual_piece = {}
        self.dico_img = {
            "green": get_img(self.case_width-20, self.case_width-20, "green.jpg"),
            "blue" : get_img(self.case_width-20, self.case_width-20, "blue.jpg")
            }
        self.actual_click_img = []
        self.window.geometry(str(self.width) + "x" + str(self.height))
        self.cases = [None]*8
        for i in range(8):
            self.cases[i] = [None] * 8
            for j in range(8):
                self.cases[i][j] = {
                  "image" : "vide",
                  "piece" : "vide",
                  "color" : "vide",
                  "id" : "vide",
                  "blue" : False,
                  "green" : False,
                  "blue_img" : "vide"
             }
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()    
        self.canvas.bind("<Button-1>", lambda event: self.click_on_canvas(event))
        self.init_game()
        self.window.mainloop()
    
    def click_on_canvas(self, event):
        x, y = self.convert_clic_to_indice(event.x, event.y)
        if(x == "out" or (self.cases[x][y]["piece"] == "vide" and not self.cases[x][y]["green"])):
            return
        elif(self.cases[x][y]["blue"] or self.cases[x][y]["green"]):
            self.move_piece(self.actual_piece["x"], self.actual_piece["y"], x, y)
            self.reset_actual_click_img_tab()
            return
        self.reset_actual_click_img_tab()
        piece = self.cases[x][y]["piece"] 
        if(self.cases[x][y]["color"] == "white"):
            self.actual_piece = {"x": x, "y": y}
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
        
    

    def move_piece(self, x_move, y_move, new_x, new_y):
        if(self.cases[new_x][new_y]["blue"]):
            self.canvas.delete(self.cases[new_x][new_y]["image"])
            self.canvas.delete(self.cases[new_x][new_y]["blue_img"])
        piece = self.cases[x_move][y_move]["piece"]
        color = self.cases[x_move][y_move]["color"]
        id = self.cases[x_move][y_move]["id"]
        print(piece)
        print(self.cases[x_move][y_move])
        self.canvas.delete(self.cases[x_move][y_move]["image"])
        self.cases[new_x][new_y]["piece"] = piece
        self.cases[new_x][new_y]["color"] = color
        self.cases[new_x][new_y]["id"] = id
        self.cases[x_move][y_move] = {
                  "image" : "vide",
                  "piece" : "vide",
                  "color" : "vide",
                  "id" : "vide",
                  "blue" : False,
                  "green" : False,
                  "blue_img" : "vide"
             }
        self.cases[new_x][new_y]["image"] = self.canvas.create_image((new_x+1)*self.case_width, (new_y+1)*self.case_width, image = self.dico_img[piece+"_"+color+str(id)], anchor = "nw")
        
    def reset_actual_click_img_tab(self):
        for i in range(8):
            for j in range(8):
                if(self.cases[i][j]["green"]):
                    self.canvas.delete(self.cases[i][j]["green_img"])
                    self.cases[i][j]["green"] = False
                    self.cases[i][j]["image"] = "vide"
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
        if(x >= 0 and x <= 7 and y >= 0 and y <= 7):
            if(self.cases[x][y]["piece"] == "vide"):
                self.cases[x][y]["green_img"] = self.canvas.create_image((x+1)*self.case_width+10, (y+1)*self.case_width+10,image=self.dico_img["green"], anchor="nw"), 
                self.cases[x][y]["blue"] = False,
                self.cases[x][y]["green"] = True
                return "valid"
            elif(self.cases[x][y]["color"] == "black"):
                id = self.cases[x][y]["id"]
                piece = self.cases[x][y]["piece"]
                self.cases[x][y]["blue_img"] = self.canvas.create_image((x+1)*self.case_width+10, (y+1)*self.case_width+10,image=self.dico_img["blue"], anchor="nw")
                self.canvas.delete(self.cases[x][y]["image"])
                self.cases[x][y]["image"] = self.canvas.create_image((x+1)*self.case_width, (y+1)*self.case_width,image=self.dico_img[piece+"_black"+str(id)], anchor="nw")
                self.cases[x][y]["blue"] = True
                return "stop"
        return "unvalid"
        
    
    def click_on_king(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(i != 0 or j != 0):
                    self.init_possible_case(x+i, y+j)
    
    def click_on_pown(self, x, y):
        self.init_possible_case(x, y-1)
        if(y == 6):
            self.init_possible_case(x, 4)

    def click_on_knight(self, x, y):
        for i in range(-2, 3, 1):
            if(i != 0):
                self.init_possible_case(x+i, y + (3 - abs(i)))
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

    def init_game(self):
        self.echiquier = get_img(self.width, self.height, "echiquier.jpg")
        self.canvas.create_image(0, 0, image = self.echiquier, anchor = "nw")
       
        color_king = "black"
        path_color = "b"
        for i in range(2):
            self.init_piece(4, i*7, "king", color_king, "pieces/"+path_color+"K.png", 0)
            self.init_piece(3, i*7, "queen", color_king, "pieces/"+path_color+"Q.png", 0)
            color_king = "white"
            path_color = "w"
            self.init_piece(2+i*3, 0, "beshop", "black", "pieces/bB.png", i)
            self.init_piece(2+i*3, 7, "beshop", "white", "pieces/wB.png", i)

            self.init_piece(1+i*5, 0, "knight", "black", "pieces/bN.png", i)
            self.init_piece(1+i*5, 7, "knight", "white", "pieces/wN.png", i)

            self.init_piece(i*7, 0, "rook", "black", "pieces/bR.png", i)
            self.init_piece(i*7, 7, "rook", "white", "pieces/wR.png", i)
        
            
        for i in range(8):
            self.init_piece(i, 1, "pown", "black", "pieces/bP.png", i)
            self.init_piece(i, 6, "pown", "white", "pieces/wP.png", i)

        
    def init_piece(self, i, j, piece, color, path, id):
        self.dico_img[piece+"_"+color + str(id)] = get_img(self.piece_width, self.piece_width, path)
        self.cases[i][j] = {
            "image" : self.canvas.create_image((i+1)*self.case_width, (j+1)*self.case_width, image = self.dico_img[piece+"_"+color+str(id)], anchor = "nw"),
            "piece" : piece,
            "color" : color,
            "id" : id,
            "blue" : False,
            "green" : False,
            "blue_img" : "vide"
        }


def get_img(width, height, img_path):
        img = Image.open("C:/Users/zivom/OneDrive/Bureau/Perso/Echecs/" + img_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img
    

Game()