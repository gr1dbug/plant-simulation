# Plant Simulation

A 2D physically-based simulation of plant growing with moisture and nutrient diffusion using Python and Pygame.

## Features

- 2D grid-based simulation with soil in the bottom half and air in the top half
- Physically-based diffusion of moisture through soil cells
- Nutrient diffusion along with moisture
- Visualization of moisture (blue) and nutrient (red) levels
- Periodic moisture replenishment to maintain the simulation

## Requirements

- Python 3.10+
- Pygame 2.6.1+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gr1dbug/plant-simulation.git
cd plant-simulation
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install pygame
```

## Running the Simulation

```bash
python src/main.py
```

## How It Works

- The simulation uses a 100x100 grid (100x50 soil cells, 100x50 air cells)
- Each cell is 10x10 pixels
- Soil cells are initialized with random nutrient values (0.0-1.0)
- 100 random soil cells start with a moisture value of 0.9
- Moisture diffuses to surrounding cells each step
- Nutrients are dissolved in moisture and diffuse proportionally
- Cells are colored based on their moisture (blue) and nutrient (red) values
- Moisture is periodically added to random soil cells to maintain the simulation

## License

MIT