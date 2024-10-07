import pygame
import sys
import random
from tkinter import messagebox, Tk

pygame.init()

SCREEN_WIDTH = 240  
SCREEN_HEIGHT = 320  
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 80
ROWS = 4 
COLUMNS = 3  

BACKGROUND_COLOR = (255, 255, 255) 

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dirt Blocks Grid")

dirt_block=pygame.image.load("Block.jpg")
dirt_block = pygame.transform.scale(dirt_block, (BLOCK_WIDTH, BLOCK_HEIGHT))

blocks = []
for row in range(ROWS):
    for col in range(COLUMNS):
        x = col * BLOCK_WIDTH
        y = row * BLOCK_HEIGHT
        blocks.append(pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT))

root = Tk()
root.withdraw()

click_count = 0
failed_attempts = 0 

MINERAL_DROP_CHANCE = 30 
MINERAL_TYPES = {
    "gold": 50,    # 50% chance for gold
    "silver": 30,  # 30% chance for silver
    "diamond": 20  # 20% chance for diamond
}

def get_mineral():
    rand_val = random.randint(1, 100)
    cumulative = 0
    for mineral, chance in MINERAL_TYPES.items():
        cumulative += chance
        if rand_val <= cumulative:
            return mineral
    return None

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any block was clicked
            for block in blocks:
                if block.collidepoint(event.pos):
                    click_count += 1 

                    if random.random() <= 0.5:
                        blocks.remove(block)  # Remove the block (make it disappear)
                        
                        mineral_dropped = False
                        if random.random() <= MINERAL_DROP_CHANCE or failed_attempts >= 3:
                            mineral = get_mineral()
                            messagebox.showinfo("You found a mineral!", f"Congratulations! You found {mineral}!")
                            mineral_dropped = True
                            failed_attempts = 0  # Reset failed attempts on mineral drop
                        
                        if failed_attempts >= 3 and not mineral_dropped:
                            mineral = get_mineral()
                            messagebox.showinfo("Guaranteed Mineral!", f"You have now received {mineral}!")
                            failed_attempts = 0  # Reset failed attempts

    screen.fill(BACKGROUND_COLOR)

    # Draw blocks
    for block in blocks:
        screen.blit(dirt_block, block.topleft) 

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
