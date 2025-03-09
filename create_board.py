def create_board(canvas, board_size=10, canvas_size=500):
    """
    Draws a board on the given canvas.

    Parameters:
    - canvas: The Tkinter Canvas on which to draw.
    - board_size: Number of rows and columns (default is 10).
    - canvas_size: Size (in pixels) of the canvas (default is 500).
    """
    cell_size = canvas_size / board_size
    for row in range(board_size):
        for col in range(board_size):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            canvas.create_rectangle(x0, y0, x1, y1, outline="white", fill="black")
