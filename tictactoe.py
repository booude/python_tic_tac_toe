import random
import sys
import pygame as p
import numpy as np

from const import *

p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Python Tic Tac Toe")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self):
        for col in range(COLS):
            if (
                self.squares[0][col]
                == self.squares[1][col]
                == self.squares[2][col]
                != 0
            ):
                return self.squares[0][col]

        for row in range(ROWS):
            if (
                self.squares[row][0]
                == self.squares[row][1]
                == self.squares[row][2]
                != 0
            ):
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = "ai"
        self.running = True
        self.show_lines()

    def show_lines(self):
        p.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        p.draw.line(
            screen,
            LINE_COLOR,
            (WIDTH - SQSIZE, 0),
            (WIDTH - SQSIZE, HEIGHT),
            LINE_WIDTH,
        )

        p.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        p.draw.line(
            screen,
            LINE_COLOR,
            (0, HEIGHT - SQSIZE),
            (WIDTH, HEIGHT - SQSIZE),
            LINE_WIDTH,
        )

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            p.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            p.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        if self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            p.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1


class AI:
    def __init__(self, level=0, player=2) -> None:
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]

    def eval(self, main_board):
        if self.level == 0:
            eval = "random"
            move = self.rnd(main_board)
        else:
            eval, move = self.minmax(main_board, False)
        return move


def main():
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, 1)
                    game.draw_fig(row, col)
                    game.next_turn()

        if game.gamemode == "ai" and game.player == ai.player:
            p.display.update()

            row, col = ai.eval(board)

            board.mark_sqr(row, col, 1)
            game.draw_fig(row, col)
            game.next_turn()

        p.display.update()


main()
