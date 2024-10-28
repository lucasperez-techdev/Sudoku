import pygame

class Cell:
    selected = False
    def __init__(self, row, col, screen):
        self.row = row
        self.col = col
        self.screen = screen
        self.cell_size = 81

        self.y = self.row * self.cell_size
        self.x = self.col * self.cell_size

    def draw(self):
        rect = pygame.Rect(self.x + 18, self.y + 18, 82, 82)
        # If user selects a cell, outline in red
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)

    def set_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.value = value
        # Additional logic for sketching, if needed

    def clear(self):
        self.value = 0
        # Additional logic for clearing, if needed
