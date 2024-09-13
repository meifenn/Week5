import pygame
import random

# pygame setup
pygame.init()

# Agent settings
agentCOUNT = 5
agentSIZE = 20
agentSPEED = 2
# Define different colors for each agent
AGENT_COLORS = [(255, 32, 0), (87, 255, 0), (99, 0, 255), (255, 176, 0), (255, 0, 255)]

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Agent:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.speed = agentSPEED
        self.color = color

    def move_towards(self, target):
        direction = pygame.Vector2(target) - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
            self.pos += direction * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), agentSIZE)

# Create exactly 5 agents at random positions with different colors
agents = [Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), AGENT_COLORS[i]) for i in range(agentCOUNT)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightblue")

    # Draw player
    pygame.draw.circle(screen, "pink", player_pos, 40)

    # Move agents towards player
    for agent in agents:
        agent.move_towards(player_pos)

    # Draw agents
    for agent in agents:
        agent.draw(screen)

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
