import pygame
import sys
import heapq
from collections import deque, defaultdict

WIDTH, HEIGHT = 600, 600
NODE_RADIUS = 20
NODE_COLOR = (100, 149, 237)
VISITED_COLOR = (255, 69, 0)
SHORTEST_PATH_COLOR = (50, 205, 50)
EDGE_COLOR = (192, 192, 192)
FONT_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Traversal Visualization")
font = pygame.font.Font(None, 24)

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)
        self.positions = {}

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))  # Assuming undirected graph

    def add_node(self, node, position):
        self.positions[node] = position

    def draw(self, visited=None, shortest_path=None):
        screen.fill((255, 255, 255))
        
        # Draw edges
        for u in self.adj_list:
            for v, _ in self.adj_list[u]:
                pygame.draw.line(screen, EDGE_COLOR, self.positions[u], self.positions[v], 2)

        if shortest_path:
            for i in range(len(shortest_path) - 1):
                u, v = shortest_path[i], shortest_path[i + 1]
                pygame.draw.line(screen, SHORTEST_PATH_COLOR, self.positions[u], self.positions[v], 4)

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

    def dijkstra(self, start, target):
        visited = set()
        distances = {node: float('inf') for node in self.positions}
        distances[start] = 0
        previous_nodes = {node: None for node in self.positions}
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, node = heapq.heappop(priority_queue)
            if node in visited:
                continue
            visited.add(node)
            self.draw(visited)

            if node == target:
                break

            for neighbor, weight in self.adj_list[node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = node
                    heapq.heappush(priority_queue, (distance, neighbor))
            
            pygame.time.delay(500)

        # Reconstruct the shortest path
        path = []
        while target is not None:
            path.append(target)
            target = previous_nodes[target]
        path.reverse()

        # Draw final shortest path
        self.draw(visited, path)
        return path

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # Run Depth-First Search
                graph.depth_first_search('A')
            elif event.key == pygame.K_b:  # Run Breadth-First Search
                graph.breadth_first_search('A')
            elif event.key == pygame.K_k:  # Run Dijkstra's algorithm with shortest path visualization
                shortest_path = graph.dijkstra('A', 'E')
                print("Shortest path from A to E:", shortest_path)

    pygame.display.flip()

pygame.quit()
sys.exit()
