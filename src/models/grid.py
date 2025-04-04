import random

class Cell:
    def __init__(self, moisture=0.0, nutrient=0.0):
        self._moisture = max(0.0, min(1.0, moisture))  # Clamp between 0.0 and 1.0
        self._nutrient = max(0.0, min(1.0, nutrient))  # Clamp between 0.0 and 1.0
    
    @property
    def moisture(self):
        return self._moisture
    
    @moisture.setter
    def moisture(self, value):
        self._moisture = max(0.0, min(1.0, value))  # Clamp between 0.0 and 1.0
    
    @property
    def nutrient(self):
        return self._nutrient
    
    @nutrient.setter
    def nutrient(self, value):
        self._nutrient = max(0.0, min(1.0, value))  # Clamp between 0.0 and 1.0

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Initialize the grid with all cells at 0 moisture and 0 nutrient
        self.grid = [[Cell(moisture=0.0, nutrient=0.0) for _ in range(width)]
                    for _ in range(height)]
        
        # Set random nutrient values for soil cells (bottom half)
        for y in range(50, height):
            for x in range(width):
                self.grid[y][x].nutrient = random.uniform(0.0, 1.0)
        
        # Set initial moisture to 0.9 in 100 random soil cells
        moisture_cells = 0
        while moisture_cells < 100:
            x = random.randint(0, width - 1)
            y = random.randint(50, height - 1)  # Only set moisture in the bottom half (soil)
            # Ensure we don't set the same cell twice
            if self.grid[y][x].moisture < 0.9:
                self.grid[y][x].moisture = 0.9
                moisture_cells += 1

    def get_cell(self, x, y):
        return self.grid[y][x]

    def update(self, frame_count=0):
        # Create a copy of the grid to store new values
        new_grid = [[Cell(moisture=self.get_cell(x, y).moisture, nutrient=self.get_cell(x, y).nutrient)
                    for x in range(self.width)] for y in range(self.height)]
        
        # Diffuse moisture and nutrients
        for y in range(self.height):
            for x in range(self.width):
                current = self.get_cell(x, y)
                
                if y >= 50:  # Only diffuse in soil cells (bottom half)
                    # Skip diffusion if moisture is too low
                    if current.moisture <= 0.1:
                        continue
                    
                    # Calculate diffusion to surrounding cells
                    neighbors = []
                    
                    # Add valid neighboring cells
                    if x > 0:
                        neighbors.append((x - 1, y))
                    if x < self.width - 1:
                        neighbors.append((x + 1, y))
                    if y > 50:  # Only diffuse within soil layer
                        neighbors.append((x, y - 1))
                    if y < self.height - 1:
                        neighbors.append((x, y + 1))
                    
                    # Calculate diffusion amount for each neighbor
                    total_neighbors = len(neighbors)
                    if total_neighbors > 0:  # Prevent division by zero
                        # Diffuse 1% of moisture to neighbors (much more conservative)
                        diffusion_rate = 0.01
                        moisture_diffusion_per_neighbor = current.moisture * diffusion_rate / total_neighbors
                        
                        # Calculate total moisture to diffuse
                        total_moisture_diffusion = moisture_diffusion_per_neighbor * total_neighbors
                        
                        # Calculate nutrient ratio (nutrient per unit of moisture)
                        nutrient_ratio = current.nutrient / current.moisture if current.moisture > 0 else 0
                        
                        # Diffuse to neighbors
                        for nx, ny in neighbors:
                            # Only diffuse if the neighbor is a soil cell
                            if ny >= 50:
                                new_grid[ny][nx].moisture += moisture_diffusion_per_neighbor
                                
                                # Nutrient diffuses along with moisture and in proportion to it
                                nutrient_diffusion = moisture_diffusion_per_neighbor * nutrient_ratio
                                new_grid[ny][nx].nutrient += nutrient_diffusion
                        
                        # Update self (subtract total diffusion once)
                        new_grid[y][x].moisture -= total_moisture_diffusion
                        new_grid[y][x].nutrient -= total_moisture_diffusion * nutrient_ratio
        
        # Update the grid with new values
        self.grid = new_grid
        
        # Periodically add more moisture to random soil cells (every 200 frames)
        if frame_count > 0 and frame_count % 200 == 0:
            # Add moisture to 20 random soil cells
            for _ in range(20):
                x = random.randint(0, self.width - 1)
                y = random.randint(50, self.height - 1)
                self.grid[y][x].moisture = min(1.0, self.grid[y][x].moisture + 0.5)