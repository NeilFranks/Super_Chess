import pygame
from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP

import sys
from sys import exit

from pieces import *

import gc
from gc import *
from Tkconstants import CURRENT
from package import pieces
from test.test_builtin import Squares


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


def main():
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

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()

                centerOfSquare = getSquareCenter(cursor)
                selectedSquare = getSquare(cursor)

                # check if square is in movelist of selected piece
                if pieceSelected:
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

                                                        # indicate you didnt
                                                        # move
                                                        moved = False
                                                    else:
                                                        # make the move and remove the
                                                        # enermy piece
                                                        Pieces.remove(piece)
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
                if not moved:
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
