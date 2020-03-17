import numpy as np
import random
from collections import Counter

positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


class Agent():
    def __init__(self, symbol):
        self.availablePos = []
        self.symbol = symbol
        self.IsWinner = -1

    def availPos(self, gameBoard):
        self.availablePos = []
        count = 0
        for i in gameBoard:
            for j in i:
                if (j == 0):
                    self.availablePos.append(count)
                count += 1
        # print(self.availablePos)

    def checkIfWinner(self, gameBoard):
        self.tempBoard = gameBoard.copy()
        self.tempBoard = self.tempBoard.tolist()
        for row in self.tempBoard:
            self.symbolCount = Counter(row)
            # print(symbolCount)
            if (self.symbolCount[self.symbol] == 3):
                self.IsWinner = 1

                # print("winner1")
                return 1

        self.colcheck = zip(*self.tempBoard)

        for row in self.colcheck:
            self.symbolCount = Counter(row)
            # print(symbolCount)
            if (self.symbolCount[self.symbol] == 3):
                self.IsWinner = 1

                # print("winner2")
                return 1

        self.count = 0
        for i in range(0, len(self.tempBoard)):
            if (self.tempBoard[i][i] == self.symbol):
                self.count += 1

        if (self.count == 3):
            self.IsWinner = 1

            # print("Winner 3")
            return 1

        self.count = 0
        j = len(self.tempBoard) - 1
        for i in range(0, len(self.tempBoard)):
            if (self.tempBoard[i][j] == self.symbol):
                self.count += 1
            j -= 1
        if (self.count == 3):
            self.IsWinner = 1

            # print("winner 4")
            return 1

        self.tempstr = ''.join([str(val) for sublist in self.tempBoard for val in sublist])
        if str(0) not in self.tempstr:
            self.IsWinner = 0

            # print("AI draw")
            return 0

        else:
            self.IsWinner = -1
            return -1


def displayBoard(Board, p, q):
    # print(Board)
    print("---------------------------")
    Board = Board.tolist()
    for row in Board:
        temp = []
        for i in row:
            if (i == 0):
                temp.append(" ")
            if (i == p.symbol):
                temp.append("X")
            if (i == q.symbol):
                temp.append("O")
        print("|   " + str(temp[0]) + "   |   " + str(temp[1]) + "   |   " + str(temp[2]) + "   |   ")
    print("---------------------------")


class HumanPlayer():
    def __init__(self, symbol):
        self.symbol = symbol
        self.IsWinner = -1
        self.availablePos = []

    def availPos(self, gameBoard):
        self.availablePos = []
        count = 0
        for i in gameBoard:
            for j in i:
                if (j == 0):
                    self.availablePos.append(count)
                count += 1

    def PlayTurn(self, Board):
        self.availPos(Board)
        move = int(input("enter your move: "))
        while (move not in self.availablePos):
            # print("please enter a valid move!")
            move = int(input("enter your move: "))
        pos = positions[move]
        Board[pos[0]][pos[1]] = self.symbol
        return Board

    def checkIfWinner(self, gameBoard):
        self.tempBoard = gameBoard.copy()
        self.tempBoard = self.tempBoard.tolist()
        for row in self.tempBoard:
            self.symbolCount = Counter(row)
            # print(symbolCount)
            if (self.symbolCount[self.symbol] == 3):
                self.IsWinner = 1
                # print("winner1")
                return 1

        self.colcheck = zip(*self.tempBoard)
        for row in self.colcheck:
            self.symbolCount = Counter(row)
            if (self.symbolCount[self.symbol] == 3):
                self.IsWinner = 1
                # print("winner2")
                return 1

        self.count = 0
        for i in range(0, len(self.tempBoard)):
            if (self.tempBoard[i][i] == self.symbol):
                self.count += 1

        if (self.count == 3):
            self.IsWinner = 1
            # print("Winner 3")
            return 1

        self.count = 0
        j = len(self.tempBoard) - 1
        for i in range(0, len(self.tempBoard)):
            if (self.tempBoard[i][j] == self.symbol):
                self.count += 1
            j -= 1
        if (self.count == 3):
            self.IsWinner = 1
            # print("winner 4")
            return 1

        self.tempstr = ''.join([str(val) for sublist in self.tempBoard for val in sublist])
        if str(0) not in self.tempstr:
            self.IsWinner = 0
            # print("human draw")
            return 0

        else:
            self.IsWinner = -1
            return -1


