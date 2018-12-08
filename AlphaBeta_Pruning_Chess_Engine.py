"""
@date: December 5, 2018
@author: Daniel Kweon, Lin Chen

Alpha Beta Pruning Chess Engine
Combinatorics Project YAY

"""

import time
import copy


pawnScore = [[0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, -4, -4, 0, 0, 0],
            [2, 2, 4, 6, 6, 4, 2, 2],
            [4, 6, 8, 16, 16, 8, 6, 4],
            [8, 10, 12, 18, 18, 12, 10, 8],
            [12, 14, 16, 21, 21, 16, 14, 12],
            [20, 26, 26, 28, 28, 26, 26, 20],
            [0, 0, 0, 0, 0, 0, 0, 0]]

knightScore =   [[-50, -20, -10, -10, -10, -10, -20, -50], 
                [-5, 0, 5, 5, 5, 5, 0, -5], 
                [-5, 5, 8, 8, 8, 8, 5, -5], 
                [-5, 5, 10, 15, 15, 10, 5, -5], 
                [-5, 5, 10, 15, 15, 10, 5, -5], 
                [-5, 5, 10, 15, 15, 10, 5, -5], 
                [-5, 5, 5, 5, 5, 5, 5, -5],
                [-40, -10, -5, -5, -5, -5, -10, -40]] 

rookScore = [[0, 0, 5, 10, 10, 5, 0, 0], 
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [0, 0, 5, 10, 10, 5, 0, 0],
            [5, 5, 5, 10, 10, 5, 5, 5],
            [10, 10, 10, 10, 10, 10, 10, 10]]

bishopScores =  [[-50, -20, -10, -20, -20, -10, -20, -50],
                [0, 5, 0, 0, 0, 0, 5, 0],
                [0, 0, 5, 5, 5, 5, 0, 0],
                [0, 5, 10, 18, 18, 10, 5, 0],
                [0, 10, 10, 18, 18, 10, 10, 0],
                [0, 10, 10, 18, 18, 10, 10, 0],
                [0, 5, 5, 5, 5, 5, 5, 0],
                [-40, -20, -15, -15, -15, -15, -20, -40]]

