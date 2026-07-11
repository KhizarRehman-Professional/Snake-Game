# snake.py - OOP: Snake and Food classes

import pygame
import random

# Constants
CELL = 20  # size of each grid cell

class Snake:
    """Represents the snake - OOP concept"""

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.reset()

    def reset(self):
        # Snake starts as 3 blocks in the center
        cx = (self.screen_w // 2 // CELL) * CELL
        cy = (self.screen_h // 2 // CELL) * CELL
        self.body = [
            (cx, cy),
            (cx - CELL, cy),
            (cx - 2 * CELL, cy)
        ]
        self.direction = (CELL, 0)  # moving right
        self.grow = False

    def change_direction(self, new_dir):
        # Prevent reversing into itself
        opposite = (-new_dir[0], -new_dir[1])
        if opposite != self.direction:
            self.direction = new_dir

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def eat(self):
        self.grow = True

    def check_wall_collision(self):
        hx, hy = self.body[0]
        return (hx < 0 or hx >= self.screen_w or
                hy < 0 or hy >= self.screen_h)

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def get_head(self):
        return self.body[0]

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            color = (0, 200, 80) if i == 0 else (0, 150, 50)
            pygame.draw.rect(surface, color, (*segment, CELL - 2, CELL - 2), border_radius=4)


class Food:
    """Represents the food item - OOP concept"""

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.position = self._random_pos()

    def _random_pos(self):
        cols = self.screen_w // CELL
        rows = self.screen_h // CELL
        x = random.randint(0, cols - 1) * CELL
        y = random.randint(0, rows - 1) * CELL
        return (x, y)

    def respawn(self, snake_body):
        # Don't spawn on the snake
        while True:
            pos = self._random_pos()
            if pos not in snake_body:
                self.position = pos
                break

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, (220, 50, 50), (x, y, CELL - 2, CELL - 2), border_radius=4)
