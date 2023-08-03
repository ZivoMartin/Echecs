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
        self.piece_width = 56
        self.img_piece = []
        self.actual_click_img = []
        self.window.geometry(str(self.width) + "x" + str(self.height))
        self.green = get_img(self.case_width-20, self.case_width-20, "green.jpg")
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
        self.canvas.bind("<Button-1>", lambda event: self.click_on_canvas(event))
        self.init_game()
        self.window.mainloop()
    
    def click_on_canvas(self, event):
        self.reset_actual_click_img_tab()
        x, y = self.convert_clic_to_indice(event.x, event.y)
        if(x == "out" or self.cases[x][y]["piece"] == "vide"):
            return
        piece = self.cases[x][y]["piece"]
        if(self.cases[x][y]["color"] == "white"):
            if(piece == "pown"):
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y-1)*self.case_width+10, image=self.green, anchor="nw"))
            elif(piece=="king"):
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y-1)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y-1)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y-1)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y)*self.case_width+10, image=self.green, anchor="nw"))
                self.actual_click_img.append(self.canvas.create_image((x+1)*self.case_width+10, (y-1)*self.case_width+10, image=self.green, anchor="nw"))

    def reset_actual_click_img_tab(self):
        size = len(self.actual_click_img)
        for i in range(size):
            self.canvas.delete(self.actual_click_img[i])
        self.actual_click_img = []


    def convert_clic_to_indice(self, x, y):
        x = x//self.case_width
        y = y//self.case_width
        if(x == 0 or x == 10 or y == 0 or y == 10):
            return ("out", "out")
        else:
            return (x-1, y-1)


    def init_game(self):
        self.echiquier = get_img(self.width, self.height, "echiquier.jpg")
        self.canvas.create_image(0, 0, image = self.echiquier, anchor = "nw")

        color_king = "black"
        path_color = "b"
        for i in range(2):
            self.init_piece(4, i*7, "king", color_king, "pieces/"+path_color+"K.png")
            self.init_piece(3, i*7, "queen", color_king, "pieces/"+path_color+"Q.png")
            color_king = "white"
            path_color = "w"
            self.init_piece(2+i*3, 0, "beshop", "black", "pieces/bB.png")
            self.init_piece(2+i*3, 7, "beshop", "white", "pieces/wB.png")

            self.init_piece(1+i*5, 0, "knight", "black", "pieces/bN.png")
            self.init_piece(1+i*5, 7, "knight", "white", "pieces/wN.png")

            self.init_piece(i*7, 0, "rook", "black", "pieces/bR.png")
            self.init_piece(i*7, 7, "rook", "white", "pieces/wR.png")
        
            
        for i in range(8):
            self.init_piece(i, 1, "pown", "black", "pieces/bP.png")
            self.init_piece(i, 6, "pown", "white", "pieces/wP.png")

        
    def init_piece(self, i, j, piece, color, path):
        indice = len(self.img_piece)
        self.img_piece.append(get_img(self.piece_width, self.piece_width, path))
        self.cases[i][j] = {
            "image" : self.canvas.create_image((i+1)*self.case_width, (j+1)*self.case_width, image = self.img_piece[indice], anchor = "nw"),
            "piece" : piece,
            "color" : color
        }


def get_img(width, height, img_path):
        img = Image.open(img_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img
    

Game()