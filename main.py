import tkinter as tk
import random
import time
from create_board import create_board
from random_apple import put_apple
from snake import random_snake_position, draw_snake
import move  # Import the complete move module

# Global metrics dictionary.
metrics = {
    "green": 0,
    "red": 0,
    "up": 0,
    "down": 0,
    "left": 0,
    "right": 0
}
start_time = None  # Will be set when the game starts.
game_active = False  # Flag to indicate if the game is running.

# Global variable for win condition.
win_condition = None

def start_game(board_size, max_length, ai_enabled):
    global start_time, game_active, win_condition
    win_condition = max_length  # Save win condition.
    # Hide the menu.
    menu_frame.place_forget()
    # Show the game container (which includes the game canvas and metrics frame).
    game_container.place(relx=0.417, rely=0.5, width=800, height=600, anchor="center")

    game_active = True
    canvas_size = 501  # Canvas size in pixels.

    # Create the game canvas on the left side.
    game_canvas = tk.Canvas(game_container, width=canvas_size, height=canvas_size, bg="white")
    game_canvas.place(relx=0.5, rely=0.5, anchor="center")

    # Create the board.
    create_board(game_canvas, board_size=board_size, canvas_size=canvas_size-1)

    # --- Setup apples ---
    apple_list = []
    all_cells = [(r, c) for r in range(board_size) for c in range(board_size)]
    apple_positions = random.sample(all_cells, 3)
    apple_list.append((apple_positions[0][0], apple_positions[0][1], "good"))
    apple_list.append((apple_positions[1][0], apple_positions[1][1], "good"))
    apple_list.append((apple_positions[2][0], apple_positions[2][1], "bad"))

    def redraw_apples():
        game_canvas.delete("apple")
        for (r, c, status) in apple_list:
            put_apple(game_canvas, board_size=board_size, row=r, col=c,
                      canvas_size=canvas_size-1, status=status)

    def respawn_apple(apple_type):
        all_cells = [(r, c) for r in range(board_size) for c in range(board_size)]
        snake_cells = set(move.snake_coords)
        current_apples = set((a[0], a[1]) for a in apple_list)
        occupied = snake_cells.union(current_apples)
        available = [cell for cell in all_cells if cell not in occupied]
        if not available:
            return
        new_cell = random.choice(available)
        apple_list.append((new_cell[0], new_cell[1], apple_type))
        redraw_apples()

    # --- Initialize the snake ---
    start_row, start_col, ext_direction = random_snake_position(board_size)
    move.current_direction = "Left"
    move.snake_coords = [(start_row, start_col + i) for i in range(3)]
    draw_snake(game_canvas, canvas_size, board_size, move.snake_coords)
    redraw_apples()

    # Reset metrics and start timer.
    for key in metrics:
        metrics[key] = 0
    start_time = time.time()
    update_metrics_display()

    def stop_game():
        global game_active
        game_active = False
        root.unbind("<Up>")
        root.unbind("<Down>")
        root.unbind("<Left>")
        root.unbind("<Right>")

    def arrow_handler(event):
        if game_active and event.keysym.lower() in metrics:
            metrics[event.keysym.lower()] += 1
            move.change_direction(event)
    root.bind("<Up>", arrow_handler)
    root.bind("<Down>", arrow_handler)
    root.bind("<Left>", arrow_handler)
    root.bind("<Right>", arrow_handler)
    root.bind("<Escape>", lambda e: root.destroy())

    def metric_callback(apple_type):
        if apple_type == "good":
            metrics["green"] += 1
        elif apple_type == "bad":
            metrics["red"] += 1

    move.move(root, game_canvas, board_size, canvas_size,
              lambda: draw_snake(game_canvas, canvas_size, board_size, move.snake_coords),
              apple_list, respawn_apple, max_length, metric_callback, stop_game)

def update_metrics_display():
    if not game_active:
        return  # Stop updating when game is over.
    elapsed = int(time.time() - start_time) if start_time else 0
    score = len(move.snake_coords)
    score_label.config(text=f"Score: {score}")
    green_label.config(text=f"Green apple: {metrics['green']}")
    red_label.config(text=f"Red apple: {metrics['red']}")
    up_label.config(text=f"Up: {metrics['up']}")
    down_label.config(text=f"Down: {metrics['down']}")
    left_label.config(text=f"Left: {metrics['left']}")
    right_label.config(text=f"Right: {metrics['right']}")
    timer_label.config(text=f"Timer: {elapsed} sec")
    if win_condition is not None:
        max_length_label.config(text=f"Max Length: {win_condition}")
    root.after(1000, update_metrics_display)

