import math
import pygame
import random
width=1270
height=720
agents = []
Max_Speed=5

class Agent:
    def __init__(self,x,y) -> None:
        self.pos = pygame.Vector2(x, y)
        self.velocity= pygame.Vector2(0,0)
        self.acceleration=pygame.Vector2(0,0)
        self.mass=1

    def update(self):
        self.velocity=self.velocity + self.acceleration
        if self.velocity.length() > Max_Speed:
            self.velocity= self.velocity.normalize()* Max_Speed
        self.pos=self.pos +self.velocity
        self.acceleration=pygame.Vector2(0,0)

    def apply_force(self,x,y):
        force=pygame.Vector2(x,y)
        self.acceleration=self.acceleration+ (force/self.mass)
    
    def seek(self,x,y):
        d= pygame.Vector2(x,y)-self.pos
        d=d.normalize()*0.1
        seeking_force=d
        self.apply_force(seeking_force.x,seeking_force.y)

    def coherence(self, agents):

        center_of_mass=pygame.Vector2(0,0)
        agent_in_range_count=0
        for agent in agents:
            if agent != self:
                dist= math.sqrt((self.pos.x- agent.pos.x)**2 
                            + (self.pos.y-agent.pos.y)**2)
                if dist <200:
                    center_of_mass+=agent.pos
                    agent_in_range_count += 1

        if agent_in_range_count >0:
            center_of_mass /= agent_in_range_count
        d=center_of_mass-self.pos
        f=d.normalize() * 0.1
        self.apply_force(f.x,f.y)
    
    def seperation(self,agents):
        
        d= pygame.Vector2(0,0)
        for agent in agents:
            dist= math.sqrt((self.pos.x- agent.pos.x)**2 
                            + (self.pos.y-agent.pos.y)**2)
            if dist <30:
                d+=self.pos - agent.pos

        seperation_force=d * 0.01
        self.apply_force(seperation_force.x,seperation_force.y)

    def alignment(self, agents):
        v=pygame.Vector2(0,0)
        for agent in agents:
            if agent != self:
                v+=agent.velocity

        v/= len(agents)-1
        alignment_f=v*0.1
        self.apply_force(alignment_f.x,alignment_f.y)

    def draw(self):
        pygame.draw.circle(screen, "pink", self.pos , 10)
    
for i in range(100) : 
    agents.append(Agent(random.uniform(0,width),random.uniform(0,height)))

# pygame setup
pygame.init()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

while running:
    # poll for eventsd
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightblue")

    for agent in agents:
        agent.coherence(agents)
        agent.seperation(agents)
        agent.alignment(agents)
        agent.update()
        agent.draw()

    for agent in agents:
        if agent.pos.x > width +1:
            agent.pos.x=1
        elif agent.pos.x<0:
            agent.pos.x=width
        if agent.pos.y > height +1:
            agent.pos.y=1
        elif agent.pos.y<0:
            agent.pos.y=height
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
