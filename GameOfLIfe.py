import multiprocessing as mp
import numpy as np
import time
import matplotlib.pyplot as plt
import pygame

def update_subgrid(subgrid, global_grid):
    # Update the cells in the subgrid using a copy of the global grid
    new_subgrid = np.copy(subgrid)
    nrows, ncols = subgrid.shape
    for i in range(0, nrows):
        for j in range(0, ncols):
            # Count the number of alive neighbors
            count = (global_grid[i-1:i+2, j-1:j+2].sum() - global_grid[i, j])
            
            # Handle the edge cells
            if i == 0 and j == 0:
                count = (global_grid[i:i+2, j:j+2].sum() - global_grid[i, j])
            elif i == 0:
                count = (global_grid[i:i+2, j-1:j+2].sum() - global_grid[i, j])
            elif j == 0:
                count = (global_grid[i-1:i+2, j:j+2].sum() - global_grid[i, j])
            elif i == nrows-1 and j == ncols-1:
                count = (global_grid[i-1:i+1, j-1:j+1].sum() - global_grid[i, j])
            elif i == nrows-1:
                count = (global_grid[i-1:i+1, j-1:j+2].sum() - global_grid[i, j])
            elif j == ncols-1:
                count = (global_grid[i-1:i+2, j-1:j+1].sum() - global_grid[i, j])

            #print(count, 'using (i,j)', i, " ", j)
            # Apply the rules of the game
            if global_grid[i, j] == 1 and (count < 2 or count > 3):
                new_subgrid[i, j] = 0
            elif global_grid[i, j] == 0 and count == 3:
                new_subgrid[i, j] = 1

    return new_subgrid

def update_grid(grid, num_processes):
    # Divide the grid into equal-sized subgrids for each process
    nrows, ncols = grid.shape
    subgrid_size = nrows // num_processes
    subgrids = [grid[i*subgrid_size:(i+1)*subgrid_size,:] for i in range(num_processes)]
    # Create a pool of processes and update each subgrid in parallel
    with mp.Pool(processes=num_processes) as pool:
        results = [pool.apply_async(update_subgrid, args=(subgrid, grid)) for subgrid in subgrids]
        updated_subgrids = [result.get() for result in results]
    # Merge the updated subgrids back into the global grid
    for i in range(num_processes):
        grid[i*subgrid_size:(i+1)*subgrid_size,:] = updated_subgrids[i]

def simulate(grid, num_iterations, num_processes):
    # Initialize Pygame
    pygame.init()
    cell_size = 10
    nrows, ncols = grid.shape
    screen_size = (ncols * cell_size, nrows * cell_size)
    screen = pygame.display.set_mode(screen_size)

    # Create a clock to control the frame rate
    clock = pygame.time.Clock()

    # Split the grid into subgrids and create the multiprocessing pool
    subgrid_shape = (nrows//num_processes, ncols)
    pool = mp.Pool(num_processes)

    for iteration in range(num_iterations):
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Update the subgrids using multiprocessing
        subgrids = [grid[i:i+subgrid_shape[0], :] for i in range(0, nrows, subgrid_shape[0])]
        subgrids = [(subgrids[i], grid) for i in range(num_processes)]
        subgrids = pool.starmap(update_subgrid, subgrids)
        grid = np.concatenate(subgrids)

        # Draw the cells on the screen
        for i in range(nrows):
            for j in range(ncols):
                if grid[i, j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (j*cell_size, i*cell_size, cell_size, cell_size))

        # Update the screen and wait for the next frame
        pygame.display.update()
        clock.tick(1)

    # Clean up
    pool.close()
    pool.join()
    pygame.quit()
    return grid

if __name__ == '__main__':
    # Initialize the global grid
    nrows, ncols = 50, 50
    grid = np.random.randint(2, size=(nrows, ncols))
    # Run the game for a fixed number of iterations
    num_iterations = 10
    num_processes = 2

    simulate(grid, num_iterations, num_processes)


    #Print matrix
    # for i in range(num_iterations):
    #     start_time = time.time()
    #     update_grid(grid, num_processes)
    #     end_time = time.time()
    #     print(f"Iteration {i+1}: {end_time-start_time:.3f} seconds")
    #     print(grid)


