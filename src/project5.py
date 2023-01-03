import pygame
from faller_class import Faller
from field_class import Field
import field_class
import columns_logic
import math

COLUMNS = 6
ROWS = 13
HEIGHT_MARGIN = 15
BORDER = 2

def run() -> None:
    '''Runs the entire Columns game when called'''
    pygame.init()

    surface = pygame.display.set_mode((700, 600), pygame.RESIZABLE)
    field = Field(columns_logic.create_empty_state(ROWS, COLUMNS))

    running = True
    clock = pygame.time.Clock()
    timer = 0 # keeps track of when to drop the faller

    while running:
        clock.tick(100)

        try:
            if field.need_new_faller:
                field.create_faller()

            square_size, top_left_corner = draw_grid(surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        try:
                            field.move_faller_left()
                            delete_entire_faller(surface, field, top_left_corner, square_size)
                        except field_class.InvalidMoveError:
                            pass
                    elif event.key == pygame.K_RIGHT:
                        try:
                            field.move_faller_right()
                            delete_entire_faller(surface, field, top_left_corner, square_size)
                        except field_class.InvalidMoveError:
                            pass
                    elif event.key == pygame.K_DOWN:
                        timer = 100
                    elif event.key == pygame.K_SPACE:
                        field.rotate_faller()

            draw_faller(surface, field, square_size, top_left_corner)

            # drop the faller after one second
            if timer == 100:
                try:
                    field.pass_time()
                    timer = 0
                except field_class.InvalidMoveError:
                    pass
            else:
                timer += 1
            
            pygame.display.flip()
        except field_class.GameOverError:
            running = False

    pygame.quit()

def draw_grid(surface: pygame.Surface):
    '''Draws a 6x13 grid to represent the the empty field'''
    width = surface.get_width()
    height = surface.get_height()

    grid_height = int(height - (2 * HEIGHT_MARGIN))

    square_size = math.floor(grid_height / ROWS)

    width_margin = (width - square_size * COLUMNS) / 2 

    for x in range(0, square_size * COLUMNS, square_size):
        for y in range(0, square_size * ROWS, square_size):
            rect = pygame.Rect(width_margin + x, HEIGHT_MARGIN + y, square_size, square_size)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2)

    top_left_corner = (width_margin, HEIGHT_MARGIN)

    return square_size, top_left_corner

def draw_faller(surface: pygame.Surface, field: Faller, square_size: int|float, top_left_corner: (tuple[int|float])):
    '''Draws the faller on the field as three colored rectangles'''
    # represent each letter as a different color in rgb
    fill_colors = {
        'R': (255, 0, 0),
        'O': (255, 102, 0),
        'Y': (255, 234, 0),
        'G': (0, 255, 0),
        'B': (0, 170, 255),
        'I': (0, 0, 255),
        'P': (166, 0, 255)
        }

    highlights = {
        'R': (255, 122, 122),
        'O': (255, 143, 69),
        'Y': (255, 241, 92),
        'G': (94, 255, 94),
        'B': (105, 205, 255),
        'I': (99, 99, 255),
        'P': (198, 92, 255)
    }

    shadows = {
        'R': (186, 3, 0),
        'O': (196, 79, 0),
        'Y': (161, 147, 0),
        'G': (2, 156, 2),
        'B': (0, 124, 186),
        'I': (0, 0, 166),
        'P': (99, 0, 153)
    }

    faller = field.faller

    for block in range(1, faller.faller_num + 1):
        block -= 1
        color = faller.faller[block][1]
        fill_color = fill_colors[color]

        highlight = highlights[color]
        shadow = shadows[color]
        col_index = faller.faller_col
        
        x = top_left_corner[0] + square_size * col_index 
        y = HEIGHT_MARGIN + square_size * (faller.faller_spot - block - 1)
        
        square = pygame.Rect(x, y, square_size, square_size)
        pygame.draw.rect(surface, fill_color, square, border_radius = 5)
        # draw right border
        pygame.draw.line(surface, shadow, (x + square_size - BORDER, y + BORDER), (x + square_size - BORDER, (y + square_size - BORDER)), 5)
        # draw left border
        pygame.draw.line(surface, highlight, (x + BORDER, y + BORDER + 1), (x + BORDER, (y + square_size - BORDER)), 5)
        # draw top border
        pygame.draw.line(surface, highlight, (x + BORDER + 1, y + BORDER), (x - BORDER + square_size, y + BORDER), 5)
        # draw bottom border
        pygame.draw.line(surface, shadow, (x + BORDER, y + square_size - BORDER), (x + square_size - BORDER, (y + square_size - BORDER)), 5)
        
        delete_previous_blocks(surface, faller, x, y, square_size)

def delete_previous_blocks(surface: pygame.Surface, faller: Faller, x: int | float, y: int | float, square_size: int | float):
    '''Replaces the square right above the faller with a black square if all 3 blocks in the faller have entered the field'''
    if faller.faller_num == 3:
        y -= square_size
        rect = pygame.Rect(x + BORDER, y + BORDER, square_size - 4, square_size - 4)
        pygame.draw.rect(surface, (0, 0, 0), rect)

def delete_entire_faller(surface: pygame.Surface, field: Field, top_left_corner: (tuple[int|float]), square_size: int | float):
    '''Replaces each square that does not have a frozen block in it with a black square of square_size width'''
    field = field.field
    for col in range(COLUMNS):
        for row in range(ROWS):
            if field[col][row] == '   ':
                x = top_left_corner[0] + square_size * col
                y = HEIGHT_MARGIN + square_size * row
                _draw_black_box(surface, x, y, square_size)

def _draw_black_box(surface: pygame.Surface, x: int | float, y: int | float, square_size: int | float):
    '''Draws a black square of square_size width at the coord (x, y) on the given surface'''
    rect = pygame.Rect(x + BORDER, y + BORDER, square_size - 4, square_size - 4)
    pygame.draw.rect(surface, (0, 0, 0), rect)
        
if __name__ == '__main__':
    run()
