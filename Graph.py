import pygame
import sys
import heapq
from collections import deque, defaultdict

# Screen dimensions
WIDTH, HEIGHT = 600, 600
NODE_RADIUS = 20
NODE_COLOR = (100, 149, 237)
VISITED_COLOR = (255, 69, 0)
EDGE_COLOR = (192, 192, 192)
FONT_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Traversal Visualization")
font = pygame.font.Font(None, 24)

# Graph representation
class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)
        self.positions = {}

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))  # Assuming undirected graph

    def add_node(self, node, position):
        self.positions[node] = position

    def draw(self, visited=None):
        screen.fill((255, 255, 255))
        
        # Draw edges
        for u in self.adj_list:
            for v, _ in self.adj_list[u]:
                pygame.draw.line(screen, EDGE_COLOR, self.positions[u], self.positions[v], 2)

        # Draw nodes
        for node, pos in self.positions.items():
            color = VISITED_COLOR if visited and node in visited else NODE_COLOR
            pygame.draw.circle(screen, color, pos, NODE_RADIUS)
            label = font.render(str(node), True, FONT_COLOR)
            screen.blit(label, (pos[0] - label.get_width() // 2, pos[1] - label.get_height() // 2))

        pygame.display.flip()

    def depth_first_search(self, start):
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                self.draw(visited)
                pygame.time.delay(500)
                for neighbor, _ in self.adj_list[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited

    def breadth_first_search(self, start):
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                self.draw(visited)
                pygame.time.delay(500)
                for neighbor, _ in self.adj_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return visited

    def dijkstra(self, start):
        visited = set()
        distances = {node: float('inf') for node in self.positions}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, node = heapq.heappop(priority_queue)
            if node not in visited:
                visited.add(node)
                self.draw(visited)
                pygame.time.delay(500)

                for neighbor, weight in self.adj_list[node]:
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(priority_queue, (distance, neighbor))

        return distances

# Create the graph and add nodes/edges
graph = Graph()
positions = {
    'A': (100, 100),
    'B': (200, 150),
    'C': (300, 100),
    'D': (400, 200),
    'E': (500, 100),
    'F': (300, 300)
}
for node, pos in positions.items():
    graph.add_node(node, pos)

edges = [
    ('A', 'B', 1),
    ('B', 'C', 1),
    ('C', 'D', 2),
    ('D', 'E', 1),
    ('A', 'C', 2),
    ('B', 'F', 3),
    ('F', 'D', 1)
]
for u, v, weight in edges:
    graph.add_edge(u, v, weight)

# Main loop to run different traversal algorithms
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                graph.depth_first_search('A')
            elif event.key == pygame.K_b:
                graph.breadth_first_search('A')
            elif event.key == pygame.K_k:
                distances = graph.dijkstra('A')
                print("Dijkstra's distances:", distances)

    pygame.display.flip()

pygame.quit()
sys.exit()
