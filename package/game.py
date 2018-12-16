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
    teamIdx = 1  # flips at start of while loop so white starts
    pieceSelected = False

    pygame.init()

    drawBoard((DARK_BROWN, LIGHT_BROWN))

    for piece in Pieces:
        piece.draw(DISPLAY)
    pygame.display.flip()

    while True:

        if pieceSelected:
            teamIdx = (teamIdx - 1) * -1
            pieceSelected = False  # alternate between 1 and 0

        team = teams[teamIdx]

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()

                centerOfSquare = getSquareCenter(cursor)
                square = getSquare(cursor)

                # find piece if you clicked on one
                for piece in Pieces:
                    if piece.team == team and piece.coordinates == centerOfSquare:
                        pieceSelected = True

                        # clear lines
                        drawBoard((DARK_BROWN, LIGHT_BROWN))

                        for newPiece in Pieces:
                            newPiece.draw(DISPLAY)
                        pygame.display.flip()

                        moveList = piece.movelist(square)

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
        pygame.time.wait(10)


main()
