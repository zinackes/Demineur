import pygame
import random

import grid
from grid import Grid

class GridGame:
    def __init__(self, rows, cols, cell_size, window_width, window_height, mines_count, is_replay=False):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.generate_empty_grid()
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.offset_x = (window_width - (cols * cell_size)) // 2
        self.offset_y = (window_height - (rows * cell_size)) // 2
        self.game_over = False
        self.victory = False
        self.first_click = not is_replay  # Désactivé si le jeu est en mode replay
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.mines_count = mines_count
        self.is_replay = is_replay  # Nouveau attribut pour indiquer le mode replay
        self.first_click_position = None
        self.replay_first_click_position = None

    def propagate_zeros(self, row, col, grid_instance, max_propagation):
        """
        Propage toutes les cases de valeur 0 autour d'une case initiale
        avec une limite de propagation définie par max_propagation.
        """
        all_directions = self.directions
        cells_to_check = [(row, col)]
        visited = set()
        propagation_count = 0

        while cells_to_check:
            current_row, current_col = cells_to_check.pop(0)

            if propagation_count >= max_propagation:
                break

            visited.add((current_row, current_col))
            propagation_count += 1

            if 0 <= current_row < self.rows and 0 <= current_col < self.cols:
                self.revealed[current_row][current_col] = True
                self.grid[current_row][current_col] = grid_instance.grid[current_row][current_col]

                if grid_instance.grid[current_row][current_col] == 0:
                    for dr, dc in self.directions:
                        neighbor_row, neighbor_col = current_row + dr, current_col + dc
                        if (neighbor_row, neighbor_col) not in visited:
                            cells_to_check.append((neighbor_row, neighbor_col))

    def draw(self, surface):
        font = pygame.font.Font(None, 40)
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.offset_x + col * self.cell_size,
                    self.offset_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.revealed[row][col]:
                    color = "black"
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)

                    if self.grid[row][col] == -1:
                        pygame.draw.circle(
                            surface,
                            "red",
                            (
                                self.offset_x + col * self.cell_size + self.cell_size // 2,
                                self.offset_y + row * self.cell_size + self.cell_size // 2),
                            self.cell_size // 3
                        )
                    elif self.grid[row][col] > 0:
                        text = font.render(str(self.grid[row][col]), True, "yellow")
                        text_rect = text.get_rect(center=(
                            self.offset_x + col * self.cell_size + self.cell_size // 2,
                            self.offset_y + row * self.cell_size + self.cell_size // 2
                        ))
                        surface.blit(text, text_rect)
                elif self.flags[row][col]:
                    color = "mediumblue"
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)
                    pygame.draw.polygon(
                        surface,
                        "red",
                        [
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + self.cell_size // 4),
                            (self.offset_x + col * self.cell_size + 3 * self.cell_size // 4,
                             self.offset_y + row * self.cell_size + self.cell_size // 3),
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + self.cell_size // 2),
                        ]
                    )
                else:
                    if self.is_replay and self.replay_first_click_position == (row, col):
                        color = "purple"
                    else:
                        color = "mediumblue"
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)

    def changeValue(self, row, col, grid_instance):
        if self.flags[row][col] or self.game_over or self.victory:
            return

        if self.first_click:
            self.first_click = False
            self.first_click_position = (row, col)
            grid_instance.populate_mines_avoiding(row, col, self.mines_count)
            grid_instance.calculate_adjacent_numbers()
            grid_instance.grid[row][col] = 0

        if grid_instance.grid[row][col] == 0:
            self.propagate_zeros(row, col, grid_instance, max_propagation=1000)
        else:
            self.grid[row][col] = grid_instance.grid[row][col]
            self.revealed[row][col] = True

        if grid_instance.grid[row][col] == -1:
            self.game_over = True
            return

        self.check_victory(grid_instance)

    def toggle_flag(self, row, col):
        """Ajoute ou enlève un drapeau sur une case."""
        if not self.revealed[row][col]:
            self.flags[row][col] = not self.flags[row][col]

    def generate_empty_grid(self):
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def check_victory(self, grid_instance):
        for row in range(self.rows):
            for col in range(self.cols):
                if grid_instance.grid[row][col] != -1 and not self.revealed[row][col]:
                    return False
        self.victory = True
        return True
