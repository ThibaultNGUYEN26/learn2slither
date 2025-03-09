import tkinter as tk

# Global variables to hold the snake's state.
snake_coords = []         # A list of (row, col) tuples. Index 0 is the head.
current_direction = "Right"  # The snake's current moving direction.

def move(root, canvas, board_size, canvas_size, draw_snake_func, apple_list, respawn_apple_func, max_length, metric_callback=None, stop_callback=None):
    """
    Moves the snake in the current direction, updates its body,
    checks for apple consumption, collision detection, win condition,
    redraws the snake, and schedules the next move.

    When an apple is eaten, its type is reported via metric_callback.
    When the game is over (collision or win), stop_callback is called.

    Parameters:
      - root: Tkinter root.
      - canvas: The Canvas.
      - board_size: Board dimension.
      - canvas_size: Canvas size in pixels.
      - draw_snake_func: Callback to redraw snake.
      - apple_list: List of apples (row, col, status).
      - respawn_apple_func: Function to spawn a new apple of a given type.
      - max_length: The win condition snake length.
      - metric_callback: Called with apple type when an apple is eaten.
      - stop_callback: Called when game over or win occurs.
    """
    global snake_coords, current_direction

    head_row, head_col = snake_coords[0]

    # Determine new head position.
    if current_direction == "Up":
        new_head = (head_row - 1, head_col)
    elif current_direction == "Down":
        new_head = (head_row + 1, head_col)
    elif current_direction == "Left":
        new_head = (head_row, head_col - 1)
    elif current_direction == "Right":
        new_head = (head_row, head_col + 1)
    else:
        new_head = (head_row, head_col)

    # --- Collision detection ---
    # Wall collision.
    if new_head[0] < 0 or new_head[0] >= board_size or new_head[1] < 0 or new_head[1] >= board_size:
        canvas.create_text(canvas_size/2, canvas_size/2, text="Game Over!",
                           fill="red", font=("Helvetica", 24))
        if stop_callback:
            stop_callback()
        return

    # Self-collision.
    if new_head in snake_coords[:-1]:
        canvas.create_text(canvas_size/2, canvas_size/2, text="Game Over!",
                           fill="red", font=("Helvetica", 24))
        if stop_callback:
            stop_callback()
        return

    # --- Apple eating logic ---
    apple_positions = [(a[0], a[1]) for a in apple_list]
    if new_head in apple_positions:
        apple = next(a for a in apple_list if (a[0], a[1]) == new_head)
        apple_type = apple[2]
        apple_list.remove(apple)
        if metric_callback:
            metric_callback(apple_type)
        if apple_type == "good":
            snake_coords.insert(0, new_head)
        elif apple_type == "bad":
            snake_coords.insert(0, new_head)
            if snake_coords:
                snake_coords.pop()  # normal removal
            if len(snake_coords) > 0:
                snake_coords.pop()  # extra removal
            else:
                canvas.create_text(canvas_size/2, canvas_size/2, text="Game Over!",
                                   fill="red", font=("Helvetica", 24))
                if stop_callback:
                    stop_callback()
                return
        else:
            snake_coords.insert(0, new_head)
            snake_coords.pop()
        root.after(200, lambda: respawn_apple_func(apple_type))
    else:
        snake_coords.insert(0, new_head)
        snake_coords.pop()

    # --- Win condition ---
    if len(snake_coords) >= max_length:
        canvas.create_text(canvas_size/2, canvas_size/2, text="You Win!",
                           fill="green", font=("Helvetica", 24))
        if stop_callback:
            stop_callback()
        return

    draw_snake_func()
    root.after(200, lambda: move(root, canvas, board_size, canvas_size,
                                 draw_snake_func, apple_list, respawn_apple_func, max_length, metric_callback, stop_callback))


def change_direction(event):
    """
    Updates the snake's direction based on arrow key input,
    preventing a direct 180° reversal.
    """
    global current_direction
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    new_direction = event.keysym
    if opposites.get(current_direction) != new_direction:
        current_direction = new_direction
