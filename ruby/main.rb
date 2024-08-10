require 'tk'


def init()
  root = TkRoot.new { title "Conways Game of Life" }

  canvas = TkCanvas.new(root) do
    width  500
    height 500
    background "black"
    pack
  end
  grid = Array.new(50) { Array.new(50) { 0 } }

  [grid, canvas]
end

def seed_grid(grid)
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
end

def fill_cells(grid, canvas, x, y, color="white")
  TkcRectangle.new(canvas, x*10, y*10, x*10+10, y*10+10) do
    fill color
  end
  canvas.update
end

def draw_grid(grid, canvas)
  grid.each_with_index do |row, i|
    row.each_with_index do |cell, j|
      fill_cells(grid, canvas, i, j) if cell == 1
      fill_cells(grid, canvas, i, j, "black") if cell == 0
    end
  end

  draw_grid(grid, canvas)
end


def neighbor_count(grid, x, y)
  neighbors = 0
  (x-1..x+1).each do |i|
    (y-1..y+1).each do |j|
      next if i < 0 || j < 0 || i >= grid.length || j >= grid[0].length
      next if i == x && j == y
      neighbors += grid[i][j]
    end
  end
  neighbors
end

def main()
  grid, canvas = init()
  seed_grid(grid)

  loop do
    grid.each_with_index do |row, i|
      row.each_with_index do |cell, j|
        neighbors = neighbor_count(grid, i, j)
        if cell == 1
          if neighbors < 2 || neighbors > 3
            grid[i][j] = 0
            fill_cells(grid, canvas, i, j, "black")
          end
        else
          if neighbors == 3
            grid[i][j] = 1
            fill_cells(grid, canvas, i, j)
          end
        end
      end
    end

    sleep 0.1
  end
  Tk.mainloop
end

main()

