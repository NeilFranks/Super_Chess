import pygame
from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.constants import MOUSEBUTTONDOWN, KEYDOWN

import sys
from sys import exit

from pieces import *

import gc
from gc import *
from Tkconstants import CURRENT
from package import pieces
from test.test_builtin import Squares

# will be an array of arrays, each subarray being the board at a given turn
boards = []
boardIdx = -1

# will indicate promote menu is open
promote = False

# will indicate square to promote to
promoteSquare = -1  # initialize to arbitrary number


def saveBoard():
    global boardIdx
    global boards

    if boardIdx < len(boards) - 1:  # you are on a past board
        # start from end of boards and remove all stored boards
        # up until boardIdx
        for i in range(len(boards) - 1, boardIdx,  -1):
            boards.remove(boards[i])

    newBoard = []

    for piece in Pieces:
        newBoard.append(ChessPiece(
            piece.imageName, squareCenters[getSquare(piece.coordinates)], piece.team, piece.piece))

    boards.append(newBoard)
    boardIdx = boardIdx + 1


def restoreBoard(board):
    # clear lines
    drawBoard((DARK_BROWN, LIGHT_BROWN))

    for newPiece in board:
        newPiece.draw(DISPLAY)

    pygame.display.flip()


def clearLines():
    # clear lines
    drawBoard((DARK_BROWN, LIGHT_BROWN))

    for newPiece in Pieces:
        newPiece.draw(DISPLAY)
    pygame.display.flip()


def flash(square, color):

    clearLines()
    highlight(square, color)
    pygame.display.flip()

    pygame.time.wait(100)


def promotePiece():
    global promote
    promote = True

    menu = Rect(0.3 * boardHeight, 0.4 * boardHeight, .4 *
                boardHeight, .2 * boardHeight)
    pygame.draw.rect(DISPLAY, GRAY, menu)
    # get images
    qImage = pygame.image.load(os.path.join(image_path, "bq.png"))
    qImage = pygame.transform.scale(
        qImage, (boardWidth / 5, boardWidth / 5))
    qRect = pygame.Rect(qImage.get_rect())
    qRect.topleft = (.3 * boardHeight, .4 * boardHeight)

    nImage = pygame.image.load(os.path.join(image_path, "bn.png"))
    nImage = pygame.transform.scale(
        nImage, (boardWidth / 5, boardWidth / 5))
    nRect = pygame.Rect(qImage.get_rect())
    nRect.topleft = (.5 * boardHeight, .4 * boardHeight)

    DISPLAY.blit(qImage, qRect.topleft)
    DISPLAY.blit(nImage, nRect.topleft)

    pygame.display.flip()


