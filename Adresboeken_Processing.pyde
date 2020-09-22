add_library('Viewport')
from Word import *

dragging = False
downX = 0
downY = 0
type = ""
achternamen = {}
straten = {}
achternamen_blacklist = {}
beroepen = {}
viewport = None
basename = "MMUTRA01_001427001_00015_master"
# basename = "MMUTRA01_001491001_01000_access"
out = None

def setup():
    size(1700, 800)
    textAlign(LEFT)
    textFont(loadFont("SansSerif-26.vlw"))
    global img, words, viewport, out
    words = []
    out = createWriter("tmp.txt")

    lines = loadStrings("achternamen.txt")
    for l in lines:
        achternamen[trim(l.lower())] = l
    lines = loadStrings("achternamen-blacklist.txt")
    for l in lines:
        achternamen_blacklist[trim(l.lower())] = l

    lines = loadStrings("straten.txt")
    for l in lines:
        straten[trim(l.lower())] = l

    lines = loadStrings("beroepen.txt")
    for l in lines:
        beroepen[trim(l.lower())] = l

    img = loadImage(basename + ".jpg")
    viewport = Viewport(this, 0, 0, width, height, img.width, img.height)

    global xml
    xml = loadXML(basename + ".xml")
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
                        newWord.txt = unicode


def draw():
    global dragging, downX, downY

    background(50)
    # viewport.begin();

    image(img, 0, 0)
    noFill()
    stroke(0, 255, 0)
    # rect(0, 0, mouseX, mouseY)

    for word in words:
        word.display()

    if dragging:
        stroke(0, 255, 255)
        noFill()
        strokeWeight(1)
        rect(downX, downY, mouseX - downX, mouseY - downY)

    fill(255, 0, 0)
    for word in words:
        word.updateBounds()
        if (word.bounds.intersects(Rect(mouseX, mouseY, 2, 2))):
            text(trim(word.txt), mouseX, mouseY)

    # viewport.end()

def mousePressed():
    global downX, downY
    downX = mouseX
    downY = mouseY

def mouseDragged():
    global dragging, downX, downY, type

    dragging = True

    for word in words:
        word.updateBounds()
        if (word.bounds.intersects(Rect(downX, downY, mouseX - downX, mouseY - downY))):
            word.type = type


def mouseReleased():
    global dragging
    dragging = False

def keyPressed():
    global type

    if key == 'n':
        type = "naam"
    elif key == 'b':
        type = "beroep"
    elif (key == 'a'):
        type = "adres"

    elif key == 'v':
        for word in words:
            if word.txt.strip().startswith("(") or word.txt.strip().endswith(")"):
                word.type = "voornaam"

    elif key == 'f':
        for word in words:
            # out.println(trim(word.txt))

            if trim(word.txt.lower()).strip(",") in achternamen:
                # println(trim(word.txt))
                word.type = "naam"
                # word.txt = "_" + trim(word.txt.lower()) 
      # not trim(word.txt.lower()) in achternamen_blacklist):

    elif key == 's':
        for word in words:
            if trim(word.txt.lower()).strip(",").strip(".") in straten or trim(word.txt).endswith("str.") or trim(word.txt).endswith("weg") or trim(word.txt).endswith("gr."):
                word.type = "adres"

    elif key == 'B':
        for word in words:
            if (word.txt.lower().find("schilder")>-1):
                println(trim(word.txt.lower()) + "  -->  " + trim(word.txt.lower()).strip(",").strip("."))
                
            if trim(word.txt.lower()).strip(",").strip(".") in beroepen:
                word.type = "beroep"

    elif key==' ':
        out.flush()
        out.close()
