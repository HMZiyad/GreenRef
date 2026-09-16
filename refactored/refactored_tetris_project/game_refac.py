from grid import Grid
from blocks import *
import random
import pygame
import os

class Game:
    rotate_sound = pygame.mixer.Sound(os.path.join("Sounds", "rotate.ogg"))
    clear_sound = pygame.mixer.Sound(os.path.join("Sounds", "clear.ogg"))
    pygame.mixer.music.load(os.path.join("Sounds", "music.ogg"))
    pygame.mixer.music.play(-1)

    def __init__(self):
        self.grid = Grid()
        self.block_classes = [IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, ZBlock]
        self.blocks = [cls() for cls in self.block_classes]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, move_down_points):
        score_map = {1: 100, 2: 300, 3: 500}
        self.score += score_map.get(lines_cleared, 0)
        self.score += move_down_points

    def get_random_block(self):
        if not self.blocks:
            self.blocks = [cls() for cls in self.block_classes]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            Game.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [cls() for cls in self.block_classes]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        return all(self.grid.is_empty(tile.row, tile.column)
                   for tile in self.current_block.get_cell_positions())

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            Game.rotate_sound.play()

    def block_inside(self):
        return all(self.grid.is_inside(tile.row, tile.column)
                   for tile in self.current_block.get_cell_positions())

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        offset_x, offset_y = (270, 270)
        if self.next_block.id == 3:
            offset_x, offset_y = 255, 290
        elif self.next_block.id == 4:
            offset_x, offset_y = 255, 280
        self.next_block.draw(screen, offset_x, offset_y)
