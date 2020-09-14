from Rect import *

class Word(object):  # Class definition

    def __init__(self, id, txt, coords):  # Object constructor
        self.id = id
        self.txt = txt
        self.coords = coords
        # self.color = color(0)
        self.type = ""

    def display(self):  # Display method
    
        if self.type == "naam":
            fill(255, 0, 0, 50)
            stroke(255, 0, 0)
        elif self.type == "beroep":
            fill(255, 255, 0, 50)
            stroke(255, 255, 0)
        elif self.type == "adres":
            fill(0, 255, 0, 50)
            stroke(0, 255, 0)
        elif self.type=="voornaam":
            fill(0,0,255,50)
            stroke(0,0,255)  
        else:
            noFill()
            stroke(0)         
        
        beginShape()
        for coord in self.coords:
            vertex(coord[0], coord[1])
        endShape(CLOSE)
        
    def updateBounds(self):
        self.bounds = Rect(self.coords[0][0],self.coords[0][1],
                           self.coords[2][0]-self.coords[0][0],self.coords[2][1]-self.coords[0][1])
        
        