def main():

    global promote
    promote = False
    global promoteSquare
    promoteSquare = -1
    global Pieces

    saveBoard()

    gc.enable()

    teams = ['White', 'Black']
    teamIdx = 0  # white starts
    pieceSelected = False

    currentPiece = Pieces[0]  # arbitrary initialization
    moveList = Set([])

    pygame.init()

    drawBoard((DARK_BROWN, LIGHT_BROWN))

    for piece in Pieces:
        piece.draw(DISPLAY)
    pygame.display.flip()

    while True:

        team = teams[teamIdx]

        moved = False
        # check for pawns who made it to the end
        for piece in Pieces:
            if piece.pawn and not (piece.rook or piece.knight or piece.bishop or piece.queen or piece.king):
                square = getSquare(piece.coordinates)
                if piece.team == "White" and square / 8 == 0:
                    promoteSquare = square
                    promotePiece()
                    Pieces.remove(piece)

                elif piece.team == "Black" and square / 8 == 7:
                    promoteSquare = square
                    promotePiece()
                    Pieces.remove(piece)

        # check for check on your team
        for checkPiece in Pieces:
            if checkPiece.king:
                if checkPiece.team == team:
                    if checkPiece.inCheck():  # you're putting yourself in check
                        highlight(getSquare(checkPiece.coordinates), PURPLE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    global boardIdx
                    if(boardIdx > 0):
                        boardIdx = boardIdx - 1

                        # its the other team's turn
                        # alternate between 1 and 0
                        teamIdx = (teamIdx - 1) * -1

                    restoreBoard(boards[boardIdx])

                elif event.key == pygame.K_RIGHT:
                    global boardIdx
                    if(boardIdx < len(boards) - 1):
                        boardIdx = boardIdx + 1

                        # its the other team's turn
                        # alternate between 1 and 0
                        teamIdx = (teamIdx - 1) * -1

                    restoreBoard(boards[boardIdx])

            elif event.type == MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()

                centerOfSquare = getSquareCenter(cursor)
                selectedSquare = getSquare(cursor)

                if promote:  # must choose queen or knight from menu
                    if (0.3 * boardHeight <= cursor[0] <= 0.5 * boardHeight) and (0.4 * boardHeight <= cursor[1] <= 0.6 * boardHeight):
                        choose = 'Queen'
                    elif (0.5 * boardHeight <= cursor[0] <= 0.7 * boardHeight) and (0.4 * boardHeight <= cursor[1] <= 0.6 * boardHeight):
                        choose = 'Knight'

                    if promoteSquare < 8:  # in top row, so white was there
                        if choose == 'Queen':
                            Pieces.append(ChessPiece(
                                'wq.png', squareCenters[promoteSquare], 'White', 'q'))
                        elif choose == 'Knight':
                            Pieces.append(ChessPiece(
                                'wn.png', squareCenters[promoteSquare], 'White', 'n'))

                        promote = False
                        promoteSquare = -1

                    elif promoteSquare > 55:  # in bottom row, so black was there
                        if choose == 'Queen':
                            Pieces.append(ChessPiece(
                                'bq.png', squareCenters[promoteSquare], 'Black', 'q'))
                        elif choose == 'Knight':
                            Pieces.append(ChessPiece(
                                'bn.png', squareCenters[promoteSquare], 'Black', 'n'))

                        promote = False
                        promoteSquare = -1

                    clearLines()

                # check if square is in movelist of selected piece
                elif pieceSelected:

                    if selectedSquare in moveList:

                        # check if this square has a piece on it
                        for piece in Pieces:
                            if selectedSquare == getSquare(piece.coordinates) and not moved:

                                if piece.team == team:  # you can merge

                                    # find kings and check if they're in check
                                    if not currentPiece.king:

                                        Pieces.remove(currentPiece)
                                        moved = True

                                        for checkPiece in Pieces:
                                            if checkPiece.king:
                                                if checkPiece.team == team:
                                                    if checkPiece.inCheck():  # you're putting yourself in check

                                                        flash(
                                                            getSquare(checkPiece.coordinates), PURPLE)
                                                        # undo removal of
                                                        # currentPiece
                                                        Pieces.append(
                                                            currentPiece)

                                                        # indicate you didnt
                                                        # move
                                                        moved = False
                                                    else:
                                                        # make the move
                                                        piece.mergePiece(
                                                            squareCenters[selectedSquare], currentPiece)
                                    else:  # you're trying to move your king into another one of your pieces
                                        # remember what square currentPiece is
                                        # on
                                        currentSquare = getSquare(
                                            currentPiece.coordinates)

                                        # move your king to the new square
                                        currentPiece.updatePiece(
                                            squareCenters[selectedSquare])
                                        moved = True

                                        # check if king is in check on new
                                        # square
                                        if currentPiece.inCheck():
                                            flash(
                                                getSquare(currentPiece.coordinates), PURPLE)

                                            # undo move
                                            currentPiece.updatePiece(
                                                squareCenters[currentSquare])

                                            # indicate you didnt move
                                            moved = False

                                        else:
                                            # make the move
                                            Pieces.remove(currentPiece)
                                            piece.mergePiece(
                                                squareCenters[selectedSquare], currentPiece)

                                else:  # you can take

                                    # find kings and check if they're in check
                                    if not currentPiece.king:
                                        # remember what square currentPiece is
                                        # on
                                        currentSquare = getSquare(
                                            currentPiece.coordinates)

                                        # move currentPiece
                                        currentPiece.updatePiece(
                                            squareCenters[selectedSquare])

                                        # remove the enemy piece
                                        Pieces.remove(piece)

                                        moved = True

                                        for checkPiece in Pieces:
                                            if checkPiece.king:
                                                if checkPiece.team == team:

                                                    if checkPiece.inCheck():  # you're putting yourself in check

                                                        flash(
                                                            getSquare(checkPiece.coordinates), PURPLE)

                                                        # undo movement of
                                                        # currentPiece
                                                        currentPiece.updatePiece(
                                                            squareCenters[currentSquare])

                                                        # undo removal of piece
                                                        Pieces.append(piece)

                                                        # indicate you didnt
                                                        # move
                                                        moved = False
                                    else:  # you're trying to move your king into an enemy
                                        # remember what square currentPiece is
                                        # on
                                        currentSquare = getSquare(
                                            currentPiece.coordinates)

                                        # move your king to the new square
                                        currentPiece.updatePiece(
                                            squareCenters[selectedSquare])
                                        moved = True

                                        # check if king is in check on new
                                        # square
                                        if currentPiece.inCheck():
                                            flash(
                                                getSquare(currentPiece.coordinates), PURPLE)

                                            # undo move
                                            currentPiece.updatePiece(
                                                squareCenters[currentSquare])

                                            # indicate you didnt move
                                            moved = False

                                        else:
                                            # make the move and remove the
                                            # enermy piece
                                            Pieces.remove(piece)

                        if not moved:  # selectedSquare didnt have a piece on it. move to empty square
                            # find kings and check if they're in check
                            if not currentPiece.king:
                                # remember what square currentPiece is on
                                currentSquare = getSquare(
                                    currentPiece.coordinates)

                                # move currentPiece
                                currentPiece.updatePiece(
                                    squareCenters[selectedSquare])

                                moved = True

                                for checkPiece in Pieces:
                                    if checkPiece.king:
                                        if checkPiece.team == team:
                                            if checkPiece.inCheck():  # you're putting yourself in check
                                                flash(
                                                    getSquare(checkPiece.coordinates), PURPLE)

                                                # undo movement of currentPiece
                                                currentPiece.updatePiece(
                                                    squareCenters[currentSquare])

                                                # indicate you didn't move
                                                moved = False

                            else:  # you're trying to move your king into an empty space
                                # remember what square currentPiece is
                                # on
                                currentSquare = getSquare(
                                    currentPiece.coordinates)

                                # move your king to the new square
                                currentPiece.updatePiece(
                                    squareCenters[selectedSquare])
                                moved = True

                                # check if king is in check on new
                                # square
                                if currentPiece.inCheck():
                                    flash(
                                        selectedSquare, PURPLE)

                                    # undo move
                                    currentPiece.updatePiece(
                                        squareCenters[currentSquare])

                                    # indicate you didnt move
                                    moved = False

                        if moved:
                            # register a pawn move
                            # CAN CHANGE: should it count as pawn move if a merged piece moves in a
                            # way a pawn cant?
                            if currentPiece.pawn:
                                diff = currentSquare - selectedSquare
                                if currentPiece.team == "White":
                                    if diff == 8 or diff == 16:  # thats a pawn move
                                        currentPiece.pawnMoved = True
                                else:
                                    if diff == -8 or diff == -16:  # thats a pawn move
                                        currentPiece.pawnMoved = True

                            saveBoard()

                            clearLines()

                            # its the other team's turn
                            # alternate between 1 and 0
                            teamIdx = (teamIdx - 1) * -1

                            # reset pieceSelected
                            pieceSelected = False

                    else:  # square is not in move list. deselect piece
                        clearLines()

                        # reset pieceSelected
                        pieceSelected = False

                # find piece if you clicked on one
                if not moved and not promote:
                    global boardIdx
                    if boardIdx < len(boards) - 1:  # you are on a past board

                        # copy old board into current board
                        newBoard = []
                        for piece in boards[boardIdx]:
                            newBoard.append(ChessPiece(
                                piece.imageName, squareCenters[getSquare(piece.coordinates)], piece.team, piece.piece))

                        Pieces = newBoard

                    clearLines()

                    for piece in Pieces:
                        if piece.team == team and piece.coordinates == centerOfSquare:
                            pieceSelected = True
                            currentPiece = piece

                            moveList = piece.movelist(selectedSquare)

                            # highlight squares you can move to
                            for square in moveList:
                                highlight(square, GREEN)

                            # find squares where you can either take or merge
                            for piece in Pieces:
                                square = getSquare(piece.coordinates)
                                if square in moveList:
                                    if piece.team == team:  # you can merge
                                        highlight(square, BLUE)
                                    else:  # you can take
                                        highlight(square, RED)

                            pygame.display.flip()

        pygame.display.flip()
        pygame.time.wait(10)


main()
