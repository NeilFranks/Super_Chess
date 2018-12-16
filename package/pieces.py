from work import *
import os
from test.pyclbr_input import Other


# directory information
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')


class ChessPiece(pygame.sprite.Sprite):

    def __init__(self, image, position, team, piece):
        pygame.sprite.Sprite.__init__(self)

        # set characteristics
        self.pawn = False
        self.rook = False
        self.knight = False
        self.bishop = False
        self.king = False
        self.queen = False
        self.pawnMoved = False  # for only allowing pawns to move 2 spaces for their first move
        self.team = team

        # get image
        self.image = pygame.image.load(os.path.join(image_path, image))
        self.image = pygame.transform.scale(
            self.image, (boardWidth / 8, boardWidth / 8))
        self.square = position
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = position.topleft
        self.rect.center = position.center
        self.coordinates = position.center

        # set initial piece
        if piece == 'p':
            self.pawn = True
        elif piece == 'r':
            self.rook = True
        elif piece == 'n':
            self.knight = True
        elif piece == 'b':
            self.bishop = True
        elif piece == 'k':
            self.king = True
        elif piece == 'q':
            self.queen = True

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def updatePiece(self, position):
        # remember where you came from
        oldSquare = getSquare(self.coordinates)

        # update
        self.square = position
        self.rect.center = position.center
        self.coordinates = position.center

        newSquare = getSquare(self.coordinates)

        # register a pawn move
        # CAN CHANGE: should it count as pawn move if a merged piece moves in a
        # way a pawn cant?
        if self.pawn:
            diff = oldSquare - newSquare
            if self.team == "White":
                if diff == 8 or diff == 16:  # thats a pawn move
                    self.pawnMoved = True
            else:
                if diff == -8 or diff == -16:  # thats a pawn move
                    self.pawnMoved = True

    def mergePiece(self, position, otherPiece):
        if self.pawn and otherPiece.pawn:  # both pieces have pawn characteristics
            # if at least one hasnt moved, this one can move twice
            self.pawnMoved = self.pawnMoved and otherPiece.pawnMoved
        elif otherPiece.pawnMoved:  # only the other piece has pawn characteristics
            self.pawnMoved = otherPiece.pawnMoved

        self.pawn = self.pawn or otherPiece.pawn
        self.rook = self.rook or otherPiece.rook
        self.knight = self.knight or otherPiece.knight
        self.bishop = self.bishop or otherPiece.bishop
        self.king = self.king or otherPiece.king
        self.queen = self.queen or otherPiece.queen

        # fill in name of image fil
        name = ''
        if self.team == 'White':
            name = 'w'
        else:
            name = 'b'

        if self.pawn:
            name = name + 'p'

        if self.rook:
            name = name + 'r'

        if self.bishop:
            name = name + 'b'

        if self.knight:
            name = name + 'n'

        if self.king:
            name = name + 'k'

        if self.queen:
            name = name + 'q'

        name = name + '.png'

        # get image
        self.image = pygame.image.load(os.path.join(image_path, name))
        self.image = pygame.transform.scale(
            self.image, (boardWidth / 8, boardWidth / 8))
        self.square = position
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = position.topleft
        self.rect.center = position.center
        self.coordinates = position.center

    def inCheck(self):
        if self.king:
            # check if it's in check

            # check if it can see a pawn
            for piece in Pieces:
                if piece.team != self.team and piece.pawn:
                    if self.team == 'White':  # enemy pawn must be black
                        kingSquare = getSquare(self.coordinates)
                        pawnSquare = getSquare(piece.coordinates)
                        if kingSquare / 8 == 1 + pawnSquare / 8:  # black pawn must be on row right above white king
                            diff = kingSquare - pawnSquare
                            if diff == 7 or diff == 9:  # black pawn must be in taking position
                                return True
                    else:  # enemy pawn must be white; king is black
                        kingSquare = getSquare(self.coordinates)
                        pawnSquare = getSquare(piece.coordinates)
                        if kingSquare / 8 == pawnSquare / 8 - 1:  # white pawn must be on row right below black king
                            diff = kingSquare - pawnSquare
                            if diff == -7 or diff == -9:  # white pawn must be in taking position
                                return True

            # check if it can see an enemy rook with rookMoves
            canSee = rookMoves(getSquare(self.coordinates))

            # trim canSee with pieceBlock()
            canSee = self.pieceBlock(getSquare(self.coordinates), canSee)

            for piece in Pieces:
                if piece.team != self.team and getSquare(piece.coordinates) in canSee and piece.rook:
                    return True

            # check if it can see an enemy knight with knightMoves
            canSee = knightMoves(getSquare(self.coordinates))

            # trim canSee with pieceBlock()
            canSee = self.pieceBlock(getSquare(self.coordinates), canSee)

            for piece in Pieces:
                if piece.team != self.team and getSquare(piece.coordinates) in canSee and piece.knight:
                    return True

            # check if it can see an enemy bishop with bishopMoves
            canSee = bishopMoves(getSquare(self.coordinates))

            # trim canSee with pieceBlock()
            canSee = self.pieceBlock(getSquare(self.coordinates), canSee)

            for piece in Pieces:
                if piece.team != self.team and getSquare(piece.coordinates) in canSee and piece.bishop:
                    return True

            # check if it can see an enemy king with kingMoves
            canSee = kingMoves(getSquare(self.coordinates))

            # trim canSee with pieceBlock()
            canSee = self.pieceBlock(getSquare(self.coordinates), canSee)

            for piece in Pieces:
                if piece.team != self.team and getSquare(piece.coordinates) in canSee and piece.king:
                    return True

            # check if it can see an enemy queen with queenMoves
            canSee = queenMoves(getSquare(self.coordinates))

            # trim canSee with pieceBlock()
            canSee = self.pieceBlock(getSquare(self.coordinates), canSee)

            for piece in Pieces:
                if piece.team != self.team and getSquare(piece.coordinates) in canSee and piece.queen:
                    return True

            # return false if you got this far
            return False

        else:
            return False

    # finds nearest pieces on various paths and removes unreachable pieces
    def pieceBlock(self, square, moveList):

        newMoveList = moveList
        killList = []
        mergeList = []

        for piece in Pieces:
            otherSquare = getSquare(piece.coordinates)
            if otherSquare in moveList:
                newMoveList = prune(square, otherSquare, newMoveList)

        return newMoveList

    # returns squares you can move to
    def movelist(self, position):

        moveSquares = Set([])
        if self.pawn:
            moveSquares = moveSquares.union(
                pawnMoves(position, self.team, self.pawnMoved))

            if self.team == 'White':
                for piece in Pieces:
                    if piece.team == 'Black':
                        square = getSquare(piece.coordinates)
                        if square == position - 7:  # can take
                            moveSquares.add(position - 7)
                        elif square == position - 8:  # cant take right in front of it
                            moveSquares.remove(position - 8)

                        elif square == position - 9:  # can take
                            moveSquares.add(position - 9)

                        if not self.pawnMoved:
                            if square == position - 16:  # cant take right in front of it
                                moveSquares.remove(position - 16)
            else:
                for piece in Pieces:
                    if piece.team == 'White':
                        square = getSquare(piece.coordinates)
                        if square == position + 7:  # can take
                            moveSquares.add(position + 7)
                        elif square == position + 8:  # cant take right in front of it
                            moveSquares.remove(position + 8)
                        elif square == position + 9:  # can take
                            moveSquares.add(position + 9)

                        if not self.pawnMoved:
                            if square == position + 16:  # cant take right in front of it
                                moveSquares.remove(position + 16)

        if self.rook:
            moveSquares = moveSquares.union(rookMoves(position))
        if self.knight:
            moveSquares = moveSquares.union(knightMoves(position))
        if self.bishop:
            moveSquares = moveSquares.union(bishopMoves(position))
        if self.king:
            moveSquares = moveSquares.union(kingMoves(position))
        if self.queen:
            moveSquares = moveSquares.union(queenMoves(position))

        # trim moveSquares with pieceBlock()
        moveSquares = self.pieceBlock(getSquare(self.coordinates), moveSquares)

        return moveSquares



