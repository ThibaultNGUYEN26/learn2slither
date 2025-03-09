import random

def put_apple(canvas, board_size, row, col, canvas_size, status):
    """
    Draws an apple that is smaller than a board cell and centered in the specified board cell.

    Parameters:
    - canvas: The Tkinter Canvas on which to draw.
    - board_size: Number of rows and columns in the board.
    - row: The row index for the cell (starting at 0).
    - col: The column index for the cell (starting at 0).
    - canvas_size: Size (in pixels) of the canvas.
    - status: 'good' for a green apple, 'bad' for a red apple.
    """
    # Calculate the size of each board cell
    cell_size = canvas_size / board_size

    # Define apple size as 30% of the cell size
    apple_size = cell_size * 0.3

    # Calculate the top-left coordinate of the specified cell
    cell_x0 = col * cell_size
    cell_y0 = row * cell_size

    # Find the center of that cell
    center_x = cell_x0 + cell_size / 2
    center_y = cell_y0 + cell_size / 2

    # Calculate coordinates for the apple rectangle so that it's centered in the cell
    x0 = center_x - apple_size / 2
    y0 = center_y - apple_size / 2
    x1 = center_x + apple_size / 2
    y1 = center_y + apple_size / 2

    if status == 'good':
        canvas.create_oval(x0, y0, x1, y1, outline="black", fill="green", tags="apple")
    else:
        canvas.create_oval(x0, y0, x1, y1, outline="black", fill="red", tags="apple")
