import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk



class Game():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chess")
        self.width = 560
        self.height = 560
        self.case_width = 56
        self.piece_width = 54
        self.img_piece = []
        self.window.geometry(str(self.width) + "x" + str(self.height))
        self.cases = [None]*8
        for i in range(8):
            self.cases[i] = [None] * 8
            for j in range(8):
                self.cases[i][j] = {
                  "image" : "vide",
                  "piece" : "vide"
             }
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()        
        self.init_game()
        self.window.mainloop()

    def init_game(self):
        self.echiquier = get_img(self.width, self.height, "echiquier2.jpg")
        self.canvas.create_image(0, 0, image = self.echiquier, anchor = "nw")

        color_king = "black"
        path_color = "b"
        for i in range(2):
            self.init_piece(4, i*7, color_king+"_king", "pieces/"+path_color+"K.png")
            self.init_piece(3, i*7, color_king+"_queen", "pieces/"+path_color+"Q.png")
            color_king = "white"
            path_color = "w"
            
            self.init_piece(2+i*3, 0, "black_beshop", "pieces/bB.png")
            self.init_piece(2+i*3, 7, "wight_beshop", "pieces/wB.png")

            self.init_piece(1+i*5, 0, "black_knight", "pieces/bN.png")
            self.init_piece(1+i*5, 7, "wight_knight", "pieces/wN.png")

            self.init_piece(i*7, 0, "black_rook", "pieces/bR.png")
            self.init_piece(i*7, 7, "wight_rook", "pieces/wR.png")
        
            
        for i in range(8):
            self.init_piece(i, 1, "black_pown", "pieces/bP.png")
            self.init_piece(i, 6, "wight_pown", "pieces/wP.png")

        
    def init_piece(self, i, j, piece, path):
        indice = len(self.img_piece)
        self.img_piece.append(get_img(self.piece_width, self.piece_width, path))
        self.cases[i][j] = {
            "image" : self.canvas.create_image((i+1)*self.case_width, (j+1)*self.case_width, image = self.img_piece[indice], anchor = "nw"),
            "piece" : piece
        }


def get_img(width, height, img_path):
        img = Image.open(img_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img
    

Game()