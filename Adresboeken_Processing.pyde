from Word import *

dragging = False
downX = 0 
downY = 0
type = ""

def setup():
    size(1700, 800)
    global img
    global words
    words = []
    img = loadImage("MMUTRA01_001491001_01000_access.jpg")
    global xml
    xml = loadXML("MMUTRA01_001491001_01000_access.xml")
    for page in xml.getChildren("Page"):
        w = page.getString("imageWidth")
        h = page.getString("imageHeight")
        print w, h
        for textRegion in page.getChildren("TextRegion"):
            textRegionId = textRegion.getString("id")
            for textLine in textRegion.getChildren("TextLine"):
                textLineId = textLine.getString("id")
                for word in textLine.getChildren("Word"):
                    wordId = word.getString("id")
                    newWord = Word(id, "", [])
                    words.append(newWord)

                    for coord in word.getChildren("Coords"):
                        points = coord.getString("points")
                        points = points.split(" ")
                        for p in points:
                            x, y = map(int, p.split(","))
                            newWord.coords.append([x, y])

                    for textEquiv in word.getChildren("TextEquiv"):
                        unicode = textEquiv.getContent("Unicode")
                        newWord.txt = unicode;
    

def draw():
    global dragging, downX, downY
    
    background(50)
    image(img, 0, 0)
    noFill()
    stroke(0, 255, 0)
    # rect(0, 0, mouseX, mouseY)

    for word in words:
        word.display()
        
    if dragging:
        stroke(0,255,255)
        noFill()
        strokeWeight(1)
        rect(downX,downY,mouseX-downX,mouseY-downY)

def mousePressed():
    global downX, downY
    downX = mouseX
    downY = mouseY
            
def mouseDragged():
    global dragging, downX, downY, type
    
    dragging = True
        
    for word in words:
        word.updateBounds()
        if (word.bounds.intersects(Rect(downX,downY,mouseX-downX, mouseY-downY))):
            word.type = type
            
   
def mouseReleased():
    global dragging
    dragging = False
    
def keyPressed():
    global type;
    
    if key=='n':
        type = "naam"
    elif key=='b':
        type = "beroep"
    elif (key=='a'):
        type = "adres"
    elif key=='/':
       for word in words:
           if word.txt.strip().startswith("(") or word.txt.strip().endswith(")"):
               word.type = "voornaam"
        
        
