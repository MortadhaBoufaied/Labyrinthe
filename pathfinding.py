# pathfinding.py
import heapq

class Pathfinding:
    def __init__(self, grid):
        self.grid = grid

    # Fonction Dijkstra pour trouver le chemin
    def dijkstra(self, start, end):
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    priority = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current
        return []

    # Fonction de voisinage
    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                if self.grid[ny][nx] == 0:  # Si la case est libre
                    neighbors.append((nx, ny))
        return neighbors

    # Heuristique pour A*
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

