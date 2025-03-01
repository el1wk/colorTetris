from tkinter import *
import random
import copy

#creates empty box for screensize
def playTetris(rows = 30, cols = 10):
    cellSize = 20
    margin = 25
    width = (margin*2) + (cellSize*cols)
    height = (margin*2) + (cellSize*rows)
    run(width, height)

def init(data):
    data.timeIncrease = 0
    data.timerDelay = 400 + data.timeIncrease
    data.cellSize = 20
    data.margin = 25
    data.rows = 30
    data.cols = 10
    data.colorPicker = random.randint(0, 3) #picks new color palette each level
    print (data.colorPicker)
    if data.colorPicker == 0:
        data.emptyColor = "LightYellow2"
        data.tetrisPieceColor =["forest green","olive drab", "medium sea green"]
    if data.colorPicker == 1:
        data.emptyColor = "azure2"
        data.tetrisPieceColor =["deep sky blue","DodgerBlue2", "turquoise2"]
    if data.colorPicker == 2:
        data.emptyColor = "whitesmoke"
        data.tetrisPieceColor =["gold2","chocolate1", "orange"]
    if data.colorPicker == 3:
        data.emptyColor = "lavender blush"
        data.tetrisPieceColor =["pink1","RosyBrown2", "PaleVioletRed1"]
    data.board = [([data.emptyColor]*data.cols)for row in range(data.rows)]
    data.iPiece = [[  True,  True,  True,  True ]]
    data.jPiece = [[  True, False, False ],[  True,  True,  True ]]
    data.lPiece = [[ False, False,  True ],[  True,  True,  True ]]
    data.oPiece = [[  True,  True ],[  True,  True ]]
    data.sPiece = [[ False,  True,  True ],[  True,  True, False ]]
    data.tPiece = [[ False,  True, False ],[  True,  True,  True ]]
    data.zPiece = [[  True,  True, False ],[ False,  True,  True ]]
    data.uPiece = [[  True,  False, True ],[ True,  True,  True ]]
    data.tetrisPieces = [data.iPiece,data.jPiece,data.lPiece,data.uPiece,
                         data.oPiece,data.sPiece,data.tPiece,data.zPiece]
    newfP(data)
    data.isGameOver = False
    data.score = 0

def newfP(data): #generates new piece from list of tetris pieces
    randomIndex = random.randint(0, len(data.tetrisPieces)-1)
    randomIndexColor = random.randint(0, len(data.tetrisPieceColor)-1)
    data.fP = data.tetrisPieces[randomIndex] #fallingPiece
    data.fPCor = data.tetrisPieceColor[randomIndexColor] #fallingPieceColor
    data.fPR = 0 #fallingPieceRow
    data.fPC = data.cols//2 #fallingPieceCol
    data.fPC = data.fPC - (data.fPC//2)

def movefP(data, drow, dcol): #moves piece depending on keys pressed
    data.fPC += dcol
    data.fPR += drow
    if not (fPIsLegalBound(data)):
        data.fPC -= dcol
        data.fPR -= drow
        return False
    if not (fPIsLegalColor(data)):
        data.fPC -= dcol
        data.fPR -= drow
        return False
    return True

def rotatefP(data): #rotates piece counterclockwise when the up key is pressed
    calculateOldNew(data)
    for i in range (len(data.fP)):
        for j in range (len(data.fP[0])):
            data.newfP[(len(data.fP[0]))-j-1][i]= data.fP[i][j]
    data.fP = data.newfP
    data.fPR = data.newCenterRow
    data.fPC = data.newCenterCol
    if (fPIsLegalBound(data) and fPIsLegalColor(data)):
        pass
    else:
        data.fP = oldfP
        data.fPR = oldFallingRow
        data.fPC = oldFallingCol

def calculateOldNew(data):
    #calculate new row center
    data.centerRow = data.fPR + data.fPR//2
    data.oldCenterRow = data.fPR + len(data.fP)//2
    data.newCenterRow = (data.fPR
    + len(data.fP)//2)- len(data.fP[0])//2
    #calculate new col center
    data.centerCol = data.fPC + data.fPC//2
    data.oldCenterCol = data.fPC + len(data.fP[0])//2
    data.newCenterCol = (data.fPC
    + len(data.fP[0])//2)-len(data.fP)//2
    #old data
    oldfP = data.fP
    oldFallingRow = data.fPR
    oldFallingCol = data.fPC
    #new data
    data.newfPR = oldFallingCol
    data.newfPC = oldFallingRow
    data.newfP = [([0]*len(data.fP))for row in range (len(data.fP[0]))]

def fPIsLegalBound(data): #returns false if piece is out of bounds
    for row in range (len(data.fP)):
        for col in range (len(data.fP[0])):
            if (data.fP[row][col]):
                if (row+data.fPR == data.rows): return False
                if (row+data.fPR == -1): return False
                if (col+data.fPC == -1): return False
                if (col+data.fPC == data.cols): return False
    return True

def fPIsLegalColor(data): #returns false if piece is falling into taken spot
    for row in range (len(data.fP)):
        for col in range (len(data.fP[0])):
            if (data.fP[row][col]):
                if ((data.board[row+data.fPR]
                               [col+data.fPC])
                               != data.emptyColor):return False
    return True

def placefP(data): #places falling piece into board
    for rows in range (len(data.fP)):
        for cols in range (len(data.fP[0])):
            if data.fP[rows][cols]:
                data.board[rows+data.fPR][cols+data.fPC]= data.fPCor
    removeFullRows(data)

def removeFullRows(data): #adds to score and removes bottom row if it's full
    for i in range (len(data.board)):
        if data.emptyColor not in data.board[i]:
            for j in range (len(data.board[i])):
                data.board[i][j] = data.emptyColor
                data.board[i][j]= data.board[i-1][j-1]
                data.score+=1
                data.timeIncrease -=100

#################################

def drawBoard(canvas, data):
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            drawCell(canvas, data, i, j, data.board[i][j])

def drawfP(canvas, data):
    for rows in range (len(data.fP)):
        for cols in range (len(data.fP[0])):
            if data.fP[rows][cols]:drawCell(canvas,data,
                                             rows+data.fPR,
                                             cols+data.fPC,
                                             data.fPCor)

def drawCell(canvas, data, rows, cols, color):
    left = data.margin+data.cellSize*cols
    top = data.margin+data.cellSize*rows
    right = left + data.cellSize
    bottom = top + data.cellSize
    if data.isGameOver:
        canvas.create_rectangle(left, top, right, bottom, fill = "white")
        canvas.create_text(data.width/2, data.margin/2, text = "GAME OVER", font = "Helvetica 20")
    if not data.isGameOver:
        canvas.create_rectangle(left, top, right, bottom, fill = color, outline = color)
        canvas.create_text(data.width/2, data.margin/2, text = data.score, font = "Helvetica 20 bold")

def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawfP(canvas, data)

#####################################################

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event,data):
    # use event.char and event.keysym
    if not data.isGameOver:
        if event.keysym == "Up": rotatefP(data)
        elif event.keysym == "Left": movefP(data,0,-1)
        elif event.keysym == "Right": movefP(data,0,+1)
        elif event.keysym == "Down": movefP(data,+1,0)
        elif event.keysym == "r": init(data)
        else: newfP(data)
    else:
        if event.keysym == "r": init(data)

def timerFired(data):
    if not (movefP(data, 0, 0)):
        data.isGameOver = True

    if not data.isGameOver:
        movefP(data,+1,0)
        if not (movefP(data,+1,0)):
            placefP(data)
            newfP(data)

####################################
# use the run function as-is
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

playTetris()