def minimax(gameBoard, Ai, Human, ismaxip):
    maxscore = -10000
    minscore = 10000

    if (Ai.checkIfWinner(gameBoard) == 1):
        return (1, None)
    if (Human.checkIfWinner(gameBoard) == 1):
        return (-1, None)
    if (Ai.checkIfWinner(gameBoard) == 0):
        return (0, None)

    if (ismaxip == True):
        Ai.availPos(gameBoard)
        for val in Ai.availablePos:
            pos = positions[val]
            gameBoard[pos[0]][pos[1]] = Ai.symbol
            # print(gameBoard)
            score, temp = minimax(gameBoard, Ai, Human, ismaxip=False)
            if (maxscore < score):
                maxscore = score
                action = pos
            gameBoard[pos[0]][pos[1]] = 0
        return (maxscore, action)

    if (ismaxip == False):
        Human.availPos(gameBoard)
        for val in Human.availablePos:
            pos = positions[val]
            gameBoard[pos[0]][pos[1]] = Human.symbol
            score, temp = minimax(gameBoard, Ai, Human, ismaxip=True)
            if (score < minscore):
                minscore = score
                action = pos
            gameBoard[pos[0]][pos[1]] = 0
        return (minscore, action)


def PlayTicTacToe():
    gameBoard = np.zeros([3, 3], dtype=int)
    Ai = Agent(1)
    Human = HumanPlayer(2)
    turn = random.randint(0, 1)
    # turn = 1
    if (turn == 1):

        print("You get to play First!")

        while (1):

            # human plays first
            print("------------ your turn ---------------")
            gameBoard = Human.PlayTurn(gameBoard)
            displayBoard(gameBoard, Human, Ai)
            if (Human.checkIfWinner(gameBoard) == 1):
                print("Bravo, You Won!!")
                break
            if (Human.checkIfWinner(gameBoard) == 0):
                print("Its a Tie!!")
                break

            # AI plays second
            print("------------ AI's turn ---------------")
            score, action = minimax(gameBoard, Ai, Human, ismaxip=True)

            gameBoard[action[0]][action[1]] = Ai.symbol
            displayBoard(gameBoard, Human, Ai)
            if (Ai.checkIfWinner(gameBoard) == 1):
                print("ooPs, AI is damn smart!!")
                break
            if (Ai.checkIfWinner(gameBoard) == 0):
                print("Its a Tie!!")
                break
        gameBoard = np.zeros([3, 3], dtype=int)

    else:

        print("AI gets to play First!")
        firstturn = True
        while (1):

            # AI plays first
            print("------------ AI's turn ---------------")
            if (firstturn == True):
                p = random.randint(0, 8)
                action = positions[p]
                firstturn = False
            else:
                score, action = minimax(gameBoard, Ai, Human, ismaxip=True)

            gameBoard[action[0]][action[1]] = Ai.symbol
            displayBoard(gameBoard, Human, Ai)
            if (Ai.checkIfWinner(gameBoard) == 1):
                print("ooPs, AI is damn smart!!")
                break
            if (Ai.checkIfWinner(gameBoard) == 0):
                print("Its a Tie!!")
                break

            # human plays first
            print("------------ your turn ---------------")
            gameBoard = Human.PlayTurn(gameBoard)
            displayBoard(gameBoard, Human, Ai)
            if (Human.checkIfWinner(gameBoard) == 1):
                print("Bravo, You Won!!")
                break
            if (Human.checkIfWinner(gameBoard) == 0):
                print("Its a Tie!!")
                break


PlayTicTacToe()
