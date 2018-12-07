"""
@date: December 5, 2018
@author: Daniel Kweon, Lin Chen

Alpha Beta Pruning Chess Engine
Combinatorics Project

"""

import time
import copy

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

def move(board, fromMove, toMove):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    fromCol = 0
    toCol = 0
    for x in range(0,8):
        if cols[x] == fromMove[0] :
            fromCol = x
        if cols[x] == toMove[0] :
            toCol = x
    piece = board[8 - int(fromMove[1])][fromCol]
    board[8 - int(fromMove[1])][fromCol] = board[8 - int(toMove[1])][toCol]
    board[8 - int(toMove[1])][toCol] = piece
    return board

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


def scoreBoard(board):
    score = 0
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in "p":
                score = score + pawnScore[row][col]
            elif board[row][col] in "n":
                score = score + knightScore[row][col]
            elif board[row][col] in "P":
                score = score - pawnScore[7 - row][col]
            elif board[row][col] in "N":
                score = score - knightScore[7 - row][col]
    return score

def possibleMoves(board, row, col, moves):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    copyBoard = copy.deepcopy(board)
    if copyBoard[row][col] == 'a':
        if copyBoard[row + 1][col] == '.' :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if row == 1 and copyBoard[row + 2][col] == '.': 
                toPos = cols[col] + str(6 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    if copyBoard[row][col] == 'n':
        if row + 1 < 8 and col + 2 < 8 and copyBoard[row + 1][col + 2] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 1 < 8 and col - 2 >= 0 and copyBoard[row + 1][col - 2] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col - 2 >= 0 and copyBoard[row - 1][col - 2] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 1 >= 0 and col + 2 < 8 and copyBoard[row - 1][col + 2] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 2] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
        if row + 2 < 8 and col + 1 < 8 and copyBoard[row + 2][col + 1] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))  
        if row + 2 < 8 and col - 1 >= 0 and copyBoard[row + 2][col - 1] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(6 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col - 1 >= 0 and copyBoard[row - 2][col - 1] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col - 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
        if row - 2 >= 0 and col + 1 < 8 and copyBoard[row - 2][col + 1] in "PQKNRB.":
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col + 1] + str(10 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos)) 
    return moves

def possibleMovesOpponent(board, row, col):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    copyBoard = copy.deepcopy(board)
    moves = []
    if copyBoard[row][col] == 'P':
        if copyBoard[row - 1][col] == '.' :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(9 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if row == 6 and copyBoard[row - 2][col] == '.': 
                toPos = cols[col] + str(10 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    return moves

def respond(board):
    possibleMovesArray = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in "pn":
                possibleMoves(board, row, col, possibleMovesArray)
    bestMinScore = -1000
    respondMove = []
    for position in possibleMovesArray:
        for row in range(0,8):
            for col in range(0,8):
                if position[row][col] in "P":
                    possibleMovesDepth_2 = possibleMovesOpponent(position, row, col)
                    minscore = 1000
                    minmove = []
                    for possibleBoards in possibleMovesDepth_2:
                        score = scoreBoard(possibleBoards)
                        printBoard(possibleBoards, -1)
                        print(score)
                        if score < minscore:
                            minscore = score
                            minmove = possibleBoards
                    if bestMinScore < minscore:
                        bestMinScore = minscore
                        respondMove = position
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
while ~gameEnded :
    movefrom = input("Type your move from: ")
    moveto = input("Type your move to: ")
    if movefrom == 'q':
        quit()
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
        movenumber +=  1
    else :
        print("INVALID MOVES try again")


