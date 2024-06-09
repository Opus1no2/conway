import time
import random
import tkinter as tk
from ttkthemes import ThemedTk

window = ThemedTk(theme="black")

cell_size = 10

window.title("Conways Game of Life")


def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.

    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    root = tk.Tk()
    root.update_idletasks()
    root.attributes("-fullscreen", True)
    root.state("iconic")
    geometry = root.winfo_geometry()
    root.destroy()
    return geometry


geometry = get_curr_screen_geometry()
resolution = geometry.split("+")[0]


screen_height = int(resolution.split("x")[1])
screen_width = int(resolution.split("x")[0])

height = (screen_height // cell_size * cell_size) - 200
width = (screen_width // cell_size * cell_size) - 200

window.geometry(f"{width}x{height}+0+0")

canvas = tk.Canvas(window, width=width, height=height, bg="black")


def init_grid(canvas):
    grid = []

    for _ in range(height // cell_size):
        grid.append([0] * (width // cell_size))

    grid = seed_grid(grid)

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell:
                create_cell(j, i, grid, canvas)

    return grid


def seed_grid(grid):
    grid[0][0] = 1
    grid[0][2] = 1
    grid[1][1] = 1
    grid[1][0] = 1
    grid[1][2] = 1
    grid[2][1] = 1
    grid[2][2] = 1
    grid[2][0] = 1
    grid[3][1] = 1
    grid[3][2] = 0
    grid[3][0] = 1
    grid[4][1] = 1

    return grid


def get_cell_neighbors(matrix, x, y):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    neighbors = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append(matrix[nx][ny])

    return neighbors


def live_cell_count(cells):
    return len(list(filter(lambda x: x > 0, cells)))


def random_color():
    r = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (r(), r(), r())


def create_cell(x, y, grid, canvas):
    cell = canvas.create_rectangle(
        x * cell_size,
        y * cell_size,
        x * cell_size + cell_size,
        y * cell_size + cell_size,
        fill=random_color(),
    )
    grid[y][x] = cell

    return cell


def delete_cell(x, y, grid, canvas):
    cell_id = grid[y][x]
    canvas.delete(cell_id)
    grid[y][x] = 0


def main(window, canvas):
    grid = init_grid(canvas)

    canvas.pack()

    while True:
        window.update()

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                cell_neighbors = get_cell_neighbors(grid, i, j)

                if cell > 0:
                    if live_cell_count(cell_neighbors) < 2:
                        delete_cell(j, i, grid, canvas)
                    elif (
                        live_cell_count(cell_neighbors) == 2
                        or live_cell_count(cell_neighbors) == 3
                    ):
                        continue
                    elif live_cell_count(cell_neighbors) > 3:
                        delete_cell(j, i, grid, canvas)
                else:
                    if live_cell_count(cell_neighbors) == 3:
                        create_cell(j, i, grid, canvas)

        canvas.update()

        time.sleep(0.1)


main(window, canvas)
window.mainloop()
