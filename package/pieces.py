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
        self.square = position
        self.rect.center = position.center
        self.coordinates = position.center

    def mergePiece(self, position, otherPiece):
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
    ChessPiece('bp.png', squareCenters[21], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[35], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[14], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[8], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[7], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[59], 'Black', 'p'),
    ChessPiece('bp.png', squareCenters[29], 'Black', 'p'),
    ChessPiece('wb.png', squareCenters[13], 'White', 'b'),
    ChessPiece('wb.png', squareCenters[11], 'White', 'b'),
    ChessPiece('bb.png', squareCenters[32], 'Black', 'b'),
    ChessPiece('bb.png', squareCenters[43], 'Black', 'b'),
    ChessPiece('wn.png', squareCenters[61], 'White', 'n'),
    ChessPiece('wn.png', squareCenters[27], 'White', 'n'),
    ChessPiece('bn.png', squareCenters[23], 'Black', 'n'),
    ChessPiece('bn.png', squareCenters[16], 'Black', 'n'),
    ChessPiece('wr.png', squareCenters[22], 'White', 'r'),
    ChessPiece('wr.png', squareCenters[60], 'White', 'r'),
    ChessPiece('br.png', squareCenters[54], 'Black', 'r'),
    ChessPiece('br.png', squareCenters[2], 'Black', 'r'),
    ChessPiece('bk.png', squareCenters[38], 'Black', 'k'),
    ChessPiece('wk.png', squareCenters[50], 'White', 'k'),
    ChessPiece('bq.png', squareCenters[52], 'Black', 'q'),
    ChessPiece('wq.png', squareCenters[5], 'White', 'q'),
    #     ChessPiece('wpawn.png', squareCenters[48], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[49], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[50], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[51], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[52], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[53], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[54], 'White', 'p'),
    #     ChessPiece('wpawn.png', squareCenters[55], 'White', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[8], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[9], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[10], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[11], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[12], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[13], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[14], 'Black', 'p'),
    #     ChessPiece('bpawn.png', squareCenters[15], 'Black', 'p'),
    #     ChessPiece('wbishop.png', squareCenters[58], 'White', 'b'),
    #     ChessPiece('wbishop.png', squareCenters[61], 'White', 'b'),
    #     ChessPiece('bbishop.png', squareCenters[2], 'Black', 'b'),
    #     ChessPiece('bbishop.png', squareCenters[5], 'Black', 'b'),
    #     ChessPiece('wknight.png', squareCenters[57], 'White', 'n'),
    #     ChessPiece('wknight.png', squareCenters[62], 'White', 'n'),
    #     ChessPiece('bknight.png', squareCenters[1], 'Black', 'n'),
    #     ChessPiece('bknight.png', squareCenters[6], 'Black', 'n'),
    #     ChessPiece('wrook.png', squareCenters[56], 'White', 'r'),
    #     ChessPiece('wrook.png', squareCenters[63], 'White', 'r'),
    #     ChessPiece('brook.png', squareCenters[0], 'Black', 'r'),
    #     ChessPiece('brook.png', squareCenters[7], 'Black', 'r'),
    #     ChessPiece('bking.png', squareCenters[4], 'Black', 'k'),
    #     ChessPiece('wking.png', squareCenters[60], 'White', 'k'),
    #     ChessPiece('bqueen.png', squareCenters[3], 'Black', 'q'),
    #     ChessPiece('wqueen.png', squareCenters[59], 'White', 'q'),
]
