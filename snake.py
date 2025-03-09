import random

def draw_snake(canvas, canvas_size, board_size, snake_coords):
    """Redraws the snake using the same style as your snake() function."""
    canvas.delete("snake")
    cell_size = canvas_size / board_size
    body_size = cell_size * 0.35  # body segments size
    head_size = cell_size * 0.45  # head size
    snake_color = "blue"
    for index, (row, col) in enumerate(snake_coords):
        cell_x0 = col * cell_size
        cell_y0 = row * cell_size
        center_x = cell_x0 + cell_size / 2
        center_y = cell_y0 + cell_size / 2
        size = head_size if index == 0 else body_size
        x0 = center_x - size / 2
        y0 = center_y - size / 2
        x1 = center_x + size / 2
        y1 = center_y + size / 2
        canvas.create_oval(x0, y0, x1, y1, outline="black", fill=snake_color, tags="snake")

def random_snake_position(board_size):
    """
    Returns a valid random starting position (head cell) and direction
    for a snake of length `snake_length`. The head is placed in the
    inner area of the board (2..board_size-3), ensuring enough space
    to avoid immediate collisions, and direction is chosen randomly.

    Assumes board_size >= 5.

    Returns:
    A tuple (start_row, start_col, direction).
    """
    directions = ["up", "down", "left", "right"]

    # Pick a random row/column at least 2 cells away from the edges
    start_row = random.randint(2, board_size - 3)
    start_col = random.randint(2, board_size - 3)

    # Pick a random direction
    direction = random.choice(directions)

    return start_row, start_col, direction
