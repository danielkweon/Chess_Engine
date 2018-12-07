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


def scoreBoard(board):
    return 0

def possibleMoves(board, row, col):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    copyBoard = copy.deepcopy(board)
    moves = []
    if copyBoard[row][col] == 'p':
        if copyBoard[row + 1][col] == '.' :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if row == 1 and copyBoard[row + 1][col] == '.': 
                toPos = cols[col] + str(6 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    return moves

def possibleMovesOpponent(board, row, col):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    copyBoard = copy.deepcopy(board)
    moves = []
    if copyBoard[row][col] == 'P':
        if copyBoard[row + 1][col] == '.' :
            fromPos = cols[col] + str(8 - row)
            toPos = cols[col] + str(7 - row)
            moves.append(move(copy.deepcopy(board), fromPos, toPos))
            if row == 1 and copyBoard[row + 1][col] == '.': 
                toPos = cols[col] + str(6 - row)
                moves.append(move(copy.deepcopy(board), fromPos, toPos))
    return moves

def respond(board):
    possibleMovesArray = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in "p":
                possibleMovesArray.append(possibleMoves(board, row, col))

    possibleMovesDepth_2 = []
    bestMove = possibleMovesArray[0]
    for position in possibleMovesArray:
        for row in range(0,8):
            for col in range(0,8):
                if position[row][col] in "P":
                    possibleMovesDepth_2.append(possibleMovesOpponent(position, row, col))
    return board



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
    if movefrom == 'q':
        exit()
    moveto = input("Type your move to: ")
    board = move(board, movefrom, moveto)
    printBoard(board, movenumber)
    movenumber +=  1

    print("The Computer's Move . . .")
    time.sleep(1)

    board = respond(board)
    printBoard(board, movenumber)
    movenumber +=  1