queenScores =   [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 10, 10, 10, 10, 0, 0],
                [0, 0, 10, 15, 15, 10, 0, 0],
                [0, 0, 10, 15, 15, 10, 0, 0],
                [0, 0, 10, 10, 10, 10, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

kingScores =    [[24, 24, 24, 16, 16, 6, 32, 32],
                [24, 20, 16, 12, 12, 16, 20, 24],
                [16, 12, 8, 4, 4, 8, 12, 16],
                [12, 8, 4, 0, 0, 4, 8, 12],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]


def printBoard(board, move):
    print("Chess Board - Move " + str(move))
    print("\t\ta\tb\tc\td\te\tf\tg\th\n")
    print("\t\t_\t_\t_\t_\t_\t_\t_\t_\n")
    for x in range(0,8):
        row = board[x]
        rowString = str(8-x) + '\t|\t'
        for col in row:
            rowString += col + '\t'
        print(rowString + "\n")

def scoreBoard(board):
    score = 0
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in "p":
                score = score + pawnScore[row][col] + 5
            elif board[row][col] in "n":
                score = score + knightScore[row][col] + 30
            elif board[row][col] in "r":
                score = score + rookScore[row][col] + 50
            elif board[row][col] in "b":
                score = score + bishopScores[row][col] + 40
            elif board[row][col] in "q":
                score = score + queenScores[row][col] + 90
            elif board[row][col] in "k":
                score = score + kingScores[row][col]     
            elif board[row][col] in "P":
                score = score - pawnScore[7 - row][col] - 5
            elif board[row][col] in "N":
                score = score - knightScore[7 - row][col] - 30
            elif board[row][col] in "R":
                score = score - rookScore[7 - row][col] - 50
            elif board[row][col] in "B":
                score = score - bishopScores[7 - row][col] - 40
            elif board[row][col] in "Q":
                score = score - queenScores[7 - row][col] - 90
            elif board[row][col] in "K":
                score = score - kingScores[7 - row][col]    
    return score

def move(board, fromMove, toMove):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    fromCol = 0
    toCol = 0
    for x in range(0,8):
        if cols[x] == fromMove[0] :
            fromCol = x
        if cols[x] == toMove[0] :
            toCol = x
    printboard = False
    if board[8 - int(toMove[1])][toCol] not in '.':
        board[8 - int(toMove[1])][toCol] = '.'
        printboard = True
    piece = board[8 - int(fromMove[1])][fromCol]
    board[8 - int(fromMove[1])][fromCol] = board[8 - int(toMove[1])][toCol]
    board[8 - int(toMove[1])][toCol] = piece
    if board[8 - int(toMove[1])][toCol] == 'P' and int(toMove[1]) == 8:
        newPiece = input("What piece do you want? : ")
        board[8 - int(toMove[1])][toCol] = newPiece
    # if printboard and piece == 'p' and piece != 'P':
    #     printBoard(board, -3)
    #     print(str(scoreBoard(board)))
    return board



def possibleMoves(board, row, col, moves):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    opponentPieces = "PQKNRB."
    copyBoard = copy.deepcopy(board)
    if copyBoard[row][col] == 'p':
        if row + 1 == 7:
            if copyBoard[row + 1][col] == '.' :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row + 1][col] = 'q'
                moves.append(movestemp)
            if col + 1 < 8 and copyBoard[row + 1][col + 1] in "PQKNRB" :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row + 1][col + 1] = 'q'
                moves.append(movestemp)
            if col - 1 >= 0 and copyBoard[row + 1][col - 1] in "PQKNRB" :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row + 1][col - 1] = 'q'
                moves.append(movestemp)
            return moves
        else :
            if copyBoard[row + 1][col] == '.' :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col] + str(7 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                if row == 1 and copyBoard[row + 2][col] == '.': 
                    toPos = cols[col] + str(6 - row)
                    moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if col + 1 < 8 and copyBoard[row + 1][col + 1] in "PQKNRB" :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col + 1] + str(7- row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if col - 1 >= 0 and copyBoard[row + 1][col - 1] in "PQKNRB" :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col - 1] + str(7 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
    if copyBoard[row][col] == 'n':
        if row + 1 < 8 and col + 2 < 8 and copyBoard[row + 1][col + 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 1 < 8 and col - 2 >= 0 and copyBoard[row + 1][col - 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col - 2 >= 0 and copyBoard[row - 1][col - 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col + 2 < 8 and copyBoard[row - 1][col + 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
        if row + 2 < 8 and col + 1 < 8 and copyBoard[row + 2][col + 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 2 < 8 and col - 1 >= 0 and copyBoard[row + 2][col - 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col - 1 >= 0 and copyBoard[row - 2][col - 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col + 1 < 8 and copyBoard[row - 2][col + 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
    if copyBoard[row][col] == 'r':
        x = col - 1
        blocked_piece = False
        while x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'pqnkbr'
            x = x - 1
        x = col + 1
        blocked_piece = False
        while x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'pqnkbr'
            x = x + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'pqnkbr'
            y = y + 1
            # printBoard(move(copy.deepcopy(board), fromPos, toPos), -1)
            # print(str(scoreBoard(move(copy.deepcopy(board), fromPos, toPos))))
        y = row - 1
        blocked_piece = False
        while y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'pqnkbr'
            y = y - 1
    if copyBoard[row][col] == 'b':
        x = col - 1
        y = row - 1
        blocked_piece = False
        while x >= 0 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x - 1     
            y = y - 1       
        x = col + 1
        y = row - 1
        blocked_piece = False
        while x < 8 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x + 1     
            y = y - 1
        x = col - 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x - 1     
            y = y + 1
        x = col + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x + 1     
            y = y + 1    
    if copyBoard[row][col] == 'q':
        x = col - 1
        y = row - 1
        blocked_piece = False
        while x >= 0 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x - 1     
            y = y - 1       
        x = col + 1
        y = row - 1
        blocked_piece = False
        while x < 8 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x + 1     
            y = y - 1
        x = col - 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x - 1     
            y = y + 1
        x = col + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'pqnkbr'
            x = x + 1     
            y = y + 1
        x = col - 1
        blocked_piece = False
        while x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'pqnkbr'
            x = x - 1
        x = col + 1
        blocked_piece = False
        while x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'pqnkbr'
            x = x + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'pqnkbr'
            y = y + 1
            # printBoard(move(copy.deepcopy(board), fromPos, toPos), -1)
            # print(str(scoreBoard(move(copy.deepcopy(board), fromPos, toPos))))
        y = row - 1
        blocked_piece = False
        while y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'PQKNRB'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'pqnkbr'
            y = y - 1 
    if copyBoard[row][col] == 'k':
        x = col - 1
        y = row - 1
        if x >= 0 and y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))    
        x = col + 1
        y = row - 1
        if x < 8 and y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col - 1
        y = row + 1
        if y < 8 and x >= 0  :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col + 1
        y = row + 1
        if y < 8 and x < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col - 1
        if x >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col + 1
        if x < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        y = row + 1
        if y < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        y = row - 1
        if y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.PQKNRB'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    return moves

def possibleMovesOpponent(board, row, col, moves):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    opponentPieces = "pbnkqr."
    copyBoard = copy.deepcopy(board)
    if copyBoard[row][col] == 'P':
        if row - 1 == 0 :
            if copyBoard[row - 1][col] == '.' :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row - 1][col] = 'Q'
                moves.append(movestemp)
            if col + 1 < 8 and copyBoard[row - 1][col + 1] in "pbnkqr" :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row - 1][col + 1] = 'Q'
                moves.append(movestemp)   
            if col - 1 >= 0 and copyBoard[row - 1][col - 1] in "pbnkqr" :
                movestemp = copy.deepcopy(board)
                movestemp[row][col] = '.'
                movestemp[row - 1][col - 1] = 'Q'
                moves.append(movestemp)   
            return moves
        else :
            if copyBoard[row - 1][col] == '.' :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col] + str(9 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                if row == 6 and copyBoard[row - 2][col] == '.': 
                    toPos = cols[col] + str(10 - row)
                    moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if col + 1 < 8 and copyBoard[row - 1][col + 1] in "pbnkqr" :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col + 1] + str(9 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if col - 1 >= 0 and copyBoard[row - 1][col - 1] in "pbnkqr" :
                fromPos = cols[col] + str(8 - row)
                toPos = cols[col - 1] + str(9 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))     
    if copyBoard[row][col] == 'N':
        if row + 1 < 8 and col + 2 < 8 and copyBoard[row + 1][col + 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 1 < 8 and col - 2 >= 0 and copyBoard[row + 1][col - 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col - 2 >= 0 and copyBoard[row - 1][col - 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col + 2 < 8 and copyBoard[row - 1][col + 2] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
        if row + 2 < 8 and col + 1 < 8 and copyBoard[row + 2][col + 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 2 < 8 and col - 1 >= 0 and copyBoard[row + 2][col - 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col - 1 >= 0 and copyBoard[row - 2][col - 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col + 1 < 8 and copyBoard[row - 2][col + 1] in opponentPieces:
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
    if copyBoard[row][col] == 'R':
        x = col - 1
        blocked_piece = False
        while x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'PQKNRB'
            x = x - 1
        x = col + 1
        blocked_piece = False
        while x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'PQKNRB'
            x = x + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'PQKNRB'
            y = y + 1
            # printBoard(move(copy.deepcopy(board), fromPos, toPos), -1)
            # print(str(scoreBoard(move(copy.deepcopy(board), fromPos, toPos))))
        y = row - 1
        blocked_piece = False
        while y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'PQKNRB'
            y = y - 1
    if copyBoard[row][col] == 'B':
        x = col - 1
        y = row - 1
        blocked_piece = False
        while x >= 0 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x - 1     
            y = y - 1       
        x = col + 1
        y = row - 1
        blocked_piece = False
        while x < 8 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x + 1     
            y = y - 1
        x = col - 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x - 1     
            y = y + 1
        x = col + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x + 1     
            y = y + 1  
    if copyBoard[row][col] == 'Q':
        x = col - 1
        y = row - 1
        blocked_piece = False
        while x >= 0 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x - 1     
            y = y - 1       
        x = col + 1
        y = row - 1
        blocked_piece = False
        while x < 8 and y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x + 1     
            y = y - 1
        x = col - 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x - 1     
            y = y + 1
        x = col + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][x] in 'PQKNRB'
            x = x + 1     
            y = y + 1
        x = col - 1
        blocked_piece = False
        while x >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'PQKNRB'
            x = x - 1
        x = col + 1
        blocked_piece = False
        while x < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[row][x] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[row][x] in 'PQKNRB'
            x = x + 1
        y = row + 1
        blocked_piece = False
        while y < 8 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'PQKNRB'
            y = y + 1
            # printBoard(move(copy.deepcopy(board), fromPos, toPos), -1)
            # print(str(scoreBoard(move(copy.deepcopy(board), fromPos, toPos))))
        y = row - 1
        blocked_piece = False
        while y >= 0 and not blocked_piece :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in opponentPieces
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
                blocked_piece = copyBoard[y][col] in 'pqnkbr'
            blocked_piece = blocked_piece or copyBoard[y][col] in 'PQKNRB'
            y = y - 1 
    if copyBoard[row][col] == 'K':
        x = col - 1
        y = row - 1
        if x >= 0 and y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))    
        x = col + 1
        y = row - 1
        if x < 8 and y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col - 1
        y = row + 1
        if y < 8 and x >= 0  :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col + 1
        y = row + 1
        if y < 8 and x < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - y)
            can_go = copyBoard[y][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col - 1
        if x >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        x = col + 1
        if x < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[x] + str(8 - row)
            can_go = copyBoard[row][x] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        y = row + 1
        if y < 8 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
        y = row - 1
        if y >= 0 :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(8 - y)
            can_go = copyBoard[y][col] in '.pbnkqr'
            if can_go :
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    return moves

def respond(board):
    possibleMovesArray = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in "pnrqkb":
                possibleMoves(board, row, col, possibleMovesArray)
    bestMinScore = -1000
    respondMove = []
    for position in possibleMovesArray:
        possibleMovesDepth_2 = []
        bestScoreDepth_2 = 1000
        bestPositionDepth_2 = []
        for row in range(0,8):
            for col in range(0,8):
                if position[row][col] in "PNRQKB":
                    possibleMovesOpponent(position, row, col, possibleMovesDepth_2)

                    """ higher depth """
                    # for positionDepth_2 in possibleMovesDepth_2:
                    #     possibleMovesDepth_3 = []
                    #     for rowDepth_3 in range(0,8):
                    #         for colDepth_3 in range(0,8):
                    #             if positionDepth_2[rowDepth_3][colDepth_3] in "pnrqkb":
                    #                 possibleMoves(positionDepth_2, rowDepth_3, colDepth_3, possibleMovesDepth_3)

                    #                 for positionDepth_3 in possibleMovesDepth_3:
                    #                     possibleMovesDepth_4 = []
                    #                     for rowDepth_4 in range(0,8):
                    #                         for colDepth_4 in range(0,8):
                    #                             if positionDepth_3[rowDepth_4][colDepth_4] in "PNRQKB":
                    #                                 possibleMoves(positionDepth_3, rowDepth_4, colDepth_4, possibleMovesDepth_4)

        minscore = 1000
        minmove = []
        #scorestr = " "
        for possibleBoards in possibleMovesDepth_2:
            score = scoreBoard(possibleBoards)
            #printBoard(possibleBoards, -1)
            #scorestr = scorestr + str(score) + " : "
            if score < minscore:
                minscore = score
                minmove = possibleBoards
        if bestMinScore < minscore:
            bestMinScore = minscore
            bestPositionDepth_2 = position
            respondMove = position
    #     printBoard(minmove, -1)
    #     print("lowest " + str(minscore))
    # printBoard(respondMove, -1)
    # print(str(scoreBoard(respondMove)))
    return respondMove

# what to do when equal scores
# what to do regarding piece values


a = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'] 
b = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
c = ['.', '.', '.', '.', '.', '.', '.', '.']
d = ['.', '.', '.', '.', '.', '.', '.', '.']
e = ['.', '.', '.', '.', '.', '.', '.', '.']
f = ['.', '.', '.', '.', '.', '.', '.', '.']
g = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
h = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
board = [a, b, c, d, e, f, g, h]

print("\nWelcome to Our Chess Engine\n")
printBoard(board, 0)

gameEnded = False
movenumber = 1
while not gameEnded :
    movefrom = input("Type your move from: ")
    if movefrom == 'q':
        quit()
    moveto = input("Type your move to: ")
    movefromvalid = (movefrom[0] in "abcdefgh") and (movefrom[1] in "12345678")
    movetovalid = (moveto[0] in "abcdefgh") and (moveto[1] in "12345678")
    if movefromvalid and movetovalid:
        board = move(board, movefrom, moveto)
        printBoard(board, movenumber)
        movenumber +=  1

        print("The Computer's Move . . .")
        time.sleep(1)

        board = respond(board)
        printBoard(board, movenumber)
        #print("score : " + str(scoreBoard(board)))
        movenumber +=  1
    else :
        print("INVALID MOVES try again")


