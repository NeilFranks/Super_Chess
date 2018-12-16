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


def main():
    gc.enable()

    teams = ['White', 'Black']
    teamIdx = 0  # white starts
    pieceSelected = False

    pygame.init()

    drawBoard((DARK_BROWN, LIGHT_BROWN))

    for piece in Pieces:
        piece.draw(DISPLAY)
    pygame.display.flip()

    while True:

        team = teams[teamIdx]

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()

                centerOfSquare = getSquareCenter(cursor)
                selectedSquare = getSquare(cursor)

                # find piece if you clicked on one
                if not pieceSelected:
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
                else:
                    # check if square is in movelist of selected piece
                    if selectedSquare in moveList:

                        moved = False

                        # check if this square has a piece on it
                        for piece in Pieces:
                            if selectedSquare == getSquare(piece.coordinates) and not moved:
                                if piece.team == team:  # you can merge
                                    currentPiece.mergePiece(
                                        squareCenters[selectedSquare], piece)
                                    Pieces.remove(piece)

                                    # reset pieceSelected
                                    pieceSelected = False

                                else:  # you can take
                                    currentPiece.updatePiece(
                                        squareCenters[selectedSquare])
                                    Pieces.remove(piece)

                                    # reset pieceSelected
                                    pieceSelected = False

                                # indicate you moved
                                moved = True

                        if not moved:
                            currentPiece.updatePiece(
                                squareCenters[selectedSquare])

                            # reset pieceSelected
                            pieceSelected = False

                            # indicate you moved
                            moved = True

                        # clear lines
                        drawBoard((DARK_BROWN, LIGHT_BROWN))

                        for newPiece in Pieces:
                            newPiece.draw(DISPLAY)
                        pygame.display.flip()

                        # its the other team's turn
                        teamIdx = (teamIdx - 1) * -1
                        pieceSelected = False  # alternate between 1 and 0

        pygame.display.flip()
        pygame.time.wait(10)


main()