# draw board so that pieces can be initialized
drawBoard((DARK_BROWN, LIGHT_BROWN))

# initialize pieces
Pieces = [
    #     ChessPiece('bp.png', squareCenters[21], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[35], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[14], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[8], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[7], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[59], 'Black', 'p'),
    #     ChessPiece('bp.png', squareCenters[29], 'Black', 'p'),
    #     ChessPiece('wb.png', squareCenters[13], 'White', 'b'),
    #     ChessPiece('wb.png', squareCenters[11], 'White', 'b'),
    #     ChessPiece('bb.png', squareCenters[32], 'Black', 'b'),
    #     ChessPiece('bb.png', squareCenters[43], 'Black', 'b'),
    #     ChessPiece('wn.png', squareCenters[61], 'White', 'n'),
    #     ChessPiece('wn.png', squareCenters[27], 'White', 'n'),
    #     ChessPiece('bn.png', squareCenters[23], 'Black', 'n'),
    #     ChessPiece('bn.png', squareCenters[16], 'Black', 'n'),
    #     ChessPiece('wr.png', squareCenters[22], 'White', 'r'),
    #     ChessPiece('wr.png', squareCenters[60], 'White', 'r'),
    #     ChessPiece('br.png', squareCenters[54], 'Black', 'r'),
    #     ChessPiece('br.png', squareCenters[2], 'Black', 'r'),
    #     ChessPiece('bk.png', squareCenters[38], 'Black', 'k'),
    #     ChessPiece('wk.png', squareCenters[50], 'White', 'k'),
    #     ChessPiece('bq.png', squareCenters[52], 'Black', 'q'),
    #     ChessPiece('wq.png', squareCenters[5], 'White', 'q'),
    ChessPiece('wp.png', squareCenters[48], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[49], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[50], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[51], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[52], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[53], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[54], 'White', 'p'),
    ChessPiece('wp.png', squareCenters[55], 'White', 'p'),
    ChessPiece('bp.png', squareCenters[8], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[9], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[10], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[11], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[12], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[13], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[14], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[15], 'Black', 'p'),
    ChessPiece('wb.png', squareCenters[58], 'White', 'b'),
    ChessPiece('wb.png', squareCenters[61], 'White', 'b'),
    ChessPiece('bb.png', squareCenters[2], 'Black', 'b'),
    ChessPiece('bb.png', squareCenters[5], 'Black', 'b'),
    ChessPiece('wn.png', squareCenters[57], 'White', 'n'),
    ChessPiece('wn.png', squareCenters[62], 'White', 'n'),
    ChessPiece('bn.png', squareCenters[1], 'Black', 'n'),
    ChessPiece('bn.png', squareCenters[6], 'Black', 'n'),
    ChessPiece('wr.png', squareCenters[56], 'White', 'r'),
    ChessPiece('wr.png', squareCenters[63], 'White', 'r'),
    ChessPiece('br.png', squareCenters[0], 'Black', 'r'),
    ChessPiece('br.png', squareCenters[7], 'Black', 'r'),
    ChessPiece('bk.png', squareCenters[4], 'Black', 'k'),
    ChessPiece('wk.png', squareCenters[60], 'White', 'k'),
    ChessPiece('bq.png', squareCenters[3], 'Black', 'q'),
    ChessPiece('wq.png', squareCenters[59], 'White', 'q'),
]
