# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np

size_of_board = 600
third_size = size_of_board / 3
sixth_size = size_of_board / 6
symbol_size = (third_size - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Tic_Tac_Toe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((3, 3), dtype=int)

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(1, 3):
            self.canvas.create_line(i * third_size, 0, i * third_size, size_of_board)
            self.canvas.create_line(0, i * third_size, size_of_board, i * third_size)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status.fill(0)

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, third_size, font="cmr 60 bold", fill=color, text=text)
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text='Scores ')
        score_text = f'''Player 1 (X) : {self.X_score}
Player 2 (O): {self.O_score}
Tie                    : {self.tie_score}'''
        self.canvas.create_text(size_of_board / 2, 3 * third_size, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text='Click to play again ')
        self.reset_board = True

    def convert_logical_to_grid_position(self, logical_position):
        return [third_size * i + sixth_size for i in logical_position]

    def convert_grid_to_logical_position(self, grid_position):
        return [int(grid_position[0] // third_size), int(grid_position[1] // third_size)]

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        p = -1 if player == 'X' else 1
        b = self.board_status
        for i in range(3):
            if all(b[i, :] == p) or all(b[:, i] == p):
                return True
        if b[0, 0] == b[1, 1] == b[2, 2] == p or b[0, 2] == b[1, 1] == b[2, 0] == p:
            return True
        return False

    def is_tie(self):
        return not (self.board_status == 0).any()

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        self.O_wins = not self.X_wins and self.is_winner('O')
        self.tie = not self.X_wins and not self.O_wins and self.is_tie()
        gameover = self.X_wins or self.O_wins or self.tie
        if self.X_wins:
            print('X wins')
        elif self.O_wins:
            print('O wins')
        elif self.tie:
            print('Its a tie')
        return gameover

    def click(self, event):
        if self.reset_board:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
            return

        logical_position = self.convert_grid_to_logical_position([event.x, event.y])
        if not self.is_grid_occupied(logical_position):
            if self.player_X_turns:
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
            else:
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
            self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
