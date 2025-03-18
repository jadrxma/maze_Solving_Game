import streamlit as st
import pygame
import numpy as np
import random
import time
from pygame import gfxdraw
import io
from PIL import Image
import imageio
import base64
from datetime import datetime

# Main Streamlit app initialization
if 'download_video_displayed' not in st.session_state:
    st.session_state.download_video_displayed = False

# Display download video section if we have frames but no recording is active
if ('frames' in st.session_state and st.session_state.frames and 
    ('recording' not in st.session_state or not st.session_state.recording) and
    not st.session_state.download_video_displayed):
    
    st.markdown("""
    <div style="border: 3px solid #00FF00; background-color: #001100; padding: 15px; margin: 20px 0; font-family: 'Courier New', monospace; text-align: center;">
    <h2 style="color: #00FF00; margin-bottom: 10px;">■ RECORDED VIDEO AVAILABLE ■</h2>
    <p style="color: #00FF00;">You can download the maze recording below</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'record_fps' in st.session_state:
        fps = st.session_state.record_fps
    else:
        fps = 10
    
    with st.spinner("Encoding video..."):
        video_bytes, filename = create_video_from_frames(st.session_state.frames, fps=fps)
        
        if video_bytes:
            st.success(f"✅ Video created successfully! ({len(video_bytes) / 1024:.1f} KB)")
            
            # Display prominent download button
            st.markdown(
                get_binary_file_downloader_html(video_bytes, filename, "DOWNLOAD RECORDING"),
                unsafe_allow_html=True
            )
            
            # Add information about the recording
            st.markdown(f"""
            <div style="font-family: 'Courier New', monospace; color: #00FF00; margin-top: 10px; padding: 10px; background-color: #001100; border: 1px solid #00FF00;">
            <code>root@terminal:~$ file {filename}</code><br>
            <code>{filename}: MP4 video, {len(st.session_state.frames)} frames @ {fps} FPS, {len(video_bytes) / 1024:.1f} KB</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.download_video_displayed = True

# Apply hacker theme to the entire app
st.markdown("""
<style>
    body {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .reportview-container {
        background-color: #000000;
        color: #00FF00;
    }
    .sidebar .sidebar-content {
        background-color: #000000;
        color: #00FF00;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00FF00 !important;
        font-family: 'Courier New', monospace;
    }
    .stApp {
        background-color: #000000;
    }
    .stMarkdown {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stText {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stButton>button:hover {
        background-color: #00FF00;
        color: #000000;
    }
    .stTextInput>div>div>input {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stTextInput>label {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stSlider>div>div>div {
        background-color: #00FF00;
    }
    .stSlider>div>div {
        background-color: #006600;
    }
    .stSlider>div {
        color: #00FF00;
    }
    .stSelectbox>div>div {
        background-color: #000000;
        color: #00FF00;
        border: 1px solid #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stSelectbox>label {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    div[data-baseweb="select"] {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    div[role="listbox"] {
        background-color: #000000;
        border: 1px solid #00FF00;
    }
    div[role="option"] {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    div[role="option"]:hover {
        background-color: #003300;
    }
    .stRadio>div {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stRadio>label {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .stCheckbox>div {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    .main {
        background-color: #000000;
    }
    .css-18e3th9 {
        background-color: #000000;
    }
    .css-1d391kg {
        background-color: #000000;
    }
    .block-container {
        background-color: #000000;
    }
    
    /* Custom styles for the terminal look */
    .terminal-text {
        color: #00FF00;
        font-family: 'Courier New', monospace;
        border-bottom: 1px solid #00FF00;
        animation: cursor-blink 1s step-end infinite;
    }
    
    @keyframes cursor-blink {
        0%, 100% { border-color: transparent }
        50% { border-color: #00FF00 }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Streamlit app
st.title("TERMINAL MAZE INFILTRATOR")
st.markdown("""
```
 ____  _____ ____ _   _ ____  ___ _______   __
/ ___|| ____/ ___| | | |  _ \|_ _|_   _\ \ / /
\___ \|  _|| |   | | | | |_) || |  | |  \ V / 
 ___) | |__| |___| |_| |  _ < | |  | |   | |  
|____/|_____\____|\___/|_| \_\___| |_|   |_|  
     _____ ____  ___ ____    ____ _____ _____ _   _ 
    |  ___|  _ \|_ _|  _ \  / ___|_   _| ____| \ | |
    | |_  | |_) || || | | | \___ \ | | |  _| |  \| |
    |  _| |  _ < | || |_| |  ___) || | | |___| |\  |
    |_|   |_| \_\___|____/  |____/ |_| |_____|_| \_|
```
>_System: Initializing security grid breach protocol. Select parameters for infiltration.
""")

# Terminal theme colors - with enhanced contrast
BACKGROUND_COLOR = (0, 0, 0)       # Black
GREEN_BRIGHT = (0, 255, 0)         # Bright terminal green
GREEN_MEDIUM = (0, 150, 0)         # Medium terminal green
GREEN_DARK = (0, 50, 0)            # Dark terminal green
GREEN_VERY_DARK = (0, 20, 0)       # Very dark green for unsolved cells
HIGHLIGHT_COLOR = (0, 255, 100)    # Bright green for active cells
PATH_COLOR = (100, 255, 100)       # Light green for path
SOLVING_COLOR = (150, 255, 50)     # Bright green-yellow for active solving
WALL_COLOR = GREEN_BRIGHT          # Walls are bright green

# Create hacker-style parameter section
st.markdown("""
<div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; margin-bottom: 20px; font-family: 'Courier New', monospace;">
<span style="color: #00FF00;">[CONFIG]</span> System Parameters
</div>
""", unsafe_allow_html=True)

# Set up maze parameters
col1, col2 = st.columns(2)
with col1:
    maze_width = st.slider("Grid Width [X]", 5, 50, 20)
with col2:
    maze_height = st.slider("Grid Height [Y]", 5, 50, 20)

# Algorithm selection
st.markdown("""
<div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; margin-bottom: 20px; font-family: 'Courier New', monospace;">
<span style="color: #00FF00;">[ALGORITHMS]</span> Protocol Selection
</div>
""", unsafe_allow_html=True)

generation_algorithm = st.selectbox(
    "Generation Protocol",
    ["Recursive Backtracking", "Kruskal's Algorithm", "Prim's Algorithm"]
)

mode = st.radio(
    "Execution Mode",
    ["Automatic Breach", "Manual Infiltration"]
)

if mode == "Automatic Breach":
    solving_algorithm = st.selectbox(
        "Breach Protocol",
        ["Depth-First Search", "Breadth-First Search", "A* Algorithm"]
    )

cell_size = 20
wall_thickness = 2

# Set up pygame surface
def init_pygame_surface(width, height):
    pygame.init()
    surface = pygame.Surface((width * cell_size, height * cell_size))
    surface.fill(BACKGROUND_COLOR)
    return surface

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.path = False
        self.solution = False
        self.player = False
        self.goal = False
        self.breadcrumb = False

    def draw(self, surface):
        x, y = self.x * cell_size, self.y * cell_size
        
        # Fill cell based on state - with enhanced visibility for solving process
        if self.player:
            # Player cell - bright green fill 
            pygame.draw.rect(surface, GREEN_MEDIUM, (x, y, cell_size, cell_size))
            # Draw player as a cursor
            if time.time() % 1 > 0.5:  # Blinking effect
                pygame.draw.rect(surface, GREEN_BRIGHT, (x + cell_size // 3, y + cell_size // 3, 
                                                    cell_size // 3, cell_size - cell_size // 1.5))
        elif self.goal:
            # Goal cell - filled with bright green
            pygame.draw.rect(surface, GREEN_MEDIUM, (x, y, cell_size, cell_size))
            # Simple ">" symbol
            points = [
                (x + cell_size // 3, y + cell_size // 2),
                (x + 2 * cell_size // 3, y + cell_size // 3),
                (x + 2 * cell_size // 3, y + 2 * cell_size // 3)
            ]
            pygame.draw.polygon(surface, GREEN_BRIGHT, points)
        elif self.solution:
            # Solution path - very bright green for high visibility
            pygame.draw.rect(surface, PATH_COLOR, (x, y, cell_size, cell_size))
            # Add a center marker to make the solution path more visible
            pygame.draw.rect(surface, GREEN_BRIGHT, 
                          (x + cell_size // 4, y + cell_size // 4, 
                           cell_size // 2, cell_size // 2))
        elif self.path:
            # Current exploration path - bright yellow-green to show active solving
            pygame.draw.rect(surface, SOLVING_COLOR, (x, y, cell_size, cell_size))
        elif self.breadcrumb:
            # Breadcrumb trail - medium green
            pygame.draw.rect(surface, GREEN_MEDIUM, (x, y, cell_size, cell_size))
            # Small dot in center
            pygame.draw.circle(surface, GREEN_BRIGHT, 
                             (x + cell_size // 2, y + cell_size // 2), cell_size // 6)
        elif self.visited:
            # Visited cells - medium green fill
            pygame.draw.rect(surface, GREEN_MEDIUM, (x, y, cell_size, cell_size))
        else:
            # Unvisited/unsolved cells - very dark green fill
            pygame.draw.rect(surface, GREEN_VERY_DARK, (x, y, cell_size, cell_size))
        
        # Draw walls - bright green lines
        if self.walls["top"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y), (x + cell_size, y), wall_thickness)
        if self.walls["right"]:
            pygame.draw.line(surface, WALL_COLOR, (x + cell_size, y), (x + cell_size, y + cell_size), wall_thickness)
        if self.walls["bottom"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y + cell_size), (x + cell_size, y + cell_size), wall_thickness)
        if self.walls["left"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y), (x, y + cell_size), wall_thickness)
        
        # Draw walls - classic terminal green lines
        if self.walls["top"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y), (x + cell_size, y), wall_thickness)
        if self.walls["right"]:
            pygame.draw.line(surface, WALL_COLOR, (x + cell_size, y), (x + cell_size, y + cell_size), wall_thickness)
        if self.walls["bottom"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y + cell_size), (x + cell_size, y + cell_size), wall_thickness)
        if self.walls["left"]:
            pygame.draw.line(surface, WALL_COLOR, (x, y), (x, y + cell_size), wall_thickness)

def remove_walls(current, next_cell):
    """Remove walls between two adjacent cells"""
    dx = current.x - next_cell.x
    dy = current.y - next_cell.y
    
    if dx == 1:  # Next is to the left of current
        current.walls["left"] = False
        next_cell.walls["right"] = False
    elif dx == -1:  # Next is to the right of current
        current.walls["right"] = False
        next_cell.walls["left"] = False
    elif dy == 1:  # Next is above current
        current.walls["top"] = False
        next_cell.walls["bottom"] = False
    elif dy == -1:  # Next is below current
        current.walls["bottom"] = False
        next_cell.walls["top"] = False

# Maze generation algorithms
def recursive_backtracking(grid, width, height, surface, placeholder):
    stack = []
    current = grid[0][0]
    current.visited = True
    stack.append(current)
    
    while stack:
        current = stack[-1]
        current.path = True
        
        # Draw current state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update Streamlit with current state
        update_streamlit(surface, placeholder)
        
        # Remove path highlighting from current cell
        current.path = False
        
        # Find unvisited neighbors
        neighbors = []
        x, y = current.x, current.y
        
        # Check neighbors
        if x > 0 and not grid[y][x - 1].visited:  # Left
            neighbors.append(grid[y][x - 1])
        if x < width - 1 and not grid[y][x + 1].visited:  # Right
            neighbors.append(grid[y][x + 1])
        if y > 0 and not grid[y - 1][x].visited:  # Top
            neighbors.append(grid[y - 1][x])
        if y < height - 1 and not grid[y + 1][x].visited:  # Bottom
            neighbors.append(grid[y + 1][x])
        
        if neighbors:
            next_cell = random.choice(neighbors)
            next_cell.visited = True
            
            # Remove walls between current and next
            remove_walls(current, next_cell)
            
            # Add next to stack
            stack.append(next_cell)
        else:
            # Backtrack
            stack.pop()
            
        time.sleep(0.01)  # Small delay to make visualization visible

def kruskals_algorithm(grid, width, height, surface, placeholder):
    """Implementation of Kruskal's algorithm for maze generation"""
    # Initialize disjoint set
    sets = {}
    for y in range(height):
        for x in range(width):
            sets[(x, y)] = (x, y)
    
    # Initialize edges
    edges = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:  # Add right edge
                edges.append(((x, y), (x + 1, y)))
            if y < height - 1:  # Add bottom edge
                edges.append(((x, y), (x, y + 1)))
    
    # Shuffle edges
    random.shuffle(edges)
    
    # Find function for disjoint set
    def find(pos):
        if sets[pos] != pos:
            sets[pos] = find(sets[pos])
        return sets[pos]
    
    # Union function for disjoint set
    def union(pos1, pos2):
        sets[find(pos1)] = find(pos2)
    
    # Kruskal's algorithm
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        
        # Highlight current cells
        grid[y1][x1].path = True
        grid[y2][x2].path = True
        
        # Draw current state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update Streamlit with current state
        update_streamlit(surface, placeholder)
        
        # Remove path highlighting
        grid[y1][x1].path = False
        grid[y2][x2].path = False
        
        # Check if cells are already connected
        if find((x1, y1)) != find((x2, y2)):
            # Mark both cells as visited
            grid[y1][x1].visited = True
            grid[y2][x2].visited = True
            
            # Remove walls between cells
            if x1 == x2:  # Vertical edge
                if y1 > y2:  # First cell is below second
                    grid[y1][x1].walls["top"] = False
                    grid[y2][x2].walls["bottom"] = False
                else:  # First cell is above second
                    grid[y1][x1].walls["bottom"] = False
                    grid[y2][x2].walls["top"] = False
            else:  # Horizontal edge
                if x1 > x2:  # First cell is to the right of second
                    grid[y1][x1].walls["left"] = False
                    grid[y2][x2].walls["right"] = False
                else:  # First cell is to the left of second
                    grid[y1][x1].walls["right"] = False
                    grid[y2][x2].walls["left"] = False
            
            # Merge sets
            union((x1, y1), (x2, y2))
        
        time.sleep(0.01)  # Small delay to make visualization visible

def prims_algorithm(grid, width, height, surface, placeholder):
    # Start with a random cell
    start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
    grid[start_y][start_x].visited = True
    
    # Walls list - contains walls that connect a visited cell to an unvisited cell
    walls = []
    
    # Add walls of the starting cell
    if start_x > 0:  # Left
        walls.append(((start_x, start_y), (start_x - 1, start_y)))
    if start_x < width - 1:  # Right
        walls.append(((start_x, start_y), (start_x + 1, start_y)))
    if start_y > 0:  # Top
        walls.append(((start_x, start_y), (start_x, start_y - 1)))
    if start_y < height - 1:  # Bottom
        walls.append(((start_x, start_y), (start_x, start_y + 1)))
    
    # Continue until there are no walls left
    while walls:
        # Pick a random wall
        wall = random.choice(walls)
        walls.remove(wall)
        
        (x1, y1), (x2, y2) = wall
        
        # Highlight current cells
        grid[y1][x1].path = True
        if 0 <= x2 < width and 0 <= y2 < height:
            grid[y2][x2].path = True
        
        # Draw current state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update Streamlit with current state
        update_streamlit(surface, placeholder)
        
        # Remove path highlighting
        grid[y1][x1].path = False
        if 0 <= x2 < width and 0 <= y2 < height:
            grid[y2][x2].path = False
        
        # Check if only one cell is visited
        if (grid[y1][x1].visited and not grid[y2][x2].visited) or \
           (not grid[y1][x1].visited and grid[y2][x2].visited):
            
            # Make sure cell2 is the unvisited one
            if grid[y1][x1].visited:
                visited_cell, unvisited_cell = (x1, y1), (x2, y2)
            else:
                visited_cell, unvisited_cell = (x2, y2), (x1, y1)
            
            # Mark unvisited as visited
            grid[unvisited_cell[1]][unvisited_cell[0]].visited = True
            
            # Remove walls between cells
            if unvisited_cell[0] == visited_cell[0]:  # Vertical connection
                if unvisited_cell[1] > visited_cell[1]:  # Unvisited is below visited
                    grid[visited_cell[1]][visited_cell[0]].walls["bottom"] = False
                    grid[unvisited_cell[1]][unvisited_cell[0]].walls["top"] = False
                else:  # Unvisited is above visited
                    grid[visited_cell[1]][visited_cell[0]].walls["top"] = False
                    grid[unvisited_cell[1]][unvisited_cell[0]].walls["bottom"] = False
            else:  # Horizontal connection
                if unvisited_cell[0] > visited_cell[0]:  # Unvisited is to the right of visited
                    grid[visited_cell[1]][visited_cell[0]].walls["right"] = False
                    grid[unvisited_cell[1]][unvisited_cell[0]].walls["left"] = False
                else:  # Unvisited is to the left of visited
                    grid[visited_cell[1]][visited_cell[0]].walls["left"] = False
                    grid[unvisited_cell[1]][unvisited_cell[0]].walls["right"] = False
            
            # Add walls of the unvisited cell
            x, y = unvisited_cell
            if x > 0 and not grid[y][x - 1].visited:  # Left
                walls.append(((x, y), (x - 1, y)))
            if x < width - 1 and not grid[y][x + 1].visited:  # Right
                walls.append(((x, y), (x + 1, y)))
            if y > 0 and not grid[y - 1][x].visited:  # Top
                walls.append(((x, y), (x, y - 1)))
            if y < height - 1 and not grid[y + 1][x].visited:  # Bottom
                walls.append(((x, y), (x, y + 1)))
        
        time.sleep(0.01)  # Small delay to make visualization visible

# Maze solving algorithms
def depth_first_search(grid, width, height, surface, placeholder):
    """Depth-first search algorithm for maze solving"""
    start = grid[0][0]
    end = grid[height - 1][width - 1]
    
    # Progress display for Streamlit
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stack = [(start, [])]
    visited = set()
    
    steps = 0
    max_steps = width * height * 2  # Approximate max steps
    
    while stack:
        steps += 1
        
        # Update progress bar
        progress = min(steps / max_steps, 0.99)
        progress_bar.progress(progress)
        status_text.text(f"DFS Search: Exploring cell {steps}")
        
        current, path = stack.pop()
        
        # Skip if already visited
        if (current.x, current.y) in visited:
            continue
            
        # Mark as visited
        visited.add((current.x, current.y))
        
        # Highlight current cell being explored
        current.path = True
        
        # Reset all previously explored cells to normal visited state
        for row in grid:
            for cell in row:
                if cell != current and (cell.x, cell.y) in visited and not cell.solution:
                    cell.path = False
        
        # Draw current state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update Streamlit with current state
        update_streamlit(surface, placeholder)
        
        # Check if we reached the end
        if current == end:
            # Visualize solution path
            for cell in path + [current]:
                cell.solution = True
                cell.path = False
            
            # Draw final solution
            for row in grid:
                for cell in row:
                    cell.draw(surface)
            
            update_streamlit(surface, placeholder)
            
            # Complete the progress bar
            progress_bar.progress(1.0)
            status_text.text(f"Solution found in {steps} steps!")
            
            print(f"DFS found solution in {steps} steps")
            return True
        
        # Get possible moves
        neighbors = []
        x, y = current.x, current.y
        
        # Check each direction - in reverse order for DFS visualization
        if not current.walls["bottom"] and (x, y + 1) not in visited:
            neighbors.append(grid[y + 1][x])
        if not current.walls["top"] and (x, y - 1) not in visited:
            neighbors.append(grid[y - 1][x])
        if not current.walls["right"] and (x + 1, y) not in visited:
            neighbors.append(grid[y][x + 1])
        if not current.walls["left"] and (x - 1, y) not in visited:
            neighbors.append(grid[y][x - 1])
        
        # Add neighbors to stack
        for neighbor in neighbors:
            stack.append((neighbor, path + [current]))
            
            # Briefly highlight the neighbor being considered
            neighbor.path = True
            
            # Draw after adding each neighbor to show consideration
            for row in grid:
                for cell in row:
                    cell.draw(surface)
            update_streamlit(surface, placeholder)
        
        # Use a delay that works well in both local and hosted environments
        time.sleep(0.1)
    
    # Failed to find solution
    progress_bar.progress(1.0)
    status_text.text(f"No solution found after {steps} steps.")
    print(f"DFS failed to find solution after {steps} steps")
    return False

def breadth_first_search(grid, width, height, surface, placeholder):
    """Breadth-first search algorithm for maze solving"""
    start = grid[0][0]
    end = grid[height - 1][width - 1]
    
    # Progress display for Streamlit
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    queue = [(start, [])]
    visited = set([(start.x, start.y)])
    
    steps = 0
    max_steps = width * height * 2  # Approximate max steps
    
    while queue:
        steps += 1
        
        # Update progress bar
        progress = min(steps / max_steps, 0.99)
        progress_bar.progress(progress)
        status_text.text(f"BFS Search: Exploring cell {steps}")
        
        current, path = queue.pop(0)
        
        # Highlight current cell being explored
        current.path = True
        
        # Reset all previously explored cells to normal visited state
        for row in grid:
            for cell in row:
                if cell != current and (cell.x, cell.y) in visited and not cell.solution:
                    cell.path = False
        
        # Draw current state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update Streamlit with current state
        update_streamlit(surface, placeholder)
        
        # Check if we reached the end
        if current == end:
            # Visualize solution path
            for cell in path + [current]:
                cell.solution = True
                cell.path = False
            
            # Draw final solution
            for row in grid:
                for cell in row:
                    cell.draw(surface)
            
            update_streamlit(surface, placeholder)
            
            # Complete the progress bar
            progress_bar.progress(1.0)
            status_text.text(f"Solution found in {steps} steps!")
            
            print(f"BFS found solution in {steps} steps")
            return True
        
        # Get possible moves
        neighbors = []
        x, y = current.x, current.y
        
        # Check each direction
        directions = [
            ("left", -1, 0), 
            ("right", 1, 0), 
            ("top", 0, -1), 
            ("bottom", 0, 1)
        ]
        
        for direction, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not current.walls[direction] and (nx, ny) not in visited:
                neighbor = grid[ny][nx]
                neighbors.append(neighbor)
                visited.add((nx, ny))
                
                # Briefly highlight each neighbor as it's discovered
                neighbor.path = True
                
                # Draw to show the wavefront expansion
                for row in grid:
                    for cell in row:
                        cell.draw(surface)
                update_streamlit(surface, placeholder)
        
        # Add neighbors to queue
        for neighbor in neighbors:
            queue.append((neighbor, path + [current]))
        
        # Use a delay that works well in both local and hosted environments
        time.sleep(0.1)
    
    # Failed to find solution
    progress_bar.progress(1.0)
    status_text.text(f"No solution found after {steps} steps.")
    print(f"BFS failed to find solution after {steps} steps")
    return False

# Perform one step of A* algorithm
def step_a_star(surface, placeholder):
    """Perform one step of A* algorithm"""
    state = st.session_state.solving_state
    grid = state['grid']
    width = state['width']
    height = state['height']
    end = grid[height - 1][width - 1]
    
    # No more steps if algorithm is complete
    if state['complete']:
        return state['solution_found']
    
    # No more steps if open_set is empty
    if not state['open_set']:
        state['complete'] = True
        return False
    
    # Get node with lowest f_score
    state['open_set'].sort(key=lambda x: x[0])
    _, current, path = state['open_set'].pop(0)
    state['current'] = current
    state['path'] = path
    
    # Skip if already processed
    if (current.x, current.y) in state['closed_set']:
        return False
    
    # Highlight current cell being explored
    current.path = True
    
    # Reset all previously explored cells to normal visited state
    for cell_pos in state['closed_set']:
        x, y = cell_pos
        if grid[y][x] != current and not grid[y][x].solution:
            grid[y][x].path = False
    
    # Add to closed set
    state['closed_set'].add((current.x, current.y))
    
    # Check if we reached the end
    if current == end:
        # Visualize solution path
        for cell in path + [current]:
            cell.solution = True
            cell.path = False
        
        state['complete'] = True
        state['solution_found'] = True
        
        # Draw final state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update display
        update_streamlit(surface, placeholder)
        
        return True
    
    # Get possible moves
    neighbors = []
    x, y = current.x, current.y
    
    # Check each direction
    if not current.walls["left"]:
        neighbors.append(grid[y][x - 1])
    if not current.walls["right"]:
        neighbors.append(grid[y][x + 1])
    if not current.walls["top"]:
        neighbors.append(grid[y - 1][x])
    if not current.walls["bottom"]:
        neighbors.append(grid[y + 1][x])
    
    # Process neighbors
    for neighbor in neighbors:
        nx, ny = neighbor.x, neighbor.y
        
        # Skip if in closed set
        if (nx, ny) in state['closed_set']:
            continue
        
        # Calculate tentative g_score
        tentative_g = state['g_score'].get((current.x, current.y), float('inf')) + 1
        
        # Skip if not better path
        if (nx, ny) in state['g_score'] and tentative_g >= state['g_score'][(nx, ny)]:
            continue
        
        # This path is better
        state['g_score'][(nx, ny)] = tentative_g
        state['f_score'][(nx, ny)] = tentative_g + heuristic(neighbor, end)
        
        # Briefly highlight the neighbor being considered
        neighbor.path = True
        
        # Add to open set
        state['open_set'].append((state['f_score'][(nx, ny)], neighbor, path + [current]))
    
    # Increment step counter
    state['step'] += 1
    
    # Draw current state
    for row in grid:
        for cell in row:
            cell.draw(surface)
    
    # Update display
    update_streamlit(surface, placeholder)
    
    return False

# Perform one step of BFS algorithm
def step_bfs(surface, placeholder):
    """Perform one step of BFS algorithm"""
    state = st.session_state.solving_state
    grid = state['grid']
    width = state['width']
    height = state['height']
    end = grid[height - 1][width - 1]
    
    # No more steps if algorithm is complete
    if state['complete']:
        return state['solution_found']
    
    # No more steps if queue is empty
    if not state['queue']:
        state['complete'] = True
        return False
    
    # Get next cell from queue
    current, path = state['queue'].pop(0)
    state['current'] = current
    state['path'] = path
    
    # Highlight current cell being explored
    current.path = True
    
    # Reset all previously explored cells to normal visited state
    for row in grid:
        for cell in row:
            if cell != current and (cell.x, cell.y) in state['visited'] and not cell.solution:
                cell.path = False
    
    # Check if we reached the end
    if current == end:
        # Visualize solution path
        for cell in path + [current]:
            cell.solution = True
            cell.path = False
        
        state['complete'] = True
        state['solution_found'] = True
        
        # Draw final state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update display
        update_streamlit(surface, placeholder)
        
        return True
    
    # Get possible moves
    neighbors = []
    x, y = current.x, current.y
    
    # Check each direction
    directions = [
        ("left", -1, 0), 
        ("right", 1, 0), 
        ("top", 0, -1), 
        ("bottom", 0, 1)
    ]
    
    for direction, dx, dy in directions:
        nx, ny = x + dx, y + dy
        if not current.walls[direction] and (nx, ny) not in state['visited']:
            neighbor = grid[ny][nx]
            neighbors.append(neighbor)
            state['visited'].add((nx, ny))
            
            # Briefly highlight each neighbor as it's discovered
            neighbor.path = True
    
    # Add neighbors to queue
    for neighbor in neighbors:
        state['queue'].append((neighbor, path + [current]))
    
    # Increment step counter
    state['step'] += 1
    
    # Draw current state
    for row in grid:
        for cell in row:
            cell.draw(surface)
    
    # Update display
    update_streamlit(surface, placeholder)
    
    return False

# Perform one step of DFS algorithm
def step_dfs(surface, placeholder):
    """Perform one step of DFS algorithm"""
    state = st.session_state.solving_state
    grid = state['grid']
    width = state['width']
    height = state['height']
    end = grid[height - 1][width - 1]
    
    # No more steps if algorithm is complete
    if state['complete']:
        return state['solution_found']
    
    # No more steps if stack is empty
    if not state['stack']:
        state['complete'] = True
        return False
    
    # Get next cell from stack
    current, path = state['stack'].pop()
    state['current'] = current
    state['path'] = path
    
    # Skip if already visited
    if (current.x, current.y) in state['visited']:
        return False
    
    # Mark as visited
    state['visited'].add((current.x, current.y))
    
    # Highlight current cell being explored
    current.path = True
    
    # Reset all previously explored cells to normal visited state
    for row in grid:
        for cell in row:
            if cell != current and (cell.x, cell.y) in state['visited'] and not cell.solution:
                cell.path = False
    
    # Check if we reached the end
    if current == end:
        # Visualize solution path
        for cell in path + [current]:
            cell.solution = True
            cell.path = False
        
        state['complete'] = True
        state['solution_found'] = True
        
        # Draw final state
        for row in grid:
            for cell in row:
                cell.draw(surface)
        
        # Update display
        update_streamlit(surface, placeholder)
        
        return True
    
    # Get possible moves
    neighbors = []
    x, y = current.x, current.y
    
    # Check each direction - in reverse order for DFS visualization
    if not current.walls["bottom"] and (x, y + 1) not in state['visited']:
        neighbors.append(grid[y + 1][x])
    if not current.walls["top"] and (x, y - 1) not in state['visited']:
        neighbors.append(grid[y - 1][x])
    if not current.walls["right"] and (x + 1, y) not in state['visited']:
        neighbors.append(grid[y][x + 1])
    if not current.walls["left"] and (x - 1, y) not in state['visited']:
        neighbors.append(grid[y][x - 1])
    
    # Add neighbors to stack
    for neighbor in neighbors:
        state['stack'].append((neighbor, path + [current]))
        
        # Briefly highlight the neighbor being considered
        neighbor.path = True
    
    # Increment step counter
    state['step'] += 1
    
    # Draw current state
    for row in grid:
        for cell in row:
            cell.draw(surface)
    
    # Update display
    update_streamlit(surface, placeholder)
    
    return False

# Heuristic function for A* (Manhattan distance)
def heuristic(cell, goal):
    return abs(cell.x - goal.x) + abs(cell.y - goal.y)

# Function for manual maze solving
def manual_solve_maze(grid, width, height, surface, placeholder):
    # Initialize player position in session state if not already present
    if 'player_pos' not in st.session_state:
        st.session_state.player_pos = [0, 0]
        st.session_state.move_history = []
        st.session_state.breadcrumbs = set()
        st.session_state.game_won = False
    
    player_x, player_y = st.session_state.player_pos
    goal_x, goal_y = width - 1, height - 1
    
    # Clear previous player and goal markings
    for y in range(height):
        for x in range(width):
            grid[y][x].player = False
            grid[y][x].breadcrumb = False
    
    # Mark start, goal and breadcrumbs
    grid[player_y][player_x].player = True
    grid[goal_y][goal_x].goal = True
    
    # Mark breadcrumbs
    for x, y in st.session_state.breadcrumbs:
        if not (x == player_x and y == player_y) and not (x == goal_x and y == goal_y):
            grid[y][x].breadcrumb = True
    
    # Define movement handlers
    def move_up():
        if player_y > 0 and not grid[player_y][player_x].walls["top"]:
            st.session_state.breadcrumbs.add((player_x, player_y))
            st.session_state.player_pos[1] -= 1
            return True
        return False
    
    def move_down():
        if player_y < height - 1 and not grid[player_y][player_x].walls["bottom"]:
            st.session_state.breadcrumbs.add((player_x, player_y))
            st.session_state.player_pos[1] += 1
            return True
        return False
    
    def move_left():
        if player_x > 0 and not grid[player_y][player_x].walls["left"]:
            st.session_state.breadcrumbs.add((player_x, player_y))
            st.session_state.player_pos[0] -= 1
            return True
        return False
    
    def move_right():
        if player_x < width - 1 and not grid[player_y][player_x].walls["right"]:
            st.session_state.breadcrumbs.add((player_x, player_y))
            st.session_state.player_pos[0] += 1
            return True
        return False
    
    # Initial draw
    for row in grid:
        for cell in row:
            cell.draw(surface)
    update_streamlit(surface, placeholder)
    
    # Set up terminal control panel with proper styling
    st.markdown("""
    <div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; margin-bottom: 20px; font-family: 'Courier New', monospace;">
    <span style="color: #00FF00;">[TERMINAL]</span> Navigation Controls
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        left_button = st.button("cd ../  [A]")
    
    with col2:
        up_button = st.button("cd ..↑  [W]")
        down_button = st.button("cd .↓  [S]")
    
    with col3:
        right_button = st.button("cd ./  [D]")
    
    # Create a container for the keyboard instructions
    key_instructions = st.empty()
    key_instructions.markdown("""
    <div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; font-family: 'Courier New', monospace;">
    <span style="color: #00FF00;">root@terminal:~$</span> echo "Use commands to navigate. WASD keys accepted."
    </div>
    """, unsafe_allow_html=True)
    
    # Container for move messages
    move_message = st.empty()
    
    # Container for completion message
    completion_message = st.empty()
    
    # Handle button clicks
    moved = False
    
    if 'last_action' not in st.session_state:
        st.session_state.last_action = None
    
    # Only process a move if we haven't won yet
    if not st.session_state.game_won:
        if left_button and st.session_state.last_action != "left":
            moved = move_left()
            st.session_state.last_action = "left"
        elif right_button and st.session_state.last_action != "right":
            moved = move_right()
            st.session_state.last_action = "right"
        elif up_button and st.session_state.last_action != "up":
            moved = move_up()
            st.session_state.last_action = "up"
        elif down_button and st.session_state.last_action != "down":
            moved = move_down()
            st.session_state.last_action = "down"
        else:
            # Reset last action to allow next button press
            st.session_state.last_action = None
    
        # Handle key presses through terminal-style text input
        key_input = st.text_input("root@terminal:~$", key="key_input", 
                                 help="Type: w (up), s (down), a (left), d (right), reset (start over)")
        
        # Process the key input
        if key_input and key_input.lower() not in st.session_state.get('processed_keys', set()):
            if 'processed_keys' not in st.session_state:
                st.session_state.processed_keys = set()
            
            last_key = key_input.lower()
            st.session_state.processed_keys.add(last_key)
            
            if last_key == 'w':
                moved = move_up()
            elif last_key == 's':
                moved = move_down()
            elif last_key == 'a':
                moved = move_left()
            elif last_key == 'd':
                moved = move_right()
            elif last_key == 'reset':
                st.session_state.player_pos = [0, 0]
                st.session_state.move_history = []
                st.session_state.breadcrumbs = set()
                moved = False
            
            # Clear the input field after processing
            st.session_state.key_input = ""
    
    # Update position and check for goal after movement
    player_x, player_y = st.session_state.player_pos
    
    # Update move message
    if moved:
        move_message.markdown(">_System: *Movement successful.* Coordinates updated.")
        st.session_state.move_history.append((player_x, player_y))
    elif (left_button or right_button or up_button or down_button or 
          (key_input and key_input.lower() not in st.session_state.get('processed_keys', set()))):
        move_message.markdown(">_System: **ACCESS DENIED** - Firewall detected.")
    
    # Check for goal
    if player_x == goal_x and player_y == goal_y and not st.session_state.game_won:
        st.session_state.game_won = True
        completion_message.markdown("""
        >_System: **SECURITY BREACH SUCCESSFUL!**
        >
        >_System: You have infiltrated the mainframe.
        >
        >_System: Connection secure. Data downloading...
        """)
    
    # Redraw with updated player position
    for row in grid:
        for cell in row:
            cell.draw(surface)
    update_streamlit(surface, placeholder)
    
    # Display move counter in hacker theme
    st.markdown(f">_System: Connection attempts: `{len(st.session_state.move_history)}`")
    
    # Option to show solution with terminal styling
    if st.button("sudo ./auto_hack.sh"):
        # Use A* to find the solution
        # First, reset player visualization so it doesn't interfere
        grid[player_y][player_x].player = False
        # Save breadcrumbs
        saved_breadcrumbs = [(x, y) for y in range(height) for x in range(width) if grid[y][x].breadcrumb]
        
        # Initialize recording if enabled
        if record_process and not ('recording' in st.session_state and st.session_state.recording):
            st.session_state.recording = True
            st.session_state.frames = []
        
        # Run the algorithm
        a_star_algorithm(grid, width, height, surface, placeholder)
        
        # Create and offer download for recording if enabled
        if 'recording' in st.session_state and st.session_state.recording and st.session_state.frames:
            st.markdown("""
            <div style="border: 3px solid #00FF00; background-color: #001100; padding: 15px; margin: 20px 0; font-family: 'Courier New', monospace; text-align: center;">
            <h2 style="color: #00FF00; margin-bottom: 10px;">■ RECORDING COMPLETE ■</h2>
            <p style="color: #00FF00;">Preparing download - please wait...</p>
            </div>
            """, unsafe_allow_html=True)
            
            download_container = st.empty()
            with st.spinner("Encoding video..."):
                download_container.info(f"Processing {len(st.session_state.frames)} frames into MP4 video...")
                video_bytes, filename = create_video_from_frames(st.session_state.frames, fps=record_fps)
                
                if video_bytes:
                    download_container.success(f"✅ Video created successfully! ({len(video_bytes) / 1024:.1f} KB)")
                    
                    # Display prominent download button
                    st.markdown(
                        get_binary_file_downloader_html(video_bytes, filename, "DOWNLOAD RECORDING"),
                        unsafe_allow_html=True
                    )
                    
                    # Add information about the recording
                    st.markdown(f"""
                    <div style="font-family: 'Courier New', monospace; color: #00FF00; margin-top: 10px; padding: 10px; background-color: #001100; border: 1px solid #00FF00;">
                    <code>root@terminal:~$ file {filename}</code><br>
                    <code>{filename}: MP4 video, {len(st.session_state.frames)} frames @ {record_fps} FPS, {len(video_bytes) / 1024:.1f} KB</code>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to create video. Please try again with fewer frames or a different recording setting.")
            
            # Reset recording state
            st.session_state.recording = False
        
        # Restore player position and breadcrumbs
        grid[player_y][player_x].player = True
        for x, y in saved_breadcrumbs:
            grid[y][x].breadcrumb = True
        
        # Update display
        for row in grid:
            for cell in row:
                cell.draw(surface)
        update_streamlit(surface, placeholder)
    
    # Add option to reset game with terminal styling
    if st.button("sudo reboot"):
        st.session_state.player_pos = [0, 0]
        st.session_state.move_history = []
        st.session_state.breadcrumbs = set()
        st.session_state.game_won = False
        st.session_state.processed_keys = set()
        
        # Redraw with reset state
        for row in grid:
            for cell in row:
                cell.breadcrumb = False
                cell.solution = False
                
        grid[0][0].player = True
        grid[height-1][width-1].goal = True
        
        for row in grid:
            for cell in row:
                cell.draw(surface)
        update_streamlit(surface, placeholder)

# Store the solving state in session_state
if 'solving_state' not in st.session_state:
    st.session_state.solving_state = {
        'step': 0,
        'algorithm': None,
        'complete': False,
        'grid': None,
        'width': 0,
        'height': 0,
        'open_set': [],
        'closed_set': set(),
        'g_score': {},
        'f_score': {},
        'queue': [],
        'stack': [],
        'visited': set(),
        'current': None,
        'path': [],
        'solution_found': False,
        'auto_advance': False
    }

# Convert surface to PIL Image for display
def pygame_surface_to_image(surface):
    """Convert pygame surface to PIL Image"""
    pygame_image = pygame.surfarray.array3d(surface)
    pygame_image = np.transpose(pygame_image, [1, 0, 2])  # Transpose to get correct orientation
    image = Image.fromarray(pygame_image.astype('uint8'))
    return image

def create_video_from_frames(frames, fps=10):
    """Create a video file from a list of frames"""
    if not frames:
        st.error("No frames were captured during recording")
        return None, None
    
    st.info(f"Creating video from {len(frames)} frames at {fps} FPS...")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"maze_recording_{timestamp}.mp4"
    
    try:
        # Create a temporary buffer for the video
        buffer = io.BytesIO()
        
        # Use imageio to write directly to the buffer
        with imageio.get_writer(buffer, format='mp4', fps=fps) as writer:
            for frame in frames:
                writer.append_data(np.array(frame))
        
        # Reset buffer position to the beginning
        buffer.seek(0)
        
        # Read the video data
        video_bytes = buffer.getvalue()
        
        return video_bytes, filename
    except Exception as e:
        st.error(f"Error creating video: {str(e)}")
        return None, None

def get_binary_file_downloader_html(bin_file, file_label='File', button_text='Download Video'):
    """Generate HTML code for a download button for binary data"""
    b64 = base64.b64encode(bin_file).decode()
    
    button_html = f'''
    <div style="text-align: center; margin: 20px 0; padding: 10px; border: 2px solid #00FF00; background-color: #001100;">
        <h3 style="color: #00FF00; font-family: 'Courier New', monospace;">VIDEO READY FOR EXTRACTION</h3>
        <a href="data:video/mp4;base64,{b64}" download="{file_label}">
            <button style="color: #000000; background-color: #00FF00; border: none; padding: 10px 20px; 
                   font-size: 16px; cursor: pointer; font-family: 'Courier New', monospace; font-weight: bold;">
                {button_text} ⬇️
            </button>
        </a>
        <p style="color: #00FF00; font-family: 'Courier New', monospace; margin-top: 10px;">
            Click the button above to download the video recording
        </p>
    </div>
    '''
    return button_html

# Main Streamlit app logic
st.markdown("""
<div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; margin-bottom: 20px; font-family: 'Courier New', monospace;">
<span style="color: #00FF00;">[SYSTEM]</span> Launch Controls
</div>
""", unsafe_allow_html=True)

if st.button("$ ./initialize_grid.sh"):
    if 'move_history' in st.session_state:
        st.session_state.move_history = []
    if 'player_pos' in st.session_state:
        st.session_state.player_pos = [0, 0]
    if 'breadcrumbs' in st.session_state:
        st.session_state.breadcrumbs = set()
    if 'game_won' in st.session_state:
        st.session_state.game_won = False
    if 'processed_keys' in st.session_state:
        st.session_state.processed_keys = set()
    
    # Initialize maze grid
    grid = [[Cell(x, y) for x in range(maze_width)] for y in range(maze_height)]
    
    # Initialize pygame surface
    surface = init_pygame_surface(maze_width, maze_height)
    
    # Create image placeholder
    placeholder = st.empty()
    
    # Generate maze
    st.markdown(">_System: Generating security grid layout...")
    if generation_algorithm == "Recursive Backtracking":
        recursive_backtracking(grid, maze_width, maze_height, surface, placeholder)
    elif generation_algorithm == "Kruskal's Algorithm":
        kruskals_algorithm(grid, maze_width, maze_height, surface, placeholder)
    elif generation_algorithm == "Prim's Algorithm":
        prims_algorithm(grid, maze_width, maze_height, surface, placeholder)
    
    # Draw the maze after generation
    for row in grid:
        for cell in row:
            cell.draw(surface)
    
    update_streamlit(surface, placeholder)
    
    # Store the grid in session state
    st.session_state.grid = grid
    st.session_state.surface = surface
    st.session_state.placeholder = placeholder
    
    # Handle solving mode
    if mode == "Automatic Breach":
        # Solve maze
        st.markdown(">_System: Executing automatic breach protocol...")
        if solving_algorithm == "Depth-First Search":
            depth_first_search(grid, maze_width, maze_height, surface, placeholder)
        elif solving_algorithm == "Breadth-First Search":
            breadth_first_search(grid, maze_width, maze_height, surface, placeholder)
        elif solving_algorithm == "A* Algorithm":
            a_star_algorithm(grid, maze_width, maze_height, surface, placeholder)
        
        st.markdown(">_System: Breach successful. Security grid infiltrated.")
        
        # Create and offer download for recording if enabled
        if 'recording' in st.session_state and st.session_state.recording and st.session_state.frames:
            st.markdown("""
            <div style="border: 1px solid #00FF00; background-color: #000000; padding: 10px; margin: 20px 0; font-family: 'Courier New', monospace;">
            <span style="color: #00FF00;">[SYSTEM]</span> Recording Complete - Download Available
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner("Processing recording..."):
                video_bytes, filename = create_video_from_frames(st.session_state.frames, fps=record_fps)
                
                if video_bytes:
                    st.markdown(
                        get_binary_file_downloader_html(video_bytes, filename, "$ ./download_recording.sh"),
                        unsafe_allow_html=True
                    )
                    
                    # Add information about the recording
                    st.markdown(f"""
                    <div style="font-family: 'Courier New', monospace; color: #00FF00; margin-top: 10px;">
                    <span style="color: #00FF00;">root@terminal:~$</span> file {filename}
                    <br>{filename}: MP4 video, {len(st.session_state.frames)} frames @ {record_fps} FPS
                    </div>
                    """, unsafe_allow_html=True)
            
            # Reset recording state
            st.session_state.recording = False
    else:  # Manual Solving
        st.markdown(">_System: Manual infiltration mode engaged. Awaiting operator commands.")
        manual_solve_maze(grid, maze_width, maze_height, surface, placeholder)

# If we have a grid in session state and we're in manual mode, show the manual solver
elif 'grid' in st.session_state and mode == "Manual Infiltration":
    st.markdown(">_System: Continuing infiltration sequence:")
    manual_solve_maze(st.session_state.grid, maze_width, maze_height, 
                      st.session_state.surface, st.session_state.placeholder)
