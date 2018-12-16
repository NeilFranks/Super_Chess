import pygame
from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
import sys
from sys import exit
from test.pyclbr_input import Other


import sets
from sets import Set

boardWidth = boardHeight = 800
squareCenters = []
DISPLAY = pygame.display.set_mode((boardWidth, boardHeight), 0, 32)
LIGHT_BROWN = (180, 140, 100)
DARK_BROWN = (100, 50, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def drawBoard(colors):
    inc = boardWidth / 8
    index = 1  # determine which color to use
    for column in range(8):
        for row in range(8):
            square = Rect(row * inc, column * inc, inc + 1, inc + 1)
            if square not in squareCenters:
                squareCenters.append(square)
            pygame.draw.rect(DISPLAY, colors[index], square)
            index = (index - 1) * -1
        index = (index - 1) * -1


def highlight(square, color):
    thickness = 5

    edgeLength = boardHeight / 8

    topLeft = ((square % 8) * edgeLength +
               thickness - 1, (square / 8) * edgeLength + thickness - 1)
    topRight = (topLeft[0] + edgeLength - 2 *
                thickness, topLeft[1])
    botLeft = (topLeft[0], topLeft[1] + edgeLength - 2 * thickness)
    botRight = (topRight[0], botLeft[1])

    # top
    pygame.draw.line(DISPLAY, color, topLeft, topRight, thickness)
    # left
    pygame.draw.line(DISPLAY, color, topLeft, botLeft, thickness)
    # right
    pygame.draw.line(DISPLAY, color, topRight, botRight, thickness)
    # bottom
    pygame.draw.line(DISPLAY, color, botLeft, botRight, thickness)


def getSquareCenter(coord):

    # round cursor to center of the square it's in
    eighth = boardHeight / 8
    sixteenth = boardHeight / 16

    return (coord[0] - (coord[0] % eighth) + sixteenth,
            coord[1] - (coord[1] % eighth) + sixteenth)


def getSquare(coord):

    eighth = boardHeight / 8

    # find the "number" square you clicked in
    square = coord[0] / eighth  # looking in x direction (row)
    # adjust square according to y
    square = square + 8 * (coord[1] / eighth)

    return square


def prune(ourSquare, otherSquare, moveList):
    # REMOVES HORIZONTAL, VERT, AND DIAGONAL MOVES THAT ARE UNREACHABLE

    distance = ourSquare - otherSquare

    # DIAGONALS
    if distance % 9 == 0:
        if distance / 9 < 0:  # blocking piece is on neg diagonal, RHS
            # remove pieces past blocking piece on neg diagonal
            tempIndex = otherSquare + 9
            while tempIndex <= 63:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex + 9

        else:  # blocking piece is on neg diagonal, LHS
            # remove pieces past blocking piece on neg diagonal
            tempIndex = otherSquare - 9
            while tempIndex >= 0:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex - 9

    if distance % 7 == 0:
        if distance / 7 < 0:  # blocking piece is on pos diagonal, LHS
            # remove pieces past blocking piece on neg diagonal
            tempIndex = otherSquare + 7
            while tempIndex <= 63:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex + 7

        else:  # blocking piece is on pos diagonal, LHS
            # remove pieces past blocking piece on neg diagonal
            tempIndex = otherSquare - 7
            while tempIndex >= 0:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex - 7

    # PERPENDICULARS
    if distance % 8 == 0:  # blocking piece is in same column
        if distance < 0:  # blocking piece is below
            # remove pieces below blocking piece
            tempIndex = otherSquare + 8
            while tempIndex <= 63:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex + 8

        else:  # blocking piece is above
            # remove pieces above blocking piece
            tempIndex = otherSquare - 8

            while tempIndex >= 0:  # lazy and ineffiecient but reliable
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex - 8

    # blocking piece is in same row (maybe, could be a knight move)
    if -7 <= distance < 0:  # would be on RHS
        if ourSquare / 8 == otherSquare / 8:  # check if really on the same row
            # remove pieces right of blocking piece
            tempIndex = otherSquare + 1
            while tempIndex / 8 == ourSquare / 8:
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex + 1

        else:
            # remove pieces left of blocking piece
            tempIndex = otherSquare - 1
            while tempIndex / 8 == ourSquare / 8:
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex - 1

    elif 0 < distance <= 7:  # would be on LHS
        if ourSquare / 8 == otherSquare / 8:  # check if really on the same row
            # remove pieces left of blocking piece
            tempIndex = otherSquare - 1
            while tempIndex / 8 == ourSquare / 8:
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex - 1

        else:
            # remove pieces right of blocking piece
            tempIndex = otherSquare + 1
            while tempIndex / 8 == ourSquare / 8:
                if tempIndex in moveList:
                    moveList.remove(tempIndex)
                tempIndex = tempIndex + 1

    return moveList


# move lists
# board rows start at squares 0,8,16,...,56
# board columns are squares with a difference divisible by 8


def pawnMoves(position, team, pawnMoved):
    moveSquares = Set([])

    if team == "White":  # white pawns can only move to lower number squares
        if pawnMoved:  # if pawn has been moved already, it can't move two squares ahead
            if position - 8 >= 0:
                moveSquares.add(position - 8)
        else:  # pawn can move one or two ahead
            if position - 8 >= 0:
                moveSquares.add(position - 8)
            if position - 16 >= 0:
                moveSquares.add(position - 16)
    else:  # black pawns can only move to higher number squares
        if pawnMoved:  # if pawn has been moved already, it can't move two squares ahead
            if position + 8 < 64:
                moveSquares.add(position + 8)
        else:  # pawn can move one or two ahead
            if position + 8 <= 64:
                moveSquares.add(position + 8)
            if position + 16 <= 64:
                moveSquares.add(position + 16)

    return moveSquares


def rookMoves(position):
    moveSquares = Set([])

    # add entire row into moveSquares
    rowStart = position - (position % 8)
    for i in range(8):
        moveSquares.add(rowStart + i)

    # add entire column into moveSquares
    colStart = position % 8
    for i in range(8):
        moveSquares.add(colStart + 8 * i)

    # cannot move to itself
    moveSquares.remove(position)

    return moveSquares


def knightMoves(position):
    moveSquares = Set([])

    # 1st row
    if position / 8 >= 2:  # if not in top 2 rows
        if position % 8 > 0:
            moveSquares.add(position - 17)
        if position % 8 < 7:
            moveSquares.add(position - 15)

    # 2nd row
    if position / 8 >= 1:  # if not in top row
        if position % 8 > 1:
            moveSquares.add(position - 10)
        if position % 8 < 6:
            moveSquares.add(position - 6)

    # 3rd row
    if position / 8 <= 7:  # if not in bottom row
        if position % 8 > 1:
            moveSquares.add(position + 6)
        if position % 8 < 6:
            moveSquares.add(position + 10)

    # 3rd row
    if position / 8 <= 6:  # if not in bottom 2 rows
        if position % 8 > 0:
            moveSquares.add(position + 15)
        if position % 8 < 7:
            moveSquares.add(position + 17)
    return moveSquares


def bishopMoves(position):
    moveSquares = Set([])

    # add neg sloping diagonal
    current = position
    # work backwards until you hit left edge (multiple of 8)
    while current % 8 != 0 and current - 9 >= 0 and current - 9 <= 63:
        moveSquares.add(current - 9)
        current = current - 9

    current = position
    # work forwards until you hit right edge (mod 8 = 7)
    while current % 8 != 7 and current + 9 >= 0 and current + 9 <= 63:
        moveSquares.add(current + 9)
        current = current + 9

    # add pos sloping diagonal
    current = position
    # work backwards until you hit left edge (multiple of 8)
    while current % 8 != 0 and current + 7 >= 0 and current + 7 <= 63:
        moveSquares.add(current + 7)
        current = current + 7

    current = position
    # work forwards until you hit right edge (mod 8 = 7)
    while current % 8 != 7 and current - 7 >= 0 and current - 7 <= 63:
        moveSquares.add(current - 7)
        current = current - 7

    return moveSquares


def kingMoves(position):
    moveSquares = Set([])

    moveSquares.add(position - 1)
    moveSquares.add(position + 7)
    moveSquares.add(position + 8)
    moveSquares.add(position + 9)
    moveSquares.add(position + 1)
    moveSquares.add(position - 7)
    moveSquares.add(position - 8)
    moveSquares.add(position - 9)

    # get rid of possibilities that aren't on the board
    for square in moveSquares:
        if square < 0 | square > 63:
            moveSquares.remove(square)

    return moveSquares


def queenMoves(position):
    moveSquares = Set([])

    for move in rookMoves(position):
        moveSquares.add(move)

    for move in bishopMoves(position):
        moveSquares.add(move)

    return moveSquares