# --- Main window and menu setup ---
root = tk.Tk()
root.title("Learn2Slither")
root.config(bg="black")
root.geometry("900x700")  # Increase width to accommodate game and metrics side by side.
root.minsize(700, 550)

# Menu frame.
menu_frame = tk.Frame(root, bg="gray")
menu_frame.place(relx=0.5, rely=0.5, anchor="center")

# Create a container frame to hold both the game canvas and the metrics frame.
game_container = tk.Frame(root, bg="black")

# Metrics frame (initially hidden; will be packed to the right of the game).
metrics_frame = tk.Frame(game_container, bg="black", bd=2, relief="solid",
                          highlightbackground="white", highlightthickness=2)
metrics_frame.pack(side="right", fill="y", padx=30, pady=48)

score_label = tk.Label(metrics_frame, text="Score: 0", bg="black", fg="white")
score_label.pack(pady=2)
max_length_label = tk.Label(metrics_frame, text="Max Length: 0", bg="black", fg="white")
max_length_label.pack(pady=2)
green_label = tk.Label(metrics_frame, text="Green apple: 0", bg="black", fg="white")
green_label.pack(pady=2)
red_label = tk.Label(metrics_frame, text="Red apple: 0", bg="black", fg="white")
red_label.pack(pady=2)
up_label = tk.Label(metrics_frame, text="Up: 0", bg="black", fg="white")
up_label.pack(pady=2)
down_label = tk.Label(metrics_frame, text="Down: 0", bg="black", fg="white")
down_label.pack(pady=2)
left_label = tk.Label(metrics_frame, text="Left: 0", bg="black", fg="white")
left_label.pack(pady=2)
right_label = tk.Label(metrics_frame, text="Right: 0", bg="black", fg="white")
right_label.pack(pady=2)
timer_label = tk.Label(metrics_frame, text="Timer: 0 sec", bg="black", fg="white")
timer_label.pack(pady=2)

# Create IntVars for menu options.
board_size_var = tk.IntVar(value=10)
max_length_var = tk.IntVar(value=15)

# Board size option.
tk.Label(menu_frame, text="Board Size (5-20):", bg="gray", fg="white")\
    .grid(row=0, column=0, padx=5, pady=5)
board_size_spinbox = tk.Spinbox(menu_frame, from_=5, to=20, width=5, textvariable=board_size_var)
board_size_spinbox.grid(row=0, column=1, padx=5, pady=5)

# Max length option.
tk.Label(menu_frame, text="Max Length (Win condition):", bg="gray", fg="white")\
    .grid(row=1, column=0, padx=5, pady=5)
max_length_spinbox = tk.Spinbox(menu_frame, from_=5,
                                to=(board_size_var.get()*9 if board_size_var.get() != 5 else 5),
                                width=5, textvariable=max_length_var)
max_length_spinbox.grid(row=1, column=1, padx=5, pady=5)

# AI option (placeholder).
tk.Label(menu_frame, text="AI (Not Implemented):", bg="gray", fg="white")\
    .grid(row=2, column=0, padx=5, pady=5)
ai_var = tk.IntVar()
ai_checkbox = tk.Checkbutton(menu_frame, variable=ai_var, state="disabled", bg="gray", fg="white")
ai_checkbox.grid(row=2, column=1, padx=5, pady=5)

# Play button.
play_button = tk.Button(menu_frame, text="Play",
                        command=lambda: start_game(int(board_size_spinbox.get()),
                                                   int(max_length_spinbox.get()),
                                                   ai_var.get()))
play_button.grid(row=3, column=0, columnspan=2, pady=10)

def update_max_length(*args):
    bs = board_size_var.get()
    max_to = 5 if bs == 5 else bs * 9
    max_length_spinbox.config(to=max_to)
    if max_length_var.get() > max_to:
        max_length_var.set(max_to)
    validate_inputs()

def validate_inputs(*args):
    try:
        bs = board_size_var.get()
        ml = max_length_var.get()
    except Exception:
        play_button.config(state="disabled")
        return
    if not (5 <= bs <= 20):
        valid = False
    elif bs == 5 and ml != 5:
        valid = False
    elif not (5 <= ml <= (bs * 9 if bs != 5 else 5)):
        valid = False
    else:
        valid = True
    play_button.config(state="normal" if valid else "disabled")

board_size_var.trace_add("write", update_max_length)
board_size_var.trace_add("write", validate_inputs)
max_length_var.trace_add("write", validate_inputs)
validate_inputs()

root.mainloop()
