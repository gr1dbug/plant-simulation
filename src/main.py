import pygame
from models.grid import Grid

def main():
    # For debugging
    import time
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    width, height = 1000, 1000
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Plant Simulation")
    
    # Create a grid instance
    grid = Grid(width=100, height=100)
    
    # Main loop
    running = True
    frame_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the grid (diffusion of moisture and nutrients)
        grid.update(frame_count)
        
        # Print debug info every 100 frames and when moisture is added
        frame_count += 1
        if frame_count % 100 == 0 or frame_count % 200 == 0:
            # Count cells with moisture > 0.1
            moisture_cells = sum(1 for y in range(grid.height) for x in range(grid.width)
                               if grid.get_cell(x, y).moisture > 0.1)
            
            # Count cells with any moisture
            any_moisture_cells = sum(1 for y in range(grid.height) for x in range(grid.width)
                                  if grid.get_cell(x, y).moisture > 0)
            
            print(f"Frame {frame_count}: Cells with moisture > 0.1: {moisture_cells}, Any moisture: {any_moisture_cells}")
            
            # If moisture was just added
            if frame_count % 200 == 0 and frame_count > 0:
                print(f"Frame {frame_count}: Added moisture to 20 random soil cells")
        
        # Clear the screen
        screen.fill((255, 255, 255))
        
        # Draw the grid
        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.get_cell(x, y)
                
                # Different visualization for air vs soil cells
                if y < 50:  # Air cells (top half)
                    # Air cells are light blue
                    color = (200, 220, 255)
                else:  # Soil cells (bottom half)
                    # Calculate color based on moisture and nutrient levels
                    moisture_value = cell.moisture
                    nutrient_value = cell.nutrient
                    
                    # Base soil color (brown)
                    base_red = 139
                    base_green = 69
                    base_blue = 19
                    
                    # Adjust for moisture (blue component)
                    # Even low moisture should be visible
                    blue_intensity = int(moisture_value * 200)
                    if moisture_value > 0 and blue_intensity == 0:
                        blue_intensity = 20  # Minimum blue for any moisture
                    
                    # Adjust for nutrient (red component)
                    # Even low nutrient should be visible
                    red_intensity = int(nutrient_value * 100) + base_red
                    if nutrient_value > 0 and red_intensity == base_red:
                        red_intensity = base_red + 20  # Minimum red for any nutrient
                    
                    # Combine colors - ensure soil cells are always visible
                    # Even with no moisture or nutrients, they should have the base brown color
                    color = (
                        min(255, max(base_red, red_intensity)),
                        base_green,
                        min(255, max(base_blue, base_blue + blue_intensity))
                    )
                
                # Draw the cell
                pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10), 0)
        
        # Draw a line to separate air and soil (at y=50*10=500)
        pygame.draw.line(screen, (0, 0, 0), (0, 500), (1000, 500), 2)
        
        # Update the display
        pygame.display.flip()
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